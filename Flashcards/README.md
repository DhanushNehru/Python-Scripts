# Python Interactive Flashcards

A lightweight, desktop-based flashcard application built with Python and Tkinter. This tool utilizes a Spaced Repetition System (SRS) to help you memorize information efficiently by scheduling reviews based on how well you remember each card.

### 🚀 Features

* **Dual Modes:** Separate workflows for **Learning** (new cards) and **Reviewing** (existing cards).
* **Spaced Repetition Algorithm:** Automatically calculates the best time to review a card based on your performance (intervals of 1, 3, 5, 7, and 15 days).
* **Persistent Storage:** All data is saved locally in a JSON file, so you never lose your progress.
* **Card Management:** Add, Edit, and Delete cards directly within the app.
* **Progress Tracking:** The main menu displays exactly how many cards are pending for learning or review.
* **Clean Interface:** Simple, distraction-free GUI.

### 🛠️ Running

1. **Clone the Repository or Download the Script**
2. **Navigate to the Script Location**
3. **Run the Script** 

### 📖 Usage Guide

#### 1. The Main Menu

Upon launching, you will see the dashboard.

* **New Learning:** Shows the count of cards you have created but haven't studied yet.
* **To Review:** Shows the count of cards due for review today (based on the SRS algorithm).

#### 2. Adding Cards

* Click **"➕ Add Card"** in the main menu.
* Enter the **Question** (Front) and **Answer** (Back).
* Click **Save**. You can add multiple cards in a row.

#### 3. Learning Mode (New Cards)

* Click **"🆕 Start Learning"**.
* This mode presents cards you have never seen before.
* Click the card to flip it and reveal the answer.
* Click **"⏭ Next"** to mark the card as "Learned."
* *Note: Once learned, a card enters the review cycle and will be scheduled for its first review tomorrow (Day +1).*

#### 4. Review Mode (Memory Training)

* Click **"🔄 Start Review"**.
* This mode only shows cards that are due for review today or are overdue.
* **Flip the card** to see the answer. You will see two options:
* **🟩 Remembered:** The card is upgraded. The interval until the next review increases (e.g., 3 days  5 days  7 days).
* **🟥 Forgot:** The card level is reset to 0. It will be scheduled for review again tomorrow to reinforce memory.

#### 5. Managing Cards

While inside the Learning or Review interface, you can manage the current card using the buttons at the bottom:

* **🗑️ Delete:** Permanently removes the current card.
* **✏️ Edit:** Allows you to modify typos or update the question/answer text.

### 🧠 How the Algorithm Works

The app uses a simplified interval scheduling logic to maximize retention:

1. **New Card:** Becomes due **1 day** after first learning.
2. **Review Level 0:** If remembered  due in **3 days**.
3. **Review Level 1:** If remembered  due in **5 days**.
4. **Review Level 2:** If remembered  due in **7 days**.
5. **Review Level 3+:** If remembered  due in **15 days** (Max interval).
6. **Forgot:** If you mark a card as "Forgot" at any stage, it resets to **Level 0** and becomes due tomorrow.

### 📂 Data Storage

* Your cards are stored in a file named `flashcards_data.json` located in the same directory as the script.
* **Do not delete this file**, or you will lose your flashcards and progress history.
* You can back up this file to save your data.
