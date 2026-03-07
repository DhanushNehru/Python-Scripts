"""Application entry point."""

import sys

from PySide6.QtWidgets import QApplication

from wifiqr.ui.main_window import MainWindow


def main() -> int:
    """Run the Qt application and return the exit code."""
    app = QApplication(sys.argv)
    app.setApplicationName("WifiQR")
    app.setOrganizationName("WifiQR")

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
