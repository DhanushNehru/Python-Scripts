import os
import random
from typing import List

from pyfiglet import Figlet, FigletFont

from PySide6 import QtCore, QtGui, QtWidgets


APP_TITLE_TEXT = "Font Art"


def list_figlet_fonts() -> List[str]:
    try:
        return sorted(FigletFont.getFonts())
    except Exception:
        # Fallback: a small known-good subset if pyfiglet fails
        return [
            "standard",
            "slant",
            "big",
            "doom",
            "banner",
            "block",
            "digital",
            "roman",
            "script",
            "shadow",
        ]


class GlassCard(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("GlassCard")
        self.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        # Drop shadow for a bubbly, floating feel
        effect = QtWidgets.QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(40)
        effect.setXOffset(0)
        effect.setYOffset(12)
        effect.setColor(QtGui.QColor(0, 0, 0, 80))
        self.setGraphicsEffect(effect)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        # Custom rounded, semi-transparent gradient card painting
        radius = 24
        rect = self.rect()
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # Glassy gradient: baby blue -> pink with alpha
        grad = QtGui.QLinearGradient(rect.topLeft(), rect.bottomRight())
        # Reduce transparency by ~20% (increase opacity)
        grad.setColorAt(0.0, QtGui.QColor(173, 216, 230, 216))  # was 180
        grad.setColorAt(1.0, QtGui.QColor(255, 182, 193, 216))  # was 180

        path = QtGui.QPainterPath()
        path.addRoundedRect(rect.adjusted(1, 1, -1, -1), radius, radius)

        # Subtle border highlight
        pen = QtGui.QPen(QtGui.QColor(255, 255, 255, 204), 1.2)
        painter.setPen(pen)
        painter.fillPath(path, grad)
        painter.drawPath(path)


class LogoView(QtWidgets.QTextEdit):
    """A read-only text view for the ASCII logo that we can refresh alone."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setFrameStyle(QtWidgets.QFrame.NoFrame)
        # Monospace font for alignment
        font = QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.FixedFont)
        font.setPointSize(10)
        self.setFont(font)
        self.setObjectName("LogoView")

    def sizeHint(self) -> QtCore.QSize:
        # Larger fixed logo area that still sits near inputs
        return QtCore.QSize(560, 120)


class PowderArrowStyle(QtWidgets.QProxyStyle):
    """Custom style to tint the combo box down-arrow to powder blue."""

    def drawPrimitive(self, element, option, painter, widget=None):
        if element == QtWidgets.QStyle.PE_IndicatorArrowDown:
            painter.save()
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(QtGui.QColor("#B0E0E6"))  # powder blue
            r = option.rect
            size = int(min(r.width(), r.height()) * 0.45)
            cx, cy = r.center().x(), r.center().y()
            pts = [
                QtCore.QPoint(cx - size, cy - size // 3),
                QtCore.QPoint(cx + size, cy - size // 3),
                QtCore.QPoint(cx, cy + size // 2),
            ]
            painter.drawPolygon(QtGui.QPolygon(pts))
            painter.restore()
            return
        super().drawPrimitive(element, option, painter, widget)


class FontArtWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("RootWindow")
        self.setWindowTitle("Font Art – Qt6")
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        # Frameless floating style
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window
        )
        self.resize(820, 560)

        # Central card with glassy look
        self.card = GlassCard(self)

        # Child layout within card
        card_layout = QtWidgets.QVBoxLayout(self.card)
        card_layout.setContentsMargins(24, 16, 24, 16)
        # We'll control exact gaps manually (logo->inputs 15px, inputs->buttons 6px)
        card_layout.setSpacing(0)

        # ASCII logo at top that only refreshes itself
        self.logo_view = LogoView()
        # Center ASCII content within the logo view
        doc = self.logo_view.document()
        opt = doc.defaultTextOption()
        opt.setAlignment(QtCore.Qt.AlignHCenter)
        doc.setDefaultTextOption(opt)
        self.logo_view.setAlignment(QtCore.Qt.AlignHCenter)
        # Fix the logo area height so layout below never moves
        self.logo_view.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.logo_view.setFixedHeight(self.logo_view.sizeHint().height())
        # Top stretch so the logo+inputs cluster is not pinned to the top
        card_layout.addStretch(1)
        card_layout.addWidget(self.logo_view)
        # Place the logo box just above the inputs with a 15px gap
        card_layout.addSpacing(15)

        # Input row: text box, font dropdown (with label over dropdown)
        self.input_edit = QtWidgets.QLineEdit()
        self.input_edit.setPlaceholderText("Type text to render…")
        self.input_edit.setObjectName("InputEdit")
        self.input_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.input_edit.setMinimumWidth(520)  # a little wider for comfortable typing

        self.font_combo = QtWidgets.QComboBox()
        self.font_combo.setObjectName("FontCombo")
        self.font_combo.setMaxVisibleItems(14)
        self.font_combo.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.font_combo.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.font_combo.setView(QtWidgets.QListView())  # scrollable
        self.font_combo.setFixedWidth(240)  # static size for consistent layout
        # Apply custom style with powder-blue arrow tint
        self.font_combo.setStyle(PowderArrowStyle(self.style()))

        self.font_label = QtWidgets.QLabel("Choose Font Style")
        self.font_label.setObjectName("FontLabel")
        self.font_label.setAlignment(QtCore.Qt.AlignHCenter)

        # Align textbox and dropdown in the same row; label sits just above dropdown
        font_widget = QtWidgets.QWidget()
        font_widget.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        font_col = QtWidgets.QVBoxLayout(font_widget)
        font_col.setSpacing(4)
        font_col.setContentsMargins(0, 0, 0, 0)
        font_col.addWidget(self.font_label, alignment=QtCore.Qt.AlignHCenter)
        font_col.addWidget(self.font_combo, alignment=QtCore.Qt.AlignVCenter)

        input_row = QtWidgets.QHBoxLayout()
        input_row.setSpacing(10)
        input_row.setContentsMargins(0, 0, 0, 0)
        input_row.addStretch(1)
        # Align bottoms so the text box and dropdown bottoms line up
        input_row.addWidget(self.input_edit, 0, QtCore.Qt.AlignBottom)
        input_row.addWidget(font_widget, 0, QtCore.Qt.AlignBottom)
        input_row.addStretch(1)
        card_layout.addLayout(input_row)

        # Buttons row: Create and Quit
        self.generate_btn = QtWidgets.QPushButton("Create")
        self.generate_btn.setObjectName("GenerateButton")
        self.generate_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.quit_btn = QtWidgets.QPushButton("Quit")
        self.quit_btn.setObjectName("QuitButton")
        self.quit_btn.setCursor(QtCore.Qt.PointingHandCursor)

        buttons_row = QtWidgets.QHBoxLayout()
        buttons_row.setSpacing(12)
        # Equal spacing across width: left, between, right stretches
        buttons_row.addStretch(1)
        buttons_row.addWidget(self.generate_btn)
        buttons_row.addStretch(1)
        buttons_row.addWidget(self.quit_btn)
        buttons_row.addStretch(1)
        # 6px gap from inputs to buttons row
        card_layout.addSpacing(6)
        card_layout.addLayout(buttons_row)
        # Bottom stretch so the cluster stays together above buttons
        card_layout.addStretch(1)

        # Populate fonts
        self.fonts: List[str] = list_figlet_fonts()
        self.font_combo.addItems(self.fonts)
        if self.fonts:
            self.font_combo.setCurrentIndex(0)  # ensure not empty

        # Figlet instance for rendering
        self.figlet = Figlet(font=self.fonts[0] if self.fonts else "standard")

        # Connections
        self.generate_btn.clicked.connect(self.on_generate)
        self.font_combo.currentTextChanged.connect(self.on_font_change)
        self.quit_btn.clicked.connect(self.close)

        # Timer for rotating logo font every 3 seconds
        self.logo_timer = QtCore.QTimer(self)
        self.logo_timer.setInterval(3000)
        self.logo_timer.timeout.connect(self.refresh_logo)
        self.logo_timer.start()

        # Initial render
        self.refresh_logo()

        # Overall layout for root: center the card
        root_layout = QtWidgets.QVBoxLayout(self)
        root_layout.setContentsMargins(24, 24, 24, 24)
        root_layout.addWidget(self.card)

        # Apply stylesheet theme
        self.apply_styles()
        # Make buttons equal width for symmetry
        btn_w = max(self.generate_btn.sizeHint().width(), self.quit_btn.sizeHint().width())
        self.generate_btn.setMinimumWidth(btn_w)
        self.quit_btn.setMinimumWidth(btn_w)

        # Adjust window width to fit content tightly
        self.adjust_width_to_content()

        # Match heights of the input and dropdown so bottoms are perfectly even
        QtCore.QTimer.singleShot(0, self._sync_input_heights)

        # Make window draggable from the logo or the card background
        self._drag_pos: QtCore.QPoint | None = None
        self.logo_view.installEventFilter(self)
        self.card.installEventFilter(self)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super().resizeEvent(event)
        # Reflow logo art to fit within fixed logo area when resized
        QtCore.QTimer.singleShot(0, self.refresh_logo)

    def apply_styles(self):
        # Baby blue + pink theme, rounded, glassy controls
        self.setStyleSheet(
            """
            #RootWindow {
                background: transparent;
            }
            QLabel {
                color: #B0E0E6; /* powder blue */
                font-weight: 600;
            }

            #LogoView {
                color: rgba(35, 35, 35, 235);
                background: transparent;
                border-radius: 12px;
            }

            #InputEdit {
                padding: 10px 14px;
                border-radius: 14px;
                border: 1px solid rgba(255,255,255,216);
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 240, 245, 240),   /* lavenderblush */
                    stop:1 rgba(224, 247, 250, 240)    /* light cyan */
                );
                color: #222;
                selection-background-color: rgba(255,182,193,216);
            }
            #InputEdit:focus {
                border: 1.5px solid rgba(135, 206, 235, 255);
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 228, 235, 255),
                    stop:1 rgba(210, 245, 255, 255)
                );
            }

            #FontCombo {
                padding: 8px 12px;
                border-radius: 14px;
                border: 1px solid rgba(255,255,255,216);
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(224, 247, 250, 240),
                    stop:1 rgba(255, 240, 245, 240)
                );
                color: #222; /* match input text color */
            }
            #FontCombo::drop-down {
                width: 26px;
                border: 0px;
            }
            #FontCombo QAbstractItemView {
                background: rgba(255,255,255, 255);
                border: 1px solid rgba(135,206,235,216);
                color: #222; /* match input text color */
                selection-background-color: rgba(255, 182, 193, 240);
                outline: none;
            }

            #GenerateButton, #QuitButton {
                padding: 12px 22px; /* slightly increased padding */
                border-radius: 18px;
                border: 1px solid rgba(255,255,255,216);
                color: #1f2937;
                font-weight: 600;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(173, 216, 230, 255),
                    stop:1 rgba(255, 182, 193, 255)
                );
            }
            #GenerateButton:hover, #QuitButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(173, 216, 230, 255),
                    stop:1 rgba(255, 182, 193, 255)
                );
            }
            #GenerateButton:pressed, #QuitButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(173, 216, 230, 240),
                    stop:1 rgba(255, 182, 193, 240)
                );
            }

            #FontLabel {
                padding-left: 0px;
            }
            """
        )

    # --- Logic ---
    def eventFilter(self, source: QtCore.QObject, event: QtCore.QEvent) -> bool:
        # Enable dragging the frameless window by grabbing the logo or card background
        if source in (self.logo_view, self.card):
            if event.type() == QtCore.QEvent.MouseButtonPress and isinstance(event, QtGui.QMouseEvent):
                if event.button() == QtCore.Qt.LeftButton:
                    # Store offset from top-left corner
                    global_pos = event.globalPosition() if hasattr(event, "globalPosition") else event.globalPos()
                    if isinstance(global_pos, QtCore.QPointF):
                        global_pos = global_pos.toPoint()
                    self._drag_pos = global_pos - self.frameGeometry().topLeft()
                    return True
            elif event.type() == QtCore.QEvent.MouseMove and isinstance(event, QtGui.QMouseEvent):
                if self._drag_pos is not None and (event.buttons() & QtCore.Qt.LeftButton):
                    global_pos = event.globalPosition() if hasattr(event, "globalPosition") else event.globalPos()
                    if isinstance(global_pos, QtCore.QPointF):
                        global_pos = global_pos.toPoint()
                    self.move(global_pos - self._drag_pos)
                    return True
            elif event.type() == QtCore.QEvent.MouseButtonRelease and isinstance(event, QtGui.QMouseEvent):
                if self._drag_pos is not None:
                    self._drag_pos = None
                    return True
        return super().eventFilter(source, event)
    def refresh_logo(self):
        if not self.fonts:
            return

        # Determine character columns that fit in the logo viewport width
        viewport_w = self.logo_view.viewport().width()
        metrics = QtGui.QFontMetrics(self.logo_view.font())
        char_w = max(1, metrics.horizontalAdvance("M"))
        cols = max(40, int((viewport_w - 16) / char_w))

        random_font = random.choice(self.fonts)
        try:
            fig = Figlet(font=random_font, width=cols, justify="center")
            art = fig.renderText(APP_TITLE_TEXT)
        except Exception:
            art = APP_TITLE_TEXT

        # Update content
        self.logo_view.setPlainText(art)

        # Fit height: reduce font size if needed so title fits above actions
        self._fit_logo_height(art)

    def on_font_change(self, font_name: str):
        try:
            self.figlet.setFont(font=font_name)
        except Exception:
            # ignore invalid font switches
            pass

    def on_generate(self):
        text = self.input_edit.text().strip()
        if not text:
            QtWidgets.QMessageBox.information(self, "Nothing to render", "Please enter some text to render.")
            return

        selected_font = self.font_combo.currentText() or "standard"
        try:
            self.figlet.setFont(font=selected_font)
            art = self.figlet.renderText(text)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Render failed", f"Could not render text with font '{selected_font}'.\n{e}")
            return

        # Ask where to save
        default_name = f"{text[:20].strip().replace(' ', '_') or 'font_art'}.txt"
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save ASCII Art",
            os.path.join(os.path.expanduser("~"), default_name),
            "Text Files (*.txt);;All Files (*)",
        )
        if not path:
            return

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(art)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Save failed", f"Could not save file:\n{e}")
            return

        QtWidgets.QMessageBox.information(self, "Saved", f"Art saved to:\n{path}")

    # --- Helpers ---
    def _fit_logo_height(self, art: str) -> None:
        # Keep the logo area height fixed; only adjust font size down to fit
        max_h = max(60, self.logo_view.height() - 4)
        f = self.logo_view.font()
        pt = f.pointSize() if f.pointSize() > 0 else 10
        metrics = QtGui.QFontMetrics(f)

        lines = art.splitlines() or [""]
        req_h = len(lines) * metrics.lineSpacing()
        while req_h > max_h and pt > 7:
            pt -= 1
            f.setPointSize(pt)
            self.logo_view.setFont(f)
            metrics = QtGui.QFontMetrics(f)
            req_h = len(lines) * metrics.lineSpacing()
        # Do not change widget height; positions of other items remain constant

    def _sync_input_heights(self) -> None:
        h = max(self.input_edit.sizeHint().height(), self.font_combo.sizeHint().height())
        self.input_edit.setFixedHeight(h)
        self.font_combo.setFixedHeight(h)

    def adjust_width_to_content(self):
        # Compute desired content width based on input+combo and buttons rows
        input_w = max(self.input_edit.minimumWidth(), self.input_edit.sizeHint().width())
        combo_w = self.font_combo.width() or self.font_combo.sizeHint().width()
        input_row_spacing = 12  # mirrors layout spacing
        content_row_w = input_w + input_row_spacing + combo_w

        # Buttons row width
        btn_w = max(self.generate_btn.minimumWidth(), self.generate_btn.sizeHint().width())
        quit_w = max(self.quit_btn.minimumWidth(), self.quit_btn.sizeHint().width())
        buttons_row_spacing = 12
        buttons_row_w = btn_w + buttons_row_spacing + quit_w

        content_w = max(content_row_w, buttons_row_w)

        # Add layout margins (card + root)
        card_m = self.card.layout().contentsMargins()
        root_m = self.layout().contentsMargins()
        total_w = content_w + (card_m.left() + card_m.right()) + (root_m.left() + root_m.right()) + 8

        # Constrain to a sensible minimum to avoid clipping
        min_w = 560
        total_w = max(total_w, min_w)

        self.setFixedWidth(total_w)


def main():
    app = QtWidgets.QApplication([])

    # Prefer system dark text rendering in semi-transparent windows
    app.setApplicationName("Font Art Qt6")
    app.setOrganizationName("FontArt")
    app.setStyle("Fusion")

    win = FontArtWindow()
    win.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
