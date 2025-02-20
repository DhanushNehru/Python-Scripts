import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

# Chess symbols for pieces (Unicode)
chess_pieces = {
    "rook_white": "\u2656",
    "rook_black": "\u265C",
    "pawn_white": "\u2659",
    "pawn_black": "\u265F",
}

# Initial piece positions for demonstration
initial_pieces = [
    (0, 0, chess_pieces["rook_black"]),
    (0, 7, chess_pieces["rook_black"]),
    (7, 0, chess_pieces["rook_white"]),
    (7, 7, chess_pieces["rook_white"]),
    (1, 0, chess_pieces["pawn_black"]),
    (1, 7, chess_pieces["pawn_black"]),
    (6, 0, chess_pieces["pawn_white"]),
    (6, 7, chess_pieces["pawn_white"]),
]

# Function to draw the chessboard
def draw_chessboard(highlight_squares=None):
    board_size = 8
    chessboard = np.add.outer(range(board_size), range(board_size)) % 2

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(chessboard, cmap="cividis", interpolation="nearest")

    # Remove axes for a cleaner look
    ax.set_xticks([])
    ax.set_yticks([])

    # Add grid lines to separate the squares
    for i in range(board_size + 1):
        ax.axhline(i - 0.5, color="black", linewidth=1, alpha=0.7)
        ax.axvline(i - 0.5, color="black", linewidth=1, alpha=0.7)

    # Highlight specific squares
    if highlight_squares:
        for (row, col) in highlight_squares:
            ax.add_patch(Rectangle((col - 0.5, row - 0.5), 1, 1, color="yellow", alpha=0.4))

    # Add chess pieces
    for row, col, piece in initial_pieces:
        ax.text(col, row, piece, fontsize=28, ha="center", va="center", color="black" if (row + col) % 2 == 0 else "white")

    # Add coordinate labels
    for i in range(board_size):
        ax.text(-0.8, i, str(8 - i), fontsize=12, va="center")  # Row labels
        ax.text(i, 8 - 0.3, chr(65 + i), fontsize=12, ha="center")  # Column labels

    # Title
    ax.set_title("Chess Board", fontweight="bold", fontsize=16)

    plt.show()

# Highlight squares (optional demo)
highlight = [(0, 0), (7, 7), (3, 3)]  # Example of squares to highlight
draw_chessboard(highlight_squares=highlight)
