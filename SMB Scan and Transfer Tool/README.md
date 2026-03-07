# SMB Scan and Transfer Tool

A Qt6-based GUI application for discovering, browsing, and transferring files over SMB (Samba) network shares on macOS. Features Zeroconf/Bonjour discovery, two-pane file explorer, and resumable transfers with optional MD5 verification.

## Features

- **Zeroconf Discovery**: Automatically discovers SMB services on the local network via Bonjour (`_smb._tcp.local`)
- **Host & Share Listing**: Lists available shares using macOS `smbutil view` (anonymous and authenticated)
- **Mount/Unmount Shares**: Mount SMB shares via `mount_smbfs` to `/Volumes/<Share>`
- **Two-Pane File Explorer**: Browse local and remote files side-by-side with `QFileSystemModel`
- **File Operations**: Copy, delete, rename, and create new folders between local and remote panes
- **Multi-Select**: Checkboxes on both panes for batch operations
- **Resumable Transfers**: Size-aware and partial-file-aware recursive copy with resume support
- **MD5 Verification**: Optional MD5 hash verification toggle for transferred files
- **Threaded Transfers**: Per-file and overall progress bars with cancellation support
- **Status & Logging**: Detailed log panel and persistent log at `~/Library/Logs/SimpleSMBExplorer.log`
- **Credential Management**: Auth prompt with optional save to macOS Keychain via `keyring`

## Requirements

- Python 3.10+
- macOS 12+ (uses macOS tools: `smbutil`, `mount_smbfs`, `diskutil`)
- PySide6 6.6+
- zeroconf
- keyring
- psutil (optional)

## Installation

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install PySide6>=6.6 zeroconf keyring
```

Optional:

```bash
pip install psutil
```

## Usage

Run the application:

```bash
python smb_transfer_tool.py
```

### Workflow

1. **Discover**: The tool automatically discovers SMB services on your local network
2. **Connect**: Select a discovered host or enter an IP/hostname manually
3. **Authenticate**: Enter credentials if required (optionally save to Keychain)
4. **Browse**: Navigate local and remote files in the two-pane explorer
5. **Transfer**: Select files and use the action buttons to copy between panes
6. **Verify**: Enable MD5 verification for transfer integrity checks

## Notes

- This tool is designed for **macOS only** — it relies on macOS-specific command-line tools
- MD5 verification on large files can be slow; disable if not needed
- Resume will append from the destination file size if it is smaller than the source

## Author

Randy Northrup

## License

MIT License — free to use, modify, and share.
