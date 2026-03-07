import sys
import os
import sysconfig
import re
import requests
import subprocess
from packaging.version import parse as parse_version, InvalidVersion
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QMessageBox, QProgressBar, QCheckBox, QTextEdit, QComboBox, QLabel
)
from PySide6.QtCore import Qt, QThread, Signal


# -------------------- HELPERS --------------------

def is_venv():
    """Check if running in a virtual environment."""
    return (hasattr(sys, 'real_prefix') or 
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))


def detect_package_managers():
    """Detect available package managers on the system."""
    managers = {}
    
    # Check for pip
    try:
        result = subprocess.run(["pip", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            managers['pip'] = 'pip'
    except Exception:
        pass
    
    # Check for pipx
    try:
        result = subprocess.run(["pipx", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            managers['pipx'] = 'pipx'
    except Exception:
        pass
    
    # Check for uv
    try:
        result = subprocess.run(["uv", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            managers['uv'] = 'uv'
    except Exception:
        pass
    
    # Check for poetry
    try:
        result = subprocess.run(["poetry", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            managers['poetry'] = 'poetry'
    except Exception:
        pass
    
    # Check for conda
    try:
        result = subprocess.run(["conda", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            managers['conda'] = 'conda'
    except Exception:
        pass
    
    # Check for pip3
    try:
        result = subprocess.run(["pip3", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and 'pip' not in managers:
            managers['pip3'] = 'pip3'
    except Exception:
        pass
    
    return managers


def get_standard_libs():
    std_lib = sysconfig.get_paths()["stdlib"]
    std_libs = set()
    for root, _, files in os.walk(std_lib):
        for file in files:
            if file.endswith(".py"):
                rel_path = os.path.relpath(os.path.join(root, file), std_lib)
                module = rel_path.replace(os.sep, ".").rsplit(".py", 1)[0]
                std_libs.add(module.split(".")[0])
    return std_libs


def clean_and_merge_requirements(reqs, log_fn):
    clean_reqs = {}
    pattern = re.compile(r"^([A-Za-z0-9_.\-]+)\s*([=<>!~]*.*)?$")

    for r in reqs:
        r = r.strip()
        if not r or r.startswith("#") or "@ file://" in r:
            continue

        match = pattern.match(r)
        if not match:
            log_fn(f"Skipping invalid line: {r}")
            continue

        pkg, spec = match.groups()
        pkg = pkg.lower()
        spec = spec.strip() if spec else ""

        if pkg in clean_reqs:
            old_spec = clean_reqs[pkg]
            try:
                if "==" in spec:
                    new_ver = spec.split("==")[-1]
                    old_ver = old_spec.split("==")[-1] if "==" in old_spec else ""
                    if not old_ver or parse_version(new_ver) > parse_version(old_ver):
                        clean_reqs[pkg] = spec
                else:
                    clean_reqs[pkg] = old_spec or spec
            except InvalidVersion:
                log_fn(f"Invalid version format for {pkg}: {spec}")
                clean_reqs[pkg] = spec or old_spec
        else:
            clean_reqs[pkg] = spec

    return [f"{pkg}{spec}" if spec else pkg for pkg, spec in sorted(clean_reqs.items())]


def validate_on_pypi(requirements, log_fn):
    """Validate each package individually with error handling."""
    valid_reqs = []
    for line in requirements:
        try:
            pkg = re.split(r"[=<>!~]", line)[0].strip()
            if not pkg:
                log_fn(f"Skipping empty package name from line: {line}")
                continue
            
            url = f"https://pypi.org/pypi/{pkg}/json"
            try:
                resp = requests.get(url, timeout=5)
                if resp.status_code == 200:
                    valid_reqs.append(line)
                    log_fn(f"✓ Validated: {pkg}")
                elif resp.status_code == 404:
                    log_fn(f"✗ Package not found on PyPI: {pkg}")
                else:
                    log_fn(f"⚠ Could not validate {pkg} (HTTP {resp.status_code})")
                    # Still include it in case it's a valid package with temporary issues
                    valid_reqs.append(line)
            except requests.exceptions.Timeout:
                log_fn(f"⚠ Timeout validating {pkg}, including anyway")
                valid_reqs.append(line)
            except requests.exceptions.RequestException as e:
                log_fn(f"⚠ Network error validating {pkg}: {type(e).__name__}, including anyway")
                valid_reqs.append(line)
        except Exception as e:
            log_fn(f"✗ Error processing line '{line}': {type(e).__name__}: {str(e)}")
            # Continue with next package even if this one fails
            continue
    
    return valid_reqs


def safe_read_file(file_path, log_fn):
    """Safely read file with multiple encoding attempts and error handling."""
    for enc in ["utf-8-sig", "utf-8", "latin-1", "cp1252"]:
        try:
            with open(file_path, "r", encoding=enc, errors="ignore") as f:
                return f.readlines()
        except FileNotFoundError:
            log_fn(f"✗ File not found: {file_path}")
            return []
        except PermissionError:
            log_fn(f"✗ Permission denied: {file_path}")
            return []
        except Exception as e:
            continue
    log_fn(f"✗ Could not read file with any encoding: {file_path}")
    return []


# -------------------- WORKER THREAD --------------------

class Worker(QThread):
    progress = Signal(int)
    finished = Signal(list)
    log_msg = Signal(str)

    def __init__(self, source_dir, exclude_std, package_manager='pip'):
        super().__init__()
        self.source_dir = source_dir
        self.exclude_std = exclude_std
        self.package_manager = package_manager
        self.std_libs = get_standard_libs() if exclude_std else set()

    def log(self, message):
        self.log_msg.emit(message)

    def run(self):
        requirements = set()
        all_files = []
        
        self.log(f"Starting scan with package manager: {self.package_manager}")
        self.log(f"Scanning directory: {self.source_dir}")
        
        try:
            for root, _, files in os.walk(self.source_dir):
                for file in files:
                    if file.endswith(".py") or file == "requirements.txt":
                        all_files.append(os.path.join(root, file))
        except Exception as e:
            self.log(f"✗ Error walking directory: {type(e).__name__}: {str(e)}")
            self.finished.emit([])
            return

        total_files = len(all_files)
        self.log(f"Found {total_files} files to process")
        
        for idx, file_path in enumerate(all_files):
            try:
                if file_path.endswith(".py"):
                    self.process_python_file(file_path, requirements)
                elif file_path.endswith("requirements.txt"):
                    self.process_requirements_file(file_path, requirements)
            except Exception as e:
                self.log(f"✗ Error processing {file_path}: {type(e).__name__}: {str(e)}")
                # Continue with next file even if this one fails
                continue
            finally:
                self.progress.emit(int((idx + 1) / total_files * 100))

        self.log(f"Found {len(requirements)} unique imports/requirements")
        
        if self.exclude_std:
            before_count = len(requirements)
            requirements = {pkg for pkg in requirements if pkg not in self.std_libs}
            self.log(f"Excluded {before_count - len(requirements)} standard library modules")

        try:
            cleaned = clean_and_merge_requirements(requirements, self.log)
            self.log(f"Cleaned and merged to {len(cleaned)} packages")
        except Exception as e:
            self.log(f"✗ Error cleaning requirements: {type(e).__name__}: {str(e)}")
            cleaned = list(requirements)
        
        try:
            self.log("Validating packages on PyPI...")
            validated = validate_on_pypi(cleaned, self.log)
            self.log(f"Validation complete: {len(validated)} valid packages")
        except Exception as e:
            self.log(f"✗ Error validating requirements: {type(e).__name__}: {str(e)}")
            validated = cleaned

        self.finished.emit(validated)

    def process_python_file(self, file_path, requirements):
        """Process Python file with individual line error handling."""
        try:
            lines = safe_read_file(file_path, self.log)
            for i, line in enumerate(lines):
                if i >= 50:
                    break
                try:
                    line = line.strip()
                    if line.startswith("import "):
                        parts = line.split()
                        if len(parts) >= 2:
                            pkg = parts[1].split(".")[0].split(",")[0]
                            if pkg and not pkg.startswith("_"):
                                requirements.add(pkg)
                    elif line.startswith("from "):
                        parts = line.split()
                        if len(parts) >= 2:
                            pkg = parts[1].split(".")[0]
                            if pkg and not pkg.startswith("_"):
                                requirements.add(pkg)
                except Exception as e:
                    # Log but continue processing other lines
                    self.log(f"⚠ Error parsing line in {os.path.basename(file_path)}: {line[:50]}")
                    continue
        except Exception as e:
            self.log(f"✗ Error processing Python file {file_path}: {type(e).__name__}")

    def process_requirements_file(self, file_path, requirements):
        """Process requirements file with individual line error handling."""
        try:
            lines = safe_read_file(file_path, self.log)
            for line in lines:
                try:
                    line = line.strip()
                    if line and not line.startswith("#") and not line.startswith("-"):
                        # Handle different requirement formats
                        if "@" in line or "git+" in line or "http" in line:
                            # Skip git/URL requirements for now
                            self.log(f"⚠ Skipping git/URL requirement: {line[:50]}")
                            continue
                        requirements.add(line)
                except Exception as e:
                    # Log but continue processing other lines
                    self.log(f"⚠ Error parsing requirement line: {line[:50]}")
                    continue
        except Exception as e:
            self.log(f"✗ Error processing requirements file {file_path}: {type(e).__name__}")


# -------------------- INSTALL WORKER --------------------

class InstallWorker(QThread):
    progress = Signal(int, int)  # current, total
    finished = Signal(dict)  # results dictionary
    log_msg = Signal(str)
    
    def __init__(self, requirements_source, package_manager='pip', from_memory=False):
        super().__init__()
        self.requirements_source = requirements_source  # Either file path or list
        self.package_manager = package_manager
        self.from_memory = from_memory
    
    def log(self, message):
        self.log_msg.emit(message)
    
    def run(self):
        """Install packages one by one with individual error handling."""
        results = {
            'success': [],
            'failed': [],
            'skipped': []
        }
        
        # Check if in venv
        in_venv = is_venv()
        venv_status = "virtual environment" if in_venv else "global Python"
        self.log(f"Installing to: {venv_status}")
        self.log(f"Python: {sys.executable}")
        self.log(f"Package manager: {self.package_manager}\n")
        
        # Get packages from either file or memory
        if self.from_memory:
            # Requirements already in list format
            packages = self.requirements_source
            self.log(f"Installing from memory")
        else:
            # Read requirements from file
            try:
                with open(self.requirements_source, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except Exception as e:
                self.log(f"✗ Error reading requirements file: {type(e).__name__}: {str(e)}")
                self.finished.emit(results)
                return
            
            # Parse requirements (skip comments and empty lines)
            packages = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    packages.append(line)
            
            self.log(f"Installing from file: {self.requirements_source}")
        
        total = len(packages)
        self.log(f"Found {total} packages to install\n")
        
        if total == 0:
            self.log("⚠ No packages to install")
            self.finished.emit(results)
            return
        
        # Install each package individually
        for idx, package in enumerate(packages, 1):
            self.progress.emit(idx, total)
            pkg_name = package  # Default to full package string
            
            try:
                # Extract package name for logging
                pkg_name = re.split(r'[=<>!~]', package)[0].strip()
                self.log(f"[{idx}/{total}] Installing {pkg_name}...")
                
                # Build install command based on package manager
                if self.package_manager == 'pip' or self.package_manager == 'pip3':
                    cmd = [self.package_manager, 'install', package]
                elif self.package_manager == 'uv':
                    cmd = ['uv', 'pip', 'install', package]
                elif self.package_manager == 'pipx':
                    # pipx installs apps, not libraries - skip
                    self.log(f"  ⚠ Skipping {pkg_name} (pipx is for applications, not libraries)")
                    results['skipped'].append(package)
                    continue
                elif self.package_manager == 'poetry':
                    cmd = ['poetry', 'add', package]
                elif self.package_manager == 'conda':
                    cmd = ['conda', 'install', '-y', package]
                else:
                    cmd = ['pip', 'install', package]
                
                # Run installation command
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=120  # 2 minute timeout per package
                )
                
                if result.returncode == 0:
                    self.log(f"  ✓ Successfully installed {pkg_name}")
                    results['success'].append(package)
                else:
                    error_msg = result.stderr.strip().split('\n')[-1] if result.stderr else 'Unknown error'
                    self.log(f"  ✗ Failed to install {pkg_name}: {error_msg}")
                    results['failed'].append(package)
                
            except subprocess.TimeoutExpired:
                self.log(f"  ✗ Timeout installing {pkg_name} (>2 minutes)")
                results['failed'].append(package)
            except Exception as e:
                self.log(f"  ✗ Error installing {pkg_name}: {type(e).__name__}: {str(e)}")
                results['failed'].append(package)
            
            # Continue to next package regardless of success/failure
        
        self.log(f"\n{'='*60}")
        self.log(f"Installation Summary:")
        self.log(f"  ✓ Success: {len(results['success'])}")
        self.log(f"  ✗ Failed: {len(results['failed'])}")
        self.log(f"  ⚠ Skipped: {len(results['skipped'])}")
        self.log(f"{'='*60}")
        
        self.finished.emit(results)


# -------------------- GUI --------------------

class RequirementsCollector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Master Requirements Generator")
        self.setGeometry(200, 200, 600, 500)

        layout = QVBoxLayout()

        self.select_src_btn = QPushButton("Select Source Directory")
        self.select_src_btn.clicked.connect(self.select_source_dir)
        layout.addWidget(self.select_src_btn)

        self.select_dest_btn = QPushButton("Select Destination for Master Requirements")
        self.select_dest_btn.clicked.connect(self.select_dest_file)
        layout.addWidget(self.select_dest_btn)

        # Package manager selection
        pm_layout = QVBoxLayout()
        pm_label = QLabel("Package Manager:")
        pm_layout.addWidget(pm_label)
        
        self.package_manager_combo = QComboBox()
        self.available_managers = detect_package_managers()
        
        if self.available_managers:
            for name, cmd in self.available_managers.items():
                self.package_manager_combo.addItem(f"{name} ({cmd})", cmd)
            pm_layout.addWidget(self.package_manager_combo)
        else:
            # Fallback if no package managers detected
            self.package_manager_combo.addItem("pip (default)", "pip")
            pm_layout.addWidget(self.package_manager_combo)
            self.log("⚠ No package managers detected, using pip as default")
        
        layout.addLayout(pm_layout)

        self.exclude_std_cb = QCheckBox("Exclude standard libraries")
        self.exclude_std_cb.setChecked(True)
        layout.addWidget(self.exclude_std_cb)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        layout.addWidget(self.log_box)

        self.generate_btn = QPushButton("Generate Master Requirements")
        self.generate_btn.clicked.connect(self.generate_requirements)
        layout.addWidget(self.generate_btn)
        
        self.install_btn = QPushButton("Install Requirements from File")
        self.install_btn.clicked.connect(self.install_requirements)
        layout.addWidget(self.install_btn)
        
        self.progress_label = QLabel("")
        layout.addWidget(self.progress_label)

        self.setLayout(layout)

        self.source_dir = ""
        self.dest_file = ""
        self.generated_requirements = []  # Store generated requirements in memory
        
        # Log detected package managers
        if self.available_managers:
            self.log(f"Detected package managers: {', '.join(self.available_managers.keys())}")

    def select_source_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Source Directory")
        if dir_path:
            self.source_dir = dir_path
            self.log(f"✓ Source directory selected: {dir_path}")

    def select_dest_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Master Requirements", "requirements.txt", "Text Files (*.txt)")
        if file_path:
            self.dest_file = file_path
            self.log(f"✓ Destination file selected: {file_path}")

    def generate_requirements(self):
        if not self.source_dir:
            QMessageBox.warning(self, "Error", "Please select a source directory.")
            return

        selected_pm = self.package_manager_combo.currentData()
        self.log(f"\n{'='*60}")
        self.log(f"Starting requirements generation...")
        self.log(f"Package Manager: {selected_pm}")
        self.log(f"{'='*60}\n")
        
        self.worker = Worker(self.source_dir, self.exclude_std_cb.isChecked(), selected_pm)
        self.worker.log_msg.connect(self.log)
        self.worker.finished.connect(self.write_requirements)
        self.worker.start()
        
        self.generate_btn.setEnabled(False)
        self.generate_btn.setText("Generating...")

    def log(self, message):
        self.log_box.append(message)

    def write_requirements(self, requirements):
        self.generate_btn.setEnabled(True)
        self.generate_btn.setText("Generate Master Requirements")
        
        if not requirements:
            self.log("\n⚠ Warning: No requirements found!")
            QMessageBox.warning(self, "Warning", "No requirements were found.")
            return
        
        # Store requirements in memory
        self.generated_requirements = requirements
        
        self.log(f"\n{'='*60}")
        self.log(f"✓ Requirements generated successfully!")
        self.log(f"Total packages: {len(requirements)}")
        
        # If destination file is selected, save to file
        if self.dest_file:
            try:
                with open(self.dest_file, "w", encoding="utf-8") as f:
                    f.write(f"# Generated by Master Requirements Generator\n")
                    f.write(f"# Package Manager: {self.package_manager_combo.currentData()}\n")
                    f.write(f"# Total packages: {len(requirements)}\n\n")
                    for req in requirements:
                        f.write(req + "\n")
                
                self.log(f"✓ Saved to file: {self.dest_file}")
                self.log(f"{'='*60}")
                
                QMessageBox.information(self, "Success", 
                    f"Master requirements.txt created at:\n{self.dest_file}\n\nTotal packages: {len(requirements)}\n\nRequirements are also stored in memory for installation.")
            except PermissionError:
                error_msg = f"Permission denied writing to: {self.dest_file}"
                self.log(f"✗ ERROR: {error_msg}")
                self.log(f"Requirements are still in memory and can be installed.")
                self.log(f"{'='*60}")
                QMessageBox.warning(self, "Partial Success", 
                    f"{error_msg}\n\nRequirements are stored in memory and can be installed without saving.")
            except Exception as e:
                error_msg = f"Could not write file: {type(e).__name__}: {str(e)}"
                self.log(f"✗ ERROR: {error_msg}")
                self.log(f"Requirements are still in memory and can be installed.")
                self.log(f"{'='*60}")
                QMessageBox.warning(self, "Partial Success", 
                    f"{error_msg}\n\nRequirements are stored in memory and can be installed without saving.")
        else:
            # No destination file, just store in memory
            self.log(f"✓ Requirements stored in memory (not saved to file)")
            self.log(f"You can install them directly or select a destination to save.")
            self.log(f"{'='*60}")
            
            QMessageBox.information(self, "Success", 
                f"Requirements generated successfully!\n\nTotal packages: {len(requirements)}\n\nRequirements are stored in memory.\nYou can install them directly without saving to a file.")
    
    def install_requirements(self):
        """Install requirements from memory or a selected file."""
        # Check if we have generated requirements in memory
        if self.generated_requirements:
            # Ask user if they want to install from memory or file
            reply = QMessageBox.question(
                self,
                "Install Source",
                f"You have {len(self.generated_requirements)} packages in memory.\n\nInstall from memory or select a file?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Yes
            )
            
            if reply == QMessageBox.StandardButton.Cancel:
                return
            elif reply == QMessageBox.StandardButton.Yes:
                # Install from memory
                self._install_from_memory()
                return
            # If No, continue to file selection
        
        # Install from file
        req_file, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Requirements File", 
            "", 
            "Text Files (*.txt);;All Files (*)"
        )
        
        if not req_file:
            return
        
        self._install_from_file(req_file)
    
    def _install_from_memory(self):
        """Install requirements from memory."""
        self.log(f"\nInstalling from memory ({len(self.generated_requirements)} packages)")
        
        # Check if in venv
        in_venv = is_venv()
        venv_msg = "You are running in a virtual environment." if in_venv else "You are running in global Python."
        
        # Confirm installation
        reply = QMessageBox.question(
            self,
            "Confirm Installation",
            f"{venv_msg}\n\nInstall {len(self.generated_requirements)} packages from memory?\n\nUsing: {self.package_manager_combo.currentData()}\n\nThis will install packages one by one. Continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.No:
            return
        
        selected_pm = self.package_manager_combo.currentData()
        self.log(f"\n{'='*60}")
        self.log(f"Starting package installation from memory...")
        self.log(f"{'='*60}\n")
        
        self.install_worker = InstallWorker(self.generated_requirements, selected_pm, from_memory=True)
        self.install_worker.log_msg.connect(self.log)
        self.install_worker.progress.connect(self.update_install_progress)
        self.install_worker.finished.connect(self.install_finished)
        self.install_worker.start()
        
        self.install_btn.setEnabled(False)
        self.install_btn.setText("Installing...")
        self.generate_btn.setEnabled(False)
    
    def _install_from_file(self, req_file):
        """Install requirements from a file."""
        self.log(f"\nSelected requirements file: {req_file}")
        
        # Check if in venv
        in_venv = is_venv()
        venv_msg = "You are running in a virtual environment." if in_venv else "You are running in global Python."
        
        # Confirm installation
        reply = QMessageBox.question(
            self,
            "Confirm Installation",
            f"{venv_msg}\n\nInstall packages from:\n{req_file}\n\nUsing: {self.package_manager_combo.currentData()}\n\nThis will install packages one by one. Continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.No:
            return
        
        selected_pm = self.package_manager_combo.currentData()
        self.log(f"\n{'='*60}")
        self.log(f"Starting package installation from file...")
        self.log(f"{'='*60}\n")
        
        self.install_worker = InstallWorker(req_file, selected_pm, from_memory=False)
        self.install_worker.log_msg.connect(self.log)
        self.install_worker.progress.connect(self.update_install_progress)
        self.install_worker.finished.connect(self.install_finished)
        self.install_worker.start()
        
        self.install_btn.setEnabled(False)
        self.install_btn.setText("Installing...")
        self.generate_btn.setEnabled(False)
    
    def update_install_progress(self, current, total):
        """Update progress label during installation."""
        self.progress_label.setText(f"Installing package {current} of {total}...")
    
    def install_finished(self, results):
        """Handle installation completion."""
        self.install_btn.setEnabled(True)
        self.install_btn.setText("Install Requirements from File")
        self.generate_btn.setEnabled(True)
        self.progress_label.setText("")
        
        success_count = len(results['success'])
        failed_count = len(results['failed'])
        skipped_count = len(results['skipped'])
        total = success_count + failed_count + skipped_count
        
        if failed_count == 0 and skipped_count == 0:
            QMessageBox.information(
                self,
                "Installation Complete",
                f"Successfully installed all {success_count} packages!"
            )
        elif success_count > 0:
            msg = f"Installation completed with some issues:\n\n"
            msg += f"✓ Success: {success_count}\n"
            if failed_count > 0:
                msg += f"✗ Failed: {failed_count}\n"
            if skipped_count > 0:
                msg += f"⚠ Skipped: {skipped_count}\n"
            msg += f"\nCheck the log for details."
            QMessageBox.warning(self, "Partial Success", msg)
        else:
            QMessageBox.critical(
                self,
                "Installation Failed",
                f"Failed to install packages. Check the log for details.\n\n"
                f"Failed: {failed_count}, Skipped: {skipped_count}"
            )


# -------------------- MAIN --------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RequirementsCollector()
    window.show()
    sys.exit(app.exec())
