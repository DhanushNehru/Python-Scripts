#!/usr/bin/env python3
import os
import sys
import shutil
import plistlib
import subprocess
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Iterable

from PySide6 import QtCore, QtGui, QtWidgets

APP_DIRS = [Path("/Applications"), Path.home() / "Applications"]

# Where we look (user-space). Each tuple is (label, path).
USER_LIBRARY_BUCKETS: List[Tuple[str, Path]] = [
    ("Application Support", Path("~/Library/Application Support").expanduser()),
    ("Preferences", Path("~/Library/Preferences").expanduser()),
    ("Caches", Path("~/Library/Caches").expanduser()),
    ("Containers", Path("~/Library/Containers").expanduser()),
    ("Group Containers", Path("~/Library/Group Containers").expanduser()),
    ("Saved Application State", Path("~/Library/Saved Application State").expanduser()),
    ("Logs", Path("~/Library/Logs").expanduser()),
    ("WebKit", Path("~/Library/WebKit").expanduser()),
    ("Cookies", Path("~/Library/Cookies").expanduser()),
    ("LaunchAgents", Path("~/Library/LaunchAgents").expanduser()),
]

SPOTLIGHT_TIMEOUT_SEC = 20


@dataclass
class AppInfo:
    name: str
    path: Path
    bundle_id: Optional[str] = None


@dataclass
class ScanResult:
    app: AppInfo
    files_by_bucket: Dict[str, List[Path]] = field(default_factory=dict)
    extra_hits: List[Path] = field(default_factory=list)  # From Spotlight that don't fall into a known bucket


def is_app_bundle(p: Path) -> bool:
    return p.suffix.lower() == ".app" and p.is_dir()


def find_installed_apps() -> List[AppInfo]:
    apps: List[AppInfo] = []
    seen = set()
    for base in APP_DIRS:
        if not base.exists():
            continue
        for entry in sorted(base.iterdir(), key=lambda x: x.name.lower()):
            if is_app_bundle(entry):
                real = entry.resolve()
                if real in seen:
                    continue
                seen.add(real)
                name = entry.name[:-4]  # strip .app
                apps.append(AppInfo(name=name, path=real))
    return apps


def read_bundle_id(app_path: Path) -> Optional[str]:
    info = app_path / "Contents" / "Info.plist"
    if not info.exists():
        return None
    try:
        with info.open("rb") as f:
            plist = plistlib.load(f)
        bid = plist.get("CFBundleIdentifier") or plist.get("CFBundleIdentifier~ipad")
        if isinstance(bid, str):
            return bid
    except Exception:
        pass
    return None


def run_mdfind(query: str) -> List[Path]:
    """Run mdfind; return Paths (unique, existing)."""
    try:
        proc = subprocess.run(
            ["mdfind", query],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=SPOTLIGHT_TIMEOUT_SEC,
        )
        hits: List[Path] = []
        if proc.returncode == 0 and proc.stdout:
            for line in proc.stdout.splitlines():
                p = Path(line.strip())
                if p.exists():
                    hits.append(p)
        # dedupe while preserving order
        seen = set()
        uniq = []
        for p in hits:
            if p not in seen:
                seen.add(p)
                uniq.append(p)
        return uniq
    except Exception:
        return []


def glob_matches(root: Path, terms: Iterable[str]) -> List[Path]:
    """Shallow-and-deep match under root for any of the terms in file/folder names."""
    if not root.exists():
        return []
    results: List[Path] = []
    lowered = [t.lower() for t in terms if t]
    try:
        for dirpath, dirnames, filenames in os.walk(root):
            # avoid traversing giant trees too long
            for name in dirnames + filenames:
                lname = name.lower()
                if any(t in lname for t in lowered):
                    results.append(Path(dirpath) / name)
    except Exception:
        pass
    return results


def group_into_buckets(paths: List[Path]) -> Tuple[Dict[str, List[Path]], List[Path]]:
    """Group paths by our known buckets; paths that don't fit go into extra_hits."""
    buckets: Dict[str, List[Path]] = {label: [] for (label, _) in USER_LIBRARY_BUCKETS}
    extras: List[Path] = []
    for p in paths:
        matched = False
        for label, root in USER_LIBRARY_BUCKETS:
            try:
                # If p is under root
                p.resolve().relative_to(root.resolve())
                buckets[label].append(p)
                matched = True
                break
            except Exception:
                continue
        if not matched:
            extras.append(p)
    # prune empties
    buckets = {k: v for k, v in buckets.items() if v}
    return buckets, extras


def scan_app(app: AppInfo) -> ScanResult:
    """
    Strategy:
      1) Prefer bundle id; Spotlight for kMDItemCFBundleIdentifier exact match.
      2) Also query Spotlight for name contains and bundle id substring.
      3) Targeted glob in user Library buckets for both bundle id and friendly app name.
    """
    terms = {app.name}
    if app.bundle_id:
        terms.add(app.bundle_id)

    spotlight_hits: List[Path] = []

    # Exact bundle id query (most precise)
    if app.bundle_id:
        spotlight_hits += run_mdfind(f'kMDItemCFBundleIdentifier == "{app.bundle_id}"')

    # Name contains (fallbacks)
    # Use quotes around name with spaces to keep phrase
    safe_name = app.name.replace('"', '\\"')
    spotlight_hits += run_mdfind(f'kMDItemDisplayName == "{safe_name}"cdw || kMDItemFSName == "{safe_name}.app"cdw')

    # Loose contains for bundle id bits (sometimes support files have bundle id in path or metadata)
    if app.bundle_id:
        safe_bid = app.bundle_id.replace('"', '\\"')
        spotlight_hits += run_mdfind(f'kMDItemTextContent == "{safe_bid}"cdw || kMDItemFSName == "{safe_bid}"cdw')

    # Targeted filesystem sweeps within user Library
    lib_hits: List[Path] = []
    # Preferences often use domain style: com.vendor.App.plist
    preference_candidates = []
    if app.bundle_id:
        preference_candidates.append(app.bundle_id)
    preference_candidates.append(app.name)
    # Sweep buckets
    for _, root in USER_LIBRARY_BUCKETS:
        lib_hits += glob_matches(root, preference_candidates)

    all_hits = []
    seen = set()
    for p in spotlight_hits + lib_hits:
        if p not in seen and p.exists():
            seen.add(p)
            all_hits.append(p)

    files_by_bucket, extra_hits = group_into_buckets(all_hits)
    return ScanResult(app=app, files_by_bucket=files_by_bucket, extra_hits=extra_hits)


# --------------------------- Qt Helpers ---------------------------

class WorkerSignals(QtCore.QObject):
    app_started = QtCore.Signal(str)
    app_progress = QtCore.Signal(int, int)  # current, total
    app_finished = QtCore.Signal(object)    # ScanResult
    all_done = QtCore.Signal()


class ScanWorker(QtCore.QRunnable):
    def __init__(self, apps: List[AppInfo]):
        super().__init__()
        self.apps = apps
        self.signals = WorkerSignals()

    @QtCore.Slot()
    def run(self):
        total = len(self.apps)
        for idx, app in enumerate(self.apps, start=1):
            self.signals.app_started.emit(app.name)
            # hydrate bundle id
            bid = read_bundle_id(app.path)
            app.bundle_id = bid
            result = scan_app(app)
            self.signals.app_progress.emit(idx, total)
            self.signals.app_finished.emit(result)
        self.signals.all_done.emit()


class CheckableTree(QtWidgets.QTreeWidget):
    """
    QTreeWidget with tri-state checkbox support and recursive propagation.
    Column 0 holds the checkboxes.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderLabels(["Path / Group", "Kind"])
        self.setUniformRowHeights(True)
        self.setExpandsOnDoubleClick(True)
        self.itemChanged.connect(self.on_item_changed)

    def on_item_changed(self, item: QtWidgets.QTreeWidgetItem, column: int):
        if column != 0:
            return
        state = item.checkState(0)
        # propagate down
        for i in range(item.childCount()):
            child = item.child(i)
            child.setCheckState(0, state)
        # propagate up
        self._update_parent_state(item)

    def _update_parent_state(self, item: QtWidgets.QTreeWidgetItem):
        parent = item.parent()
        if not parent:
            return
        checked = 0
        partial = False
        for i in range(parent.childCount()):
            cs = parent.child(i).checkState(0)
            if cs == QtCore.Qt.CheckState.PartiallyChecked:
                partial = True
            elif cs == QtCore.Qt.CheckState.Checked:
                checked += 1
        if partial or (0 < checked < parent.childCount()):
            parent.setCheckState(0, QtCore.Qt.CheckState.PartiallyChecked)
        elif checked == 0:
            parent.setCheckState(0, QtCore.Qt.CheckState.Unchecked)
        else:
            parent.setCheckState(0, QtCore.Qt.CheckState.Checked)
        self._update_parent_state(parent)


# --------------------------- Main Window ---------------------------

class AppCleaner(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("macOS App Cleaner (PySide6)")
        self.resize(1100, 700)

        # Central layout
        splitter = QtWidgets.QSplitter()
        splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)

        # Left: app list with checkboxes
        left = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout(left)
        left_layout.setContentsMargins(8, 8, 8, 8)
        self.search_bar = QtWidgets.QLineEdit()
        self.search_bar.setPlaceholderText("Filter apps…")
        self.search_bar.textChanged.connect(self.filter_apps)
        left_layout.addWidget(self.search_bar)

        self.app_list = QtWidgets.QListWidget()
        self.app_list.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        left_layout.addWidget(self.app_list, 1)

        # App toolbar
        app_toolbar = QtWidgets.QHBoxLayout()
        self.btn_select_all = QtWidgets.QPushButton("Select All")
        self.btn_select_none = QtWidgets.QPushButton("Deselect All")
        self.btn_refresh = QtWidgets.QPushButton("Rescan Apps")
        app_toolbar.addWidget(self.btn_select_all)
        app_toolbar.addWidget(self.btn_select_none)
        app_toolbar.addStretch(1)
        app_toolbar.addWidget(self.btn_refresh)
        left_layout.addLayout(app_toolbar)

        splitter.addWidget(left)

        # Right: tree of results + controls
        right = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout(right)
        right_layout.setContentsMargins(8, 8, 8, 8)

        self.tree = CheckableTree()
        right_layout.addWidget(self.tree, 1)

        # Controls
        controls = QtWidgets.QHBoxLayout()
        self.btn_scan = QtWidgets.QPushButton("Scan Selected Apps")
        self.btn_delete = QtWidgets.QPushButton("Delete Checked Items")
        self.btn_delete.setEnabled(False)
        self.progress = QtWidgets.QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.status_label = QtWidgets.QLabel("Ready.")
        controls.addWidget(self.btn_scan)
        controls.addWidget(self.btn_delete)
        controls.addStretch(1)
        controls.addWidget(self.progress, 2)
        controls.addWidget(self.status_label, 2)
        right_layout.addLayout(controls)

        splitter.addWidget(right)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        self.setCentralWidget(splitter)

        # Menu (optional niceties)
        self._make_menu()

        # State
        self.thread_pool = QtCore.QThreadPool()
        self.all_apps: List[AppInfo] = []

        # Signals
        self.btn_select_all.clicked.connect(self.select_all_apps)
        self.btn_select_none.clicked.connect(self.deselect_all_apps)
        self.btn_refresh.clicked.connect(self.load_apps)
        self.btn_scan.clicked.connect(self.scan_selected)
        self.btn_delete.clicked.connect(self.delete_checked)

        # Load apps
        self.load_apps()

        # Styling: macOS-ish padding
        self.setStyleSheet("""
            QTreeWidget::item { padding: 6px; }
            QListWidget::item { padding: 4px 6px; }
            QPushButton { padding: 6px 12px; }
        """)

    # ---------- Menu ----------
    def _make_menu(self):
        bar = self.menuBar()
        file_menu = bar.addMenu("&File")
        act_quit = QtGui.QAction("Quit", self)
        act_quit.setShortcut(QtGui.QKeySequence.StandardKey.Quit)
        act_quit.triggered.connect(self.close)
        file_menu.addAction(act_quit)

        actions_menu = bar.addMenu("&Actions")
        act_scan = QtGui.QAction("Scan Selected Apps", self)
        act_scan.setShortcut("Ctrl+S")
        act_scan.triggered.connect(self.scan_selected)
        actions_menu.addAction(act_scan)

        act_delete = QtGui.QAction("Delete Checked Items", self)
        act_delete.setShortcut("Ctrl+D")
        act_delete.triggered.connect(self.delete_checked)
        actions_menu.addAction(act_delete)

        help_menu = bar.addMenu("&Help")
        about = QtGui.QAction("About", self)
        about.triggered.connect(self.show_about)
        help_menu.addAction(about)

    def show_about(self):
        QtWidgets.QMessageBox.information(
            self,
            "About",
            "macOS App Cleaner\n\n"
            "• Scans your installed apps\n"
            "• Finds user-space support files via Spotlight and Library sweeps\n"
            "• Lets you review and delete them safely\n\n"
            "Built with PySide6."
        )

    # ---------- App list ----------
    def load_apps(self):
        self.app_list.clear()
        self.all_apps = find_installed_apps()
        # attach bundle ids lazily (during scan) to keep initial load snappy
        for app in self.all_apps:
            item = QtWidgets.QListWidgetItem(app.name)
            item.setData(QtCore.Qt.ItemDataRole.UserRole, app)
            item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.CheckState.Unchecked)
            self.app_list.addItem(item)
        self.status_label.setText(f"Found {len(self.all_apps)} apps.")

    def filter_apps(self, text: str):
        text = text.lower().strip()
        for i in range(self.app_list.count()):
            it = self.app_list.item(i)
            it.setHidden(text not in it.text().lower())

    def select_all_apps(self):
        for i in range(self.app_list.count()):
            it = self.app_list.item(i)
            if not it.isHidden():
                it.setCheckState(QtCore.Qt.CheckState.Checked)

    def deselect_all_apps(self):
        for i in range(self.app_list.count()):
            it = self.app_list.item(i)
            it.setCheckState(QtCore.Qt.CheckState.Unchecked)

    def selected_apps(self) -> List[AppInfo]:
        out: List[AppInfo] = []
        for i in range(self.app_list.count()):
            it = self.app_list.item(i)
            if it.checkState() == QtCore.Qt.CheckState.Checked:
                app = it.data(QtCore.Qt.ItemDataRole.UserRole)
                if isinstance(app, AppInfo):
                    out.append(app)
        return out

    # ---------- Scanning ----------
    def scan_selected(self):
        apps = self.selected_apps()
        if not apps:
            QtWidgets.QMessageBox.information(self, "Nothing selected",
                                              "Please select at least one app to scan.")
            return
        self.tree.clear()
        self.btn_scan.setEnabled(False)
        self.btn_delete.setEnabled(False)
        self.progress.setValue(0)
        self.status_label.setText("Scanning…")

        worker = ScanWorker(apps)
        worker.signals.app_started.connect(self.on_app_started)
        worker.signals.app_progress.connect(self.on_app_progress)
        worker.signals.app_finished.connect(self.on_app_finished)
        worker.signals.all_done.connect(self.on_all_done)
        self.thread_pool.start(worker)

    @QtCore.Slot(str)
    def on_app_started(self, app_name: str):
        self.status_label.setText(f"Scanning {app_name}…")

    @QtCore.Slot(int, int)
    def on_app_progress(self, current: int, total: int):
        pct = int(100 * current / max(1, total))
        self.progress.setValue(pct)

    @QtCore.Slot(object)
    def on_app_finished(self, result: ScanResult):
        # Build tree:
        # App (checked)
        #   Bucket (checked)
        #       file path (checked)
        #   Other Matches
        #       file path
        app_top = QtWidgets.QTreeWidgetItem([result.app.name, "App"])
        app_top.setFlags(app_top.flags() | QtCore.Qt.ItemFlag.ItemIsUserCheckable)
        app_top.setCheckState(0, QtCore.Qt.CheckState.Checked)
        app_top.setData(0, QtCore.Qt.ItemDataRole.UserRole, ("APP", str(result.app.path)))

        def add_child(parent, text, kind, payload=None):
            it = QtWidgets.QTreeWidgetItem([text, kind])
            it.setFlags(it.flags() | QtCore.Qt.ItemFlag.ItemIsUserCheckable)
            it.setCheckState(0, QtCore.Qt.CheckState.Checked)
            if payload is not None:
                it.setData(0, QtCore.Qt.ItemDataRole.UserRole, payload)
            parent.addChild(it)
            return it

        # Buckets
        for bucket, files in sorted(result.files_by_bucket.items(), key=lambda kv: kv[0].lower()):
            bnode = add_child(app_top, bucket, "Group", ("BUCKET", bucket))
            for f in sorted(files, key=lambda p: p.as_posix().lower()):
                add_child(bnode, f.as_posix(), "File", ("FILE", f.as_posix()))

        # Extra hits (Spotlight matches outside our buckets)
        if result.extra_hits:
            onode = add_child(app_top, "Other Matches", "Group", ("BUCKET", "Other Matches"))
            for f in sorted(result.extra_hits, key=lambda p: p.as_posix().lower()):
                add_child(onode, f.as_posix(), "File", ("FILE", f.as_posix()))

        self.tree.addTopLevelItem(app_top)
        self.tree.expandItem(app_top)
        self.btn_delete.setEnabled(self.tree.topLevelItemCount() > 0)

    @QtCore.Slot()
    def on_all_done(self):
        self.status_label.setText("Scan complete.")
        self.btn_scan.setEnabled(True)

    # ---------- Deletion ----------
    def _gather_checked_files(self) -> List[Path]:
        files: List[Path] = []
        for i in range(self.tree.topLevelItemCount()):
            app_node = self.tree.topLevelItem(i)
            self._collect_checked(app_node, files)
        # dedupe; prefer deepest first so if a directory is selected, we won't try individual children after moving
        uniq: List[Path] = []
        seen = set()
        for p in files:
            if p not in seen:
                seen.add(p)
                uniq.append(p)
        # Sort by path depth descending to delete children before parents if deleting directly
        uniq.sort(key=lambda p: len(p.parts), reverse=True)
        return uniq

    def _collect_checked(self, node: QtWidgets.QTreeWidgetItem, out: List[Path]):
        # If node is a file and checked, collect
        if node.checkState(0) == QtCore.Qt.CheckState.Unchecked:
            return
        payload = node.data(0, QtCore.Qt.ItemDataRole.UserRole)
        if payload and isinstance(payload, tuple) and payload[0] == "FILE":
            p = Path(payload[1])
            out.append(p)
        # Recurse
        for i in range(node.childCount()):
            self._collect_checked(node.child(i), out)

    def delete_checked(self):
        targets = self._gather_checked_files()
        if not targets:
            QtWidgets.QMessageBox.information(self, "No items selected",
                                              "Check some files/folders in the results to delete.")
            return

        # Summarize for confirmation
        preview = "\n".join(str(p) for p in targets[:12])
        more = "" if len(targets) <= 12 else f"\n… and {len(targets) - 12} more."
        msg = (f"You are about to delete/move to Trash {len(targets)} item(s).\n\n"
               f"{preview}{more}\n\n"
               "Prefer moving to Trash when possible. Continue?")
        ret = QtWidgets.QMessageBox.warning(
            self,
            "Confirm Deletion",
            msg,
            QtWidgets.QMessageBox.StandardButton.Cancel | QtWidgets.QMessageBox.StandardButton.Ok,
            QtWidgets.QMessageBox.StandardButton.Cancel
        )
        if ret != QtWidgets.QMessageBox.StandardButton.Ok:
            return

        # Try moving to Trash first
        moved, removed, failed = self._move_or_delete(targets)

        msg = (f"Finished.\n\nMoved to Trash: {len(moved)}\n"
               f"Permanently deleted: {len(removed)}\n"
               f"Failed: {len(failed)}")
        if failed:
            msg += "\n\nFailures:\n" + "\n".join(f"{p} — {err}" for p, err in failed[:10])
            if len(failed) > 10:
                msg += f"\n… and {len(failed)-10} more."
        QtWidgets.QMessageBox.information(self, "Cleanup", msg)

        # Remove deleted nodes from the tree (optimistic)
        self._prune_deleted_nodes()
        self.btn_delete.setEnabled(self.tree.topLevelItemCount() > 0)

    def _move_or_delete(self, targets: List[Path]):
        trash = Path.home() / ".Trash"
        moved, removed, failed = [], [], []

        for p in targets:
            try:
                if not p.exists():
                    continue
                # Prefer move to Trash when on same volume and Trash exists
                can_move = trash.exists() and p.anchor == trash.anchor
                if can_move:
                    # Ensure unique filename in Trash
                    dest = trash / p.name
                    suffix = 1
                    while dest.exists():
                        dest = trash / f"{p.stem} {suffix}{p.suffix}"
                        suffix += 1
                    shutil.move(str(p), str(dest))
                    moved.append(p)
                else:
                    # Fall back to permanent delete
                    if p.is_dir():
                        shutil.rmtree(p, ignore_errors=False)
                    else:
                        p.unlink()
                    removed.append(p)
            except Exception as e:
                failed.append((p, str(e)))
        return moved, removed, failed

    def _prune_deleted_nodes(self):
        # Walk tree and drop FILE nodes that no longer exist; prune empty groups; prune empty apps
        def node_exists(n: QtWidgets.QTreeWidgetItem) -> bool:
            payload = n.data(0, QtCore.Qt.ItemDataRole.UserRole)
            if payload and isinstance(payload, tuple) and payload[0] == "FILE":
                return Path(payload[1]).exists()
            return True  # non-file "group" nodes considered present

        def prune_node(n: QtWidgets.QTreeWidgetItem) -> bool:
            # returns True if node should be kept
            for i in reversed(range(n.childCount())):
                child = n.child(i)
                keep = prune_node(child)
                if not keep:
                    n.removeChild(child)
            # After pruning children, decide for this node
            payload = n.data(0, QtCore.Qt.ItemDataRole.UserRole)
            if payload and isinstance(payload, tuple) and payload[0] == "FILE":
                return node_exists(n)
            # Keep non-file nodes if they still have children
            return n.childCount() > 0

        for i in reversed(range(self.tree.topLevelItemCount())):
            top = self.tree.topLevelItem(i)
            keep = prune_node(top)
            if not keep:
                self.tree.takeTopLevelItem(i)


def main():
    # Strongly recommend running on macOS only
    if sys.platform != "darwin":
        QtWidgets.QMessageBox.warning(None, "Platform Warning", "This tool is intended for macOS.")
    QtWidgets.QApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_DontUseNativeMenuBar, False)
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("macOS App Cleaner")
    win = AppCleaner()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
