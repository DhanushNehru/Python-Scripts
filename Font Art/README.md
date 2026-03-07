# Font Art — Cute Glassy Qt6 App

A tiny, bubbly, cross‑platform app for making adorable ASCII font art. It sports a soft pink + baby‑blue “glass” card, rounded corners, cozy shadows, and a frameless, draggable window.

## Highlights

- Glassy theme with rounded edges, soft shadows, and higher opacity for readability
- Frameless and draggable (drag by the logo or card area)
- Animated title logo cycles a random FIGlet font every 3 seconds (logo refresh only)
- Centered text box, powder‑blue label “Choose Font Style”, and a scrollable font dropdown
- Powder‑blue tinted dropdown arrow; dropdown text matches the input’s gray
- Fixed logo area positioned just above the inputs (layout never jumps)
- “Create” prompts where to save `.txt`; “Quit” closes the app
- Cross‑platform ready: Windows, macOS, Linux (PySide6)

## Files

- App: `Python-Scripts/Font Art/FontArtQt6.py`
- Requirements: `Python-Scripts/Font Art/requirements.txt`

## Quick Start

1) Python 3.9+ is recommended.

2) Create a virtual environment (optional, but tidy):

- Windows
  - `py -m venv .venv`
  - `.venv\Scripts\activate`
- macOS/Linux
  - `python3 -m venv .venv`
  - `source .venv/bin/activate`

3) Install dependencies:
- `pip install -r "Python-Scripts/Font Art/requirements.txt"`

4) Run the app:
- `python "Python-Scripts/Font Art/FontArtQt6.py"`

## Use It

- Type your text in the input box.
- Pick a font from the dropdown (it defaults to the first available font).
- Click “Create” and choose where to save the generated ASCII art `.txt` file.
- The title logo keeps changing fonts every few seconds — only the logo area updates.

## Make a Stand‑Alone Binary (Optional)

- Windows
  - `pyinstaller --noconsole --onefile "Python-Scripts/Font Art/FontArtQt6.py"`
- macOS
  - `pyinstaller --windowed --onefile "Python-Scripts/Font Art/FontArtQt6.py"`
- Linux
  - `pyinstaller --windowed --onefile "Python-Scripts/Font Art/FontArtQt6.py"`

Notes:
- On Linux, transparency/shadows require a compositor (most desktops enable one by default).
- macOS app signing/notarization is not included here.

## Troubleshooting

- No fonts listed? A small fallback set is used if `pyfiglet` can’t load the full list.
- Transparency looks different across desktops; this app uses a higher‑opacity glass gradient by default.
- Window won’t drag? Drag by the logo or anywhere on the glass card background.

## Credits

- ASCII rendering by `pyfiglet`
- UI framework: `PySide6` (Qt for Python)

