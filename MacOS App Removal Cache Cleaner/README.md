# macOS App Remover and Cache Cleaner

A desktop utility for macOS that scans installed applications, finds user-space support files (preferences, caches, logs, etc.), and lets you safely review and delete them. Built with PySide6 for a modern, native-like UI.

---

## ✨ Features

- **App discovery:** Lists all installed `.app` bundles in `/Applications` and `~/Applications`.
- **Deep scan:** Finds related files using both Spotlight and targeted sweeps of user Library buckets (Application Support, Preferences, Caches, Containers, etc.).
- **Review before delete:** Presents all found files in a checkable tree grouped by type.
- **Safe deletion:** Moves files to Trash when possible, falls back to permanent deletion if needed.
- **Batch operations:** Select multiple apps, scan, and clean up in one go.
- **Progress and status:** Live progress bar, status messages, and scan summaries.
- **Modern UI:** Search/filter apps, select/deselect all, rescan, and more.
- **macOS native:** Designed specifically for macOS; uses system Trash and Spotlight.

---

## 📦 Requirements

- **macOS** (tested on 10.15+)
- **Python 3.9+**
- **PySide6** (`pip install PySide6`)

---

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install PySide6
   ```

2. **Run the app:**
   ```bash
   python mac_app_removal.py
   ```

3. **Usage:**
   - Filter or select apps from the list.
   - Click "Scan Selected Apps" to find related files.
   - Review results in the tree view.
   - Check/uncheck items to delete.
   - Click "Delete Checked Items" to move files to Trash or delete permanently.

---

## 🧭 UI Overview

- **Left panel:** App list with search/filter and select/deselect all.
- **Right panel:** Tree view of scan results, grouped by Library bucket and file type.
- **Controls:** Scan, delete, progress bar, and status.
- **Menu:** File (Quit), Actions (Scan/Delete), Help (About).

---

## 🗂️ What Gets Scanned

- **Application Support**
- **Preferences**
- **Caches**
- **Containers**
- **Group Containers**
- **Saved Application State**
- **Logs**
- **WebKit**
- **Cookies**
- **LaunchAgents**
- **Other matches** found via Spotlight

---

## 🔒 Safety & Ethics

- **Review before delete:** All files are presented for review; nothing is deleted automatically.
- **Moves to Trash:** Prefers moving files to Trash for easy recovery.
- **Permanent deletion:** Only used if Trash is unavailable or on a different volume.
- **Responsibility:** Use with care; deleting files may affect app settings or data.

---

## 🆘 Troubleshooting

- **Not finding all files:** Some apps store data outside standard buckets or use hidden locations.
- **Permission errors:** Run as a user with access to the files you want to delete.
- **Platform warning:** This tool is intended for macOS only.

---

## 🛠️ Building a Standalone App (optional)

Use PyInstaller:

```bash
pip install pyinstaller
pyinstaller --windowed --name "macOS App Cleaner" mac_app_removal.py
```

---

## 📄 License

MIT License.

---

## 👤 Author

**Randy Northrup**
