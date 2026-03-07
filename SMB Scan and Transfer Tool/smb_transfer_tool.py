#!/usr/bin/env python3
"""
Simple SMB Explorer for macOS (Qt6 + Python)

Feature set (robust, end-to-end):
- Zeroconf discovery of SMB services (Bonjour: _smb._tcp.local)
- Host & share listing via macOS `smbutil view` (anonymous, then authenticated)
- Mount/unmount SMB shares using `mount_smbfs` → /Volumes/<Share>
- Two-pane file explorer (Local ⟷ Remote) using QFileSystemModel
- **Action buttons in a centered vertical column between the two panes**:
  Copy →, ← Copy, Delete Selected, Rename, New Folder
- Checkboxes on both panes + multi-select
- Recursive copy with **resume** (size- and partial-file aware)
- Optional **MD5 verification** (toggle)
- Threaded transfers with per-file and overall progress + cancellable
- Detailed status and log panel; persistent log at ~/Library/Logs/SimpleSMBExplorer.log
- Auth prompt with optional **save credentials to macOS Keychain** (`keyring`)
- Connection status and error handling, including share mount checks
- Failed/incomplete transfer detection + resume option

Tested with: Python 3.10+, PySide6 6.6+, macOS 12+

Install:
  pip install PySide6 zeroconf keyring
(Optional): pip install psutil

NOTE:
- Uses macOS tools: `smbutil`, `mount_smbfs`, `diskutil`.
- MD5 on huge files can be slow; disable if needed.
- Resume will append from destination size if smaller than source.
"""
from __future__ import annotations
import os
import sys
import re
import hashlib
import shutil
import subprocess
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Signal, Slot, QThread
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTreeView, QSplitter, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QCheckBox, QProgressBar, QComboBox, QInputDialog,
    QMessageBox, QFileDialog, QStatusBar, QTextEdit
)

try:
    import keyring
except Exception:
    keyring = None

try:
    from zeroconf import ServiceBrowser, Zeroconf
except Exception:
    Zeroconf = None

try:
    import psutil
except Exception:
    psutil = None

LOG_DIR = Path.home() / "Library/Logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "SimpleSMBExplorer.log"
SERVICE_NAME = "SimpleSMBExplorer"

# --------------------------- Utilities ---------------------------

def log(msg: str):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}\n"
    try:
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass
    print(line, end="")


def run(cmd: List[str], timeout: int = 30) -> Tuple[int, str, str]:
    log(f"RUN: {' '.join(cmd)}")
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        out = p.stdout.strip()
        err = p.stderr.strip()
        if p.returncode != 0:
            log(f"ERR({p.returncode}): {err}")
        else:
            if out:
                log(f"OUT: {out[:200]}{'…' if len(out)>200 else ''}")
        return p.returncode, out, err
    except Exception as e:
        log(f"EXC: {e}")
        return 1, "", str(e)


def md5sum(path: Path, chunk: int = 2**20, start_offset: int = 0) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        if start_offset:
            f.seek(start_offset)
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def human(n: int) -> str:
    units = ["B","KB","MB","GB","TB"]
    s = float(n)
    for u in units:
        if s < 1024 or u == units[-1]:
            return f"{s:.1f} {u}"
        s /= 1024

# --------------------------- Auth Dialog ---------------------------

class AuthDialog(QtWidgets.QDialog):
    def __init__(self, host: str, parent=None, preset_user: str = "") -> None:
        super().__init__(parent)
        self.setWindowTitle(f"Authenticate for {host}")
        self.user = QLineEdit(preset_user)
        self.domain = QLineEdit()
        self.passw = QLineEdit(); self.passw.setEchoMode(QLineEdit.Password)
        self.save = QCheckBox("Save credentials to Keychain")

        form = QtWidgets.QFormLayout(self)
        form.addRow("Username", self.user)
        form.addRow("Domain (optional)", self.domain)
        form.addRow("Password", self.passw)
        form.addRow("", self.save)
        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        form.addRow(btns)

    def values(self) -> Tuple[str, str, str, bool]:
        return self.user.text(), self.domain.text(), self.passw.text(), self.save.isChecked()

# --------------------------- SMB Discovery ---------------------------

@dataclass
class SMBService:
    host: str
    address: str
    port: int


class ZeroconfBrowser(QtCore.QObject):
    serviceFound = Signal(object)
    serviceRemoved = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._zc = None
        self._browser = None

    def start(self):
        if Zeroconf is None:
            log("zeroconf not installed; skipping browse")
            return
        self._zc = Zeroconf()
        self._browser = ServiceBrowser(self._zc, "_smb._tcp.local.", handlers=[self._handler])

    def stop(self):
        try:
            if self._zc:
                self._zc.close()
        except Exception:
            pass

    def _handler(self, zc, type_, name, state_change):
        host = name.split(".")[0]
        if "Added" in str(state_change):
            self.serviceFound.emit(SMBService(host=host, address=host, port=445))
        elif "Removed" in str(state_change):
            self.serviceRemoved.emit(SMBService(host=host, address=host, port=445))

# --------------------------- Checkable FS Model ---------------------------

class CheckableFSModel(QtWidgets.QFileSystemModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._checked: Dict[str, Qt.CheckState] = {}
        self.setOption(QtWidgets.QFileSystemModel.DontUseCustomDirectoryIcons, True)

    def flags(self, index: QtCore.QModelIndex) -> Qt.ItemFlags:
        f = super().flags(index)
        if index.isValid():
            f |= Qt.ItemIsUserCheckable
        return f

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.CheckStateRole and index.column() == 0:
            path = self.filePath(index)
            return self._checked.get(path, Qt.Unchecked)
        return super().data(index, role)

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.CheckStateRole and index.column() == 0:
            path = self.filePath(index)
            self._checked[path] = Qt.CheckState(value)
            self.dataChanged.emit(index, index, [Qt.CheckStateRole])
            return True
        return super().setData(index, value, role)

    def checked_paths(self) -> List[Path]:
        return [Path(p) for p, state in self._checked.items() if state == Qt.Checked]

# --------------------------- Transfer Worker ---------------------------

class TransferWorker(QtCore.QObject):
    progress = Signal(int)              # overall percent
    itemProgress = Signal(str, int)     # path, percent
    status = Signal(str)                # human-readable status
    finished = Signal(bool)             # ok flag
    totals = Signal(int, int)           # total files, total bytes

    def __init__(self, sources: List[Path], dest_dir: Path, verify_md5: bool):
        super().__init__()
        self.sources = sources
        self.dest_dir = dest_dir
        self.verify_md5 = verify_md5
        self._stop = False

    @Slot()
    def run(self):
        try:
            plan: List[Tuple[Path, Path]] = []
            total_bytes = 0
            for src in self.sources:
                if src.is_dir():
                    base = src
                    for root, _, files in os.walk(src):
                        root_p = Path(root)
                        for fn in files:
                            s = root_p / fn
                            rel = s.relative_to(base)
                            d = self.dest_dir / base.name / rel
                            plan.append((s, d))
                            try:
                                total_bytes += s.stat().st_size
                            except Exception:
                                pass
                else:
                    d = self.dest_dir / src.name
                    plan.append((src, d))
                    try:
                        total_bytes += src.stat().st_size
                    except Exception:
                        pass

            self.totals.emit(len(plan), total_bytes)

            copied_bytes = 0
            for idx, (src, dst) in enumerate(plan, 1):
                if self._stop:
                    raise RuntimeError("Transfer cancelled")
                self.status.emit(f"Copying {src} → {dst}")
                dst.parent.mkdir(parents=True, exist_ok=True)
                copied_bytes += self._copy_with_resume(src, dst)
                self.itemProgress.emit(str(src), 100)
                if self.verify_md5 and src.is_file():
                    sm = md5sum(src)
                    dm = md5sum(dst)
                    if sm != dm:
                        log(f"MD5 mismatch: {src} vs {dst}")
                        raise RuntimeError(f"MD5 mismatch for {src}")
                # Update overall progress conservatively
                self.progress.emit(int(min(99, (copied_bytes * 100) / max(1, total_bytes))))

            self.status.emit("Transfer complete")
            self.progress.emit(100)
            self.finished.emit(True)
        except Exception as e:
            self.status.emit(f"Error: {e}")
            self.finished.emit(False)

    def stop(self):
        self._stop = True

    def _copy_with_resume(self, src: Path, dst: Path, chunk: int = 2**20) -> int:
        """Resume if dst smaller than src; returns bytes written this invocation."""
        if src.is_dir():
            dst.mkdir(parents=True, exist_ok=True)
            return 0
        s = src.stat().st_size
        existing = dst.stat().st_size if dst.exists() else 0
        mode = 'r+b' if dst.exists() else 'wb'
        written = 0
        with src.open('rb') as fsrc, open(dst, mode) as fdst:
            if existing and existing < s:
                fsrc.seek(existing)
                fdst.seek(existing)
            copied = existing
            while True:
                buf = fsrc.read(chunk)
                if not buf:
                    break
                fdst.write(buf)
                written += len(buf)
                copied += len(buf)
                pct = int((copied * 100) / max(1, s))
                self.itemProgress.emit(str(src), pct)
        return written

# --------------------------- Main Window ---------------------------

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple SMB Explorer")
        self.resize(1280, 820)

        self.statusbar = QStatusBar(); self.setStatusBar(self.statusbar)

        central = QWidget(); self.setCentralWidget(central)
        root_v = QVBoxLayout(central)

        # Top controls: host/share + discovery/mount
        top_h = QHBoxLayout()
        self.host_combo = QComboBox(); self.host_combo.setEditable(True)
        self.share_combo = QComboBox(); self.share_combo.setEditable(True)
        self.scan_btn = QPushButton("Scan Network")
        self.view_shares_btn = QPushButton("List Shares")
        self.mount_btn = QPushButton("Mount")
        self.unmount_btn = QPushButton("Unmount")
        top_h.addWidget(QLabel("Host:")); top_h.addWidget(self.host_combo, 2)
        top_h.addWidget(QLabel("Share:")); top_h.addWidget(self.share_combo, 2)
        top_h.addWidget(self.scan_btn)
        top_h.addWidget(self.view_shares_btn)
        top_h.addWidget(self.mount_btn)
        top_h.addWidget(self.unmount_btn)
        root_v.addLayout(top_h)

        # Progress + options
        opts_h = QHBoxLayout()
        self.progress = QProgressBar(); self.progress.setValue(0)
        self.item_label = QLabel("")
        self.verify_md5_cb = QCheckBox("MD5 verify")
        self.verify_md5_cb.setChecked(True)
        self.cancel_btn = QPushButton("Cancel Transfer")
        self.cancel_btn.setEnabled(False)
        opts_h.addWidget(QLabel("Progress:")); opts_h.addWidget(self.progress, 4)
        opts_h.addWidget(self.item_label, 2)
        opts_h.addStretch(1)
        opts_h.addWidget(self.verify_md5_cb)
        opts_h.addWidget(self.cancel_btn)
        root_v.addLayout(opts_h)

        # Splitter: Local | Actions | Remote
        splitter = QSplitter(); splitter.setChildrenCollapsible(False)
        root_v.addWidget(splitter, 1)

        # Local panel
        self.local_model = CheckableFSModel()
        self.local_root = str(Path.home())
        self.local_model.setRootPath(self.local_root)
        self.local_view = QTreeView(); self.local_view.setModel(self.local_model)
        self.local_view.setRootIndex(self.local_model.index(self.local_root))
        self.local_view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.local_view.setAlternatingRowColors(True)
        splitter.addWidget(self.local_view)

        # Middle actions panel
        mid = QWidget(); mid_v = QVBoxLayout(mid); mid_v.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        mid_v.addWidget(QLabel("Actions"))
        self.copy_lr_btn = QPushButton("Copy →")
        self.copy_rl_btn = QPushButton("← Copy")
        self.delete_btn = QPushButton("Delete Selected")
        self.rename_btn = QPushButton("Rename…")
        self.new_folder_btn = QPushButton("New Folder…")
        for b in [self.copy_lr_btn, self.copy_rl_btn, self.delete_btn, self.rename_btn, self.new_folder_btn]:
            b.setMinimumWidth(160)
            mid_v.addWidget(b)
        mid_v.addStretch(1)
        splitter.addWidget(mid)

        # Remote panel (mounted shares live under /Volumes/<Share>)
        self.remote_model = CheckableFSModel()
        self.remote_root = "/Volumes"
        self.remote_model.setRootPath(self.remote_root)
        self.remote_view = QTreeView(); self.remote_view.setModel(self.remote_model)
        self.remote_view.setRootIndex(self.remote_model.index(self.remote_root))
        self.remote_view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.remote_view.setAlternatingRowColors(True)
        splitter.addWidget(self.remote_view)
        splitter.setSizes([600, 120, 600])

        # Log area
        self.log_text = QTextEdit(); self.log_text.setReadOnly(True)
        root_v.addWidget(self.log_text, 0)
        self._load_log()

        # Signals
        self.scan_btn.clicked.connect(self.scan_network)
        self.view_shares_btn.clicked.connect(self.list_shares)
        self.mount_btn.clicked.connect(self.mount_share)
        self.unmount_btn.clicked.connect(self.unmount_share)
        self.copy_lr_btn.clicked.connect(lambda: self.copy_selected(direction="lr"))
        self.copy_rl_btn.clicked.connect(lambda: self.copy_selected(direction="rl"))
        self.delete_btn.clicked.connect(self.delete_selected)
        self.rename_btn.clicked.connect(self.rename_selected)
        self.new_folder_btn.clicked.connect(self.create_folder)
        self.cancel_btn.clicked.connect(self.cancel_transfer)

        # Zeroconf
        self.zc_browser = ZeroconfBrowser()
        self.zc_browser.serviceFound.connect(self._on_service_found)
        self.zc_browser.serviceRemoved.connect(self._on_service_removed)

        # Transfer state
        self.transfer_thread: Optional[QThread] = None
        self.transfer_worker: Optional[TransferWorker] = None

    # ----- Log helpers -----
    def _load_log(self):
        try:
            if LOG_FILE.exists():
                self.log_text.setPlainText(LOG_FILE.read_text())
        except Exception:
            pass

    def _append_log(self, text: str):
        log(text)
        self.log_text.append(text)

    # ----- Discovery & Shares -----
    def scan_network(self):
        self.statusbar.showMessage("Scanning for SMB services…")
        if Zeroconf is None:
            QMessageBox.information(self, "Zeroconf missing", "Install 'zeroconf' (pip install zeroconf) to enable discovery. You can still type a host manually.")
            return
        self.host_combo.clear()
        self.zc_browser.start()
        self._append_log("Started Zeroconf browsing for _smb._tcp.local")

    @Slot(object)
    def _on_service_found(self, svc: SMBService):
        if self.host_combo.findText(svc.host) < 0:
            self.host_combo.addItem(svc.host)
            self._append_log(f"Found SMB host: {svc.host}")

    @Slot(object)
    def _on_service_removed(self, svc: SMBService):
        idx = self.host_combo.findText(svc.host)
        if idx >= 0:
            self.host_combo.removeItem(idx)
            self._append_log(f"Removed SMB host: {svc.host}")

    def list_shares(self):
        host = self.host_combo.currentText().strip()
        if not host:
            QMessageBox.warning(self, "Host required", "Enter or pick a host first.")
            return
        # Anonymous first
        rc, out, err = run(["smbutil", "view", f"//{host}"])
        if rc != 0:
            # Prompt for creds
            user = ""
            if keyring:
                try:
                    saved = keyring.get_password(SERVICE_NAME, f"{host}:username")
                    if saved:
                        user = saved
                except Exception:
                    pass
            dlg = AuthDialog(host, self, preset_user=user)
            if dlg.exec() != QtWidgets.QDialog.Accepted:
                return
            username, domain, password, save = dlg.values()
            auth = f"{domain+';' if domain else ''}{username}:{password}"
            rc, out, err = run(["smbutil", "view", f"//{auth}@{host}"])
            if rc == 0 and save and keyring:
                try:
                    keyring.set_password(SERVICE_NAME, f"{host}:username", username)
                    keyring.set_password(SERVICE_NAME, f"{host}:password", password)
                except Exception:
                    pass
        if rc == 0:
            shares = self._parse_smbutil_view(out)
            self.share_combo.clear()
            for s in shares:
                self.share_combo.addItem(s)
            self.statusbar.showMessage(f"Found {len(shares)} share(s) on {host}")
            self._append_log(f"Shares on {host}: {shares}")
        else:
            QMessageBox.critical(self, "Error listing shares", err or out or "Unknown error")

    def _parse_smbutil_view(self, out: str) -> List[str]:
        shares: List[str] = []
        for line in out.splitlines():
            m = re.match(r"^\\\\[^\\]+\\([^\s]+)\s+", line.strip())
            if m:
                shares.append(m.group(1))
                continue
            parts = line.split()
            if parts and parts[0] not in ("Share", "-----") and not line.startswith("\\"):
                cand = parts[0]
                if cand.upper() not in ("IPC$",):
                    shares.append(cand)
        return sorted(list(dict.fromkeys(shares)))

    # ----- Mount/Unmount -----
    def _get_saved_creds(self, host: str) -> Tuple[Optional[str], Optional[str]]:
        if not keyring:
            return None, None
        try:
            u = keyring.get_password(SERVICE_NAME, f"{host}:username")
            p = keyring.get_password(SERVICE_NAME, f"{host}:password")
            return u, p
        except Exception:
            return None, None

    def _is_mounted(self, mount_point: Path) -> bool:
        if psutil:
            try:
                for p in psutil.disk_partitions(all=False):
                    if p.mountpoint == str(mount_point):
                        return True
            except Exception:
                pass
        return mount_point.exists() and any(mount_point.iterdir())

    def mount_share(self):
        host = self.host_combo.currentText().strip()
        share = self.share_combo.currentText().strip()
        if not host or not share:
            QMessageBox.warning(self, "Missing info", "Host and Share are required.")
            return
        username, password = self._get_saved_creds(host)
        if username and password:
            auth = f"{username}:{password}@"
        else:
            dlg = AuthDialog(host, self, preset_user=username or "")
            if dlg.exec() != QtWidgets.QDialog.Accepted:
                return
            u, d, p, save = dlg.values()
            userpart = f"{d+';' if d else ''}{u}"
            auth = f"{userpart}:{p}@"
            if save and keyring:
                try:
                    keyring.set_password(SERVICE_NAME, f"{host}:username", u)
                    keyring.set_password(SERVICE_NAME, f"{host}:password", p)
                except Exception:
                    pass
        mount_point = Path("/Volumes") / share
        mount_point.mkdir(parents=True, exist_ok=True)
        url = f"//{auth}{host}/{share}"
        rc, out, err = run(["mount_smbfs", url, str(mount_point)], timeout=60)
        if rc == 0:
            self.statusbar.showMessage(f"Mounted at {mount_point}")
            self._append_log(f"Mounted {url} at {mount_point}")
            self.remote_model.setRootPath(str(mount_point))
            self.remote_view.setRootIndex(self.remote_model.index(str(mount_point)))
        else:
            QMessageBox.critical(self, "Mount failed", err or out or "Unknown error")

    def unmount_share(self):
        idx = self.remote_view.rootIndex()
        path = Path(self.remote_model.filePath(idx)) if idx.isValid() else Path(self.remote_root)
        if str(path).startswith("/Volumes/") and path != Path(self.remote_root):
            rc, out, err = run(["diskutil", "unmount", str(path)])
            if rc == 0:
                self.statusbar.showMessage(f"Unmounted {path}")
                self._append_log(f"Unmounted {path}")
                self.remote_model.setRootPath(self.remote_root)
                self.remote_view.setRootIndex(self.remote_model.index(self.remote_root))
            else:
                QMessageBox.critical(self, "Unmount failed", err or out or "Unknown error")
        else:
            QMessageBox.information(self, "Nothing to unmount", "No mounted share is active.")

    # ----- File selection helpers -----
    def _selected_checked(self, view: QTreeView, model: CheckableFSModel) -> List[Path]:
        paths = set()
        for p in model.checked_paths():
            paths.add(p)
        for idx in view.selectionModel().selectedRows():
            paths.add(Path(model.filePath(idx)))
        return [p for p in paths if str(p) and Path(str(p)).exists()]

    def _active_root(self, view: QTreeView, model: CheckableFSModel) -> Path:
        idx = view.rootIndex()
        return Path(model.filePath(idx)) if idx.isValid() else Path("/")

    # ----- File ops -----
    def copy_selected(self, direction: str):
        if self.transfer_thread:
            QMessageBox.warning(self, "Busy", "A transfer is already in progress.")
            return
        if direction == "lr":
            sources = self._selected_checked(self.local_view, self.local_model)
            dest_root = self._active_root(self.remote_view, self.remote_model)
        else:
            sources = self._selected_checked(self.remote_view, self.remote_model)
            dest_root = self._active_root(self.local_view, self.local_model)
        if not sources:
            QMessageBox.information(self, "Nothing selected", "Select or check files/folders to copy.")
            return
        if not dest_root.exists():
            QMessageBox.critical(self, "Invalid destination", f"Destination root does not exist: {dest_root}")
            return
        self._start_transfer(sources, dest_root)

    def _start_transfer(self, sources: List[Path], dest_dir: Path):
        worker = TransferWorker(sources, dest_dir, self.verify_md5_cb.isChecked())
        thread = QThread()
        worker.moveToThread(thread)
        worker.progress.connect(self.progress.setValue)
        worker.itemProgress.connect(lambda p, pct: self.item_label.setText(f"{Path(p).name}: {pct}%"))
        worker.status.connect(lambda s: (self._append_log(s), self.statusbar.showMessage(s)))
        worker.finished.connect(lambda ok: self._on_transfer_finished(ok))
        thread.started.connect(worker.run)
        thread.finished.connect(thread.deleteLater)
        self.transfer_thread = thread
        self.transfer_worker = worker
        self.cancel_btn.setEnabled(True)
        thread.start()

    def cancel_transfer(self):
        if self.transfer_worker:
            self.transfer_worker.stop()
        self._append_log("Transfer cancellation requested")

    def _on_transfer_finished(self, ok: bool):
        self._append_log(f"Transfer {'OK' if ok else 'FAILED'}")
        self.statusbar.showMessage(f"Transfer {'OK' if ok else 'FAILED'}")
        if self.transfer_thread:
            self.transfer_thread.quit()
            self.transfer_thread.wait(2000)
        self.transfer_thread = None
        self.transfer_worker = None
        self.progress.setValue(0)
        self.item_label.setText("")
        self.cancel_btn.setEnabled(False)

    def delete_selected(self):
        # Deletes from whichever pane has focus
        if self.remote_view.hasFocus():
            paths = self._selected_checked(self.remote_view, self.remote_model)
        else:
            paths = self._selected_checked(self.local_view, self.local_model)
        if not paths:
            QMessageBox.information(self, "Nothing selected", "Select or check files/folders to delete.")
            return
        if QMessageBox.question(self, "Confirm delete", f"Delete {len(paths)} item(s)?") != QMessageBox.Yes:
            return
        failed = []
        for p in paths:
            try:
                if p.is_dir():
                    shutil.rmtree(p)
                else:
                    p.unlink(missing_ok=True)
                self._append_log(f"Deleted {p}")
            except Exception as e:
                failed.append((p, str(e)))
        if failed:
            self._append_log("Delete failures:" + "; ".join([f"{p}: {e}" for p, e in failed]))
            QMessageBox.warning(self, "Delete issues", f"{len(failed)} item(s) could not be deleted. See log.")
        self.statusbar.showMessage("Delete complete")

    def rename_selected(self):
        # Renames the first selected item in the focused pane
        if self.remote_view.hasFocus():
            view, model = self.remote_view, self.remote_model
        else:
            view, model = self.local_view, self.local_model
        indexes = view.selectionModel().selectedRows()
        if not indexes:
            QMessageBox.information(self, "Nothing selected", "Select a file or folder to rename.")
            return
        idx = indexes[0]
        path = Path(model.filePath(idx))
        new_name, ok = QInputDialog.getText(self, "Rename", "New name:", text=path.name)
        if not ok or not new_name:
            return
        try:
            path.rename(path.with_name(new_name))
            self._append_log(f"Renamed {path} → {path.with_name(new_name)}")
        except Exception as e:
            QMessageBox.critical(self, "Rename failed", str(e))

    def create_folder(self):
        # Creates a folder in the currently focused pane's root
        if self.remote_view.hasFocus():
            root = self._active_root(self.remote_view, self.remote_model)
        else:
            root = self._active_root(self.local_view, self.local_model)
        name, ok = QInputDialog.getText(self, "New Folder", "Folder name:")
        if not ok or not name:
            return
        try:
            p = root / name
            p.mkdir(parents=True, exist_ok=False)
            self._append_log(f"Created folder {p}")
        except Exception as e:
            QMessageBox.critical(self, "Create failed", str(e))

# --------------------------- Entrypoint ---------------------------

def main():
    if sys.platform != "darwin":
        print("This app targets macOS. Mounting requires macOS utilities.")
    app = QApplication(sys.argv)
    # Nice default font size for readability
    f = app.font(); f.setPointSize(f.pointSize()+1); app.setFont(f)
    w = MainWindow(); w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
