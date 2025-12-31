import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import random
import os
from datetime import datetime, timedelta, timedelta

DATA_FILE = os.path.join(os.path.dirname(__file__), "flashcards_data.json")

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Interactive Flashcards")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")

        self.cards = self.load_data()
        self.current_card = {}
        self.is_flipped = False
        self.study_queue = []
        self.mode = None # "learn" or "review"

        self.menu_frame = tk.Frame(root, bg="#f0f0f0")
        self.game_frame = tk.Frame(root, bg="#f0f0f0")
        self.completion_frame = tk.Frame(root, bg="#f0f0f0")

        self.setup_menu_ui()
        self.setup_game_ui()
        self.setup_completion_ui()

        self.show_menu()

    def setup_menu_ui(self):
        tk.Label(self.menu_frame, text="Flashcard", font=("Microsoft YaHei", 24, "bold"), bg="#f0f0f0", fg="#333").pack(pady=40)

        self.lbl_learn_count = tk.Label(self.menu_frame, text="", font=("Microsoft YaHei", 12), bg="#f0f0f0", fg="#666")
        self.lbl_learn_count.pack()
        tk.Button(self.menu_frame, text="🆕 Start Learning", command=self.start_learn, font=("Microsoft YaHei", 14), bg="#ddffdd", width=20).pack(pady=10)

        self.lbl_review_count = tk.Label(self.menu_frame, text="", font=("Microsoft YaHei", 12), bg="#f0f0f0", fg="#666")
        self.lbl_review_count.pack()
        tk.Button(self.menu_frame, text="🔄 Start Review", command=self.start_review, font=("Microsoft YaHei", 14), bg="#ddddff", width=20).pack(pady=10)

        tk.Button(self.menu_frame, text="➕ Add Card", command=self.add_card_window, font=("Microsoft YaHei", 12), bg="#fff").pack(pady=20)
        tk.Button(self.menu_frame, text="🚪 Exit", command=self.root.destroy, font=("Microsoft YaHei", 12), bg="#eee").pack(pady=5)

    def setup_game_ui(self):
        self.header_label = tk.Label(self.game_frame, text="Memory Training", font=("Microsoft YaHei", 16, "bold"), bg="#f0f0f0", fg="#333")
        self.header_label.pack(pady=20)

        self.card_canvas = tk.Canvas(self.game_frame, width=500, height=280, bg="white", highlightthickness=0)
        self.card_canvas.pack(pady=10)
        self.card_text = self.card_canvas.create_text(250, 140, text="", font=("Microsoft YaHei", 20, "bold"), width=480, fill="black")
        self.card_canvas.bind("<Button-1>", self.flip_card)

        tk.Label(self.game_frame, text="Click card to reveal answer", font=("Arial", 10), bg="#f0f0f0", fg="#777").pack(pady=5)

        self.button_frame = tk.Frame(self.game_frame, bg="#f0f0f0")
        self.button_frame.pack(pady=20, fill="x")

        btn_config = {"font": ("Microsoft YaHei", 10), "width": 12, "pady": 5, "bd": 1}
        
        self.btn_next = tk.Button(self.button_frame, text="⏭ Next", command=self.next_card, bg="#ddddff", **btn_config)
        self.btn_remember = tk.Button(self.button_frame, text="Remembered", command=self.mark_remembered, bg="#ddffdd", **btn_config)
        self.btn_forgot = tk.Button(self.button_frame, text="Forgot", command=self.mark_forgot, bg="#ffdddd", **btn_config)
        self.btn_back_menu = tk.Button(self.button_frame, text="🏠 Main Menu", command=self.show_menu, bg="#eeeeee", **btn_config)
        self.btn_back_menu.pack(side="left", padx=20)
        
        self.btn_delete = tk.Button(self.button_frame, text="🗑️ Delete", command=self.delete_card, bg="#ffcccc", **btn_config)
        self.btn_delete.pack(side="left", padx=5)

        self.btn_edit = tk.Button(self.button_frame, text="✏️ Edit", command=self.edit_card, bg="#fff", **btn_config)
        self.btn_edit.pack(side="left", padx=5)

    def setup_completion_ui(self):
        tk.Label(self.completion_frame, text="🎉 Congratulations!", font=("Microsoft YaHei", 24, "bold"), bg="#f0f0f0", fg="#27ae60").pack(pady=50)
        tk.Label(self.completion_frame, text="All cards in current queue completed.", font=("Microsoft YaHei", 14), bg="#f0f0f0").pack(pady=10)
        tk.Button(self.completion_frame, text="🏠 Main Menu", command=self.show_menu, font=("Microsoft YaHei", 14), bg="#ddddff").pack(pady=30)

    def show_menu(self):
        self.game_frame.pack_forget()
        self.completion_frame.pack_forget()
        self.menu_frame.pack(fill="both", expand=True)

        learn_count = len([c for c in self.cards if c.get("status") is None])
        review_count = len([c for c in self.cards if self.is_due_for_review(c)])

        self.lbl_learn_count.config(text=f"To Learn: {learn_count} cards")
        self.lbl_review_count.config(text=f"To Review: {review_count} cards")

    def start_learn(self):
        self.mode = "learn"
        self.current_card = {}
        self.init_study_queue()
        if not self.study_queue:
            messagebox.showinfo("Info", "No new cards to learn!", parent=self.root)
            return
        self.start_game()

    def start_review(self):
        self.mode = "review"
        self.current_card = {}
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        self.study_queue = []
        for c in self.cards:
            nxt = c.get("next_review")
            if nxt and nxt <= today:
                self.study_queue.append(c)
            elif c.get("status") == "forgot" and not nxt:
                self.study_queue.append(c)

        print(f"Mode: {self.mode}, To study: {len(self.study_queue)}")
        
        if not self.study_queue:
            messagebox.showinfo("Info", "No cards to review today!\nPlease learn new cards or wait for next review.", parent=self.root)
            return
        self.start_game()

    def start_game(self):
        self.menu_frame.pack_forget()
        self.completion_frame.pack_forget()
        self.game_frame.pack(fill="both", expand=True)
        self.next_card()

    def init_study_queue(self):
        if self.mode == "learn":
            self.study_queue = [c for c in self.cards if c.get("status") is None]
        elif self.mode == "review":
            self.study_queue = [c for c in self.cards if self.is_due_for_review(c)]
        else:
            self.study_queue = []
        print(f"Mode: {self.mode}, To study: {len(self.study_queue)}")

    def load_data(self):
        if not os.path.exists(DATA_FILE):
             return []
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.cards, f, ensure_ascii=False, indent=4)

    def next_card(self):
        if self.mode == "learn" and self.current_card:
            self.current_card["status"] = "learning"
            self.current_card["level"] = 0
            self.current_card["last_review"] = datetime.now().strftime("%Y-%m-%d")
            self.current_card["next_review"] = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            
            self.save_data()
            if self.current_card in self.study_queue:
                self.study_queue.remove(self.current_card)

        self.btn_remember.pack_forget()
        self.btn_forgot.pack_forget()
        self.btn_next.pack(side="right", padx=20)
        self.btn_back_menu.pack(side="left", padx=20)

        if not self.study_queue:
            self.show_completion()
            return

        if len(self.study_queue) > 1 and self.current_card in self.study_queue:
             candidates = [c for c in self.study_queue if c != self.current_card]
             self.current_card = random.choice(candidates)
        else:
             self.current_card = random.choice(self.study_queue)
        
        self.is_flipped = False
        self.update_card_ui()

    def show_completion(self):
        self.game_frame.pack_forget()
        self.completion_frame.pack(fill="both", expand=True)

    def mark_remembered(self):
        if self.current_card:
            self.current_card["status"] = "remembered"
            self.current_card["last_review"] = datetime.now().strftime("%Y-%m-%d")
            
            level = self.current_card.get("level", 0)
            
            intervals = [3, 5, 7, 15]
            
            if level < len(intervals):
                days = intervals[level]
            else:
                days = 15
            
            self.current_card["next_review"] = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
            self.current_card["level"] = level + 1
            
            self.save_data()
            if self.current_card in self.study_queue:
                self.study_queue.remove(self.current_card)
            self.next_card()

    def mark_forgot(self):
        if self.current_card:
            self.current_card["status"] = "forgot"
            self.current_card["last_review"] = datetime.now().strftime("%Y-%m-%d")
            
            self.current_card["level"] = 0
            self.current_card["next_review"] = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            
            self.save_data()
            self.next_card()

    def flip_card(self, event=None):
        if not self.current_card:
            return
            
        self.is_flipped = not self.is_flipped
        self.update_card_ui()

        if self.is_flipped:
            if self.mode == "review":
                self.btn_next.pack_forget()
                self.btn_forgot.pack(side="right", padx=10)
                self.btn_remember.pack(side="right", padx=10)
        else:
            self.btn_remember.pack_forget()
            self.btn_forgot.pack_forget()
            self.btn_next.pack(side="right", padx=20)

    def update_card_ui(self):
        if self.is_flipped:
            self.card_canvas.itemconfig(self.card_text, text=self.current_card["answer"], fill="#2c3e50")
            self.card_canvas.configure(bg="#e8f6f3")
            self.header_label.config(text="✨ Answer")
        else:
            self.card_canvas.itemconfig(self.card_text, text=self.current_card["question"], fill="black")
            self.card_canvas.configure(bg="white")
            self.header_label.config(text="🤔 Question (" + ("Learn" if self.mode == "learn" else "Review") + ")")

    def add_card_window(self):
        add_win = tk.Toplevel(self.root)
        add_win.title("Add New Card")
        add_win.geometry("400x300")

        tk.Label(add_win, text="Question (Front):", font=("Microsoft YaHei", 10)).pack(pady=5)
        q_entry = tk.Entry(add_win, width=40, font=("Microsoft YaHei", 10))
        q_entry.pack(pady=5)
        q_entry.focus_set()

        tk.Label(add_win, text="Answer (Back):", font=("Microsoft YaHei", 10)).pack(pady=5)
        a_entry = tk.Entry(add_win, width=40, font=("Microsoft YaHei", 10))
        a_entry.pack(pady=5)

        def save_new():
            q = q_entry.get().strip()
            a = a_entry.get().strip()
            if q and a:
                new_card = {"question": q, "answer": a, "status": None}
                self.cards.append(new_card)
                self.save_data()
                if self.mode is None:
                     self.show_menu()
                
                messagebox.showinfo("Success", "Card added!", parent=add_win)
                add_win.destroy()
            else:
                messagebox.showwarning("Warning", "Question and Answer cannot be empty", parent=add_win)

        tk.Button(add_win, text="Save", command=save_new, bg="#ddffdd", width=15).pack(pady=20)

    def delete_card(self):
        """Delete current card"""
        if not self.current_card:
            return
            
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this card? This cannot be undone.", parent=self.root)
        if confirm:
            if self.current_card in self.cards:
                self.cards.remove(self.current_card)
            if self.current_card in self.study_queue:
                self.study_queue.remove(self.current_card)
            
            self.save_data()
            messagebox.showinfo("Success", "Card deleted", parent=self.root)
            self.next_card()

    def edit_card(self):
        if not self.current_card:
            return

        edit_win = tk.Toplevel(self.root)
        edit_win.title("Edit Card")
        edit_win.geometry("400x300")

        tk.Label(edit_win, text="Question (Front):", font=("Microsoft YaHei", 10)).pack(pady=5)
        q_entry = tk.Entry(edit_win, width=40, font=("Microsoft YaHei", 10))
        q_entry.pack(pady=5)
        q_entry.insert(0, self.current_card.get("question", ""))
        q_entry.focus_set()

        tk.Label(edit_win, text="Answer (Back):", font=("Microsoft YaHei", 10)).pack(pady=5)
        a_entry = tk.Entry(edit_win, width=40, font=("Microsoft YaHei", 10))
        a_entry.pack(pady=5)
        a_entry.insert(0, self.current_card.get("answer", ""))

        def save_edit():
            q = q_entry.get().strip()
            a = a_entry.get().strip()
            if q and a:
                self.current_card["question"] = q
                self.current_card["answer"] = a
                self.save_data()
                self.update_card_ui()
                messagebox.showinfo("Success", "Card updated!", parent=edit_win)
                edit_win.destroy()
            else:
                messagebox.showwarning("Warning", "Question and Answer cannot be empty", parent=edit_win)

        tk.Button(edit_win, text="Save Changes", command=save_edit, bg="#ddffdd", width=15).pack(pady=20)

    def is_due_for_review(self, card):
        status = card.get("status")
        if status == "forgot":
            return True
        
        next_review_str = card.get("next_review")
        if next_review_str:
            try:
                next_review_date = datetime.strptime(next_review_str, "%Y-%m-%d")
                if datetime.now() >= next_review_date: 
                    return True
                else:
                    return False 
            except ValueError:
                pass 
        
        last_review_str = card.get("last_review")
        if status == "remembered" and last_review_str:
            try:
                last_review_date = datetime.strptime(last_review_str, "%Y-%m-%d")
                if (datetime.now() - last_review_date) > timedelta(days=3):
                    return True
            except ValueError:
                pass
        
        return False

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()