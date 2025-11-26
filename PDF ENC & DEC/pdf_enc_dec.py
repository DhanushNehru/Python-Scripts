# PDF Encrypter/Decrypter Application
# Made By Soriful Islam Sk
# Requires: pip install pypdf cryptography
# -------------------------------------------------------------------

import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfReader, PdfWriter
import os

# --- CORE ENCRYPTION/DECRYPTION LOGIC ---

def encrypt_pdf_file(input_path, output_path, user_password, owner_password):
    """Encrypts a PDF file using AES-256 and sets permissions."""
    try:
        reader = PdfReader(input_path)
        # Clone pages from reader to a new writer object
        writer = PdfWriter(clone_from=reader) 
        
        # Set AES-256 encryption and restrict user permissions
        writer.encrypt(
            user_password=user_password,
            owner_password=owner_password,
            permissions_flag=0xFFC0, # Common flag to restrict editing/copying for the user
            algorithm="AES-256"
        )
        
        with open(output_path, "wb") as output_file:
            writer.write(output_file)
            
        return True, f"Encrypted and saved as:\n{output_path}"
    except Exception as e:
        return False, f"Encryption Error: {e}"

def decrypt_pdf_file(input_path, output_path, user_password, owner_password):
    """
    Decrypts a password-protected PDF file by attempting the user_password 
    first, and then falling back to the owner_password.
    """
    try:
        reader = PdfReader(input_path)
        
        if not reader.is_encrypted:
            # If the file isn't encrypted, just save a copy and inform the user.
            writer = PdfWriter(clone_from=reader)
            with open(output_path, "wb") as output_file:
                writer.write(output_file)
            return True, f"File was not encrypted. Saved copy as:\n{output_path}"

        # 1. ATTEMPT DECRYPTION WITH USER PASSWORD
        result = reader.decrypt(user_password)
        
        if result not in (1, 0): # 1 and 0 indicate successful decryption
            # 2. FALLBACK: ATTEMPT DECRYPTION WITH OWNER PASSWORD
            result = reader.decrypt(owner_password)
        
        # 3. CHECK FINAL DECRYPTION STATUS
        if result not in (1, 0):
            return False, "Decryption Error: Neither the User nor the Owner password worked."

        # Decryption was successful (either password worked)
        writer = PdfWriter(clone_from=reader)
        
        with open(output_path, "wb") as output_file:
            writer.write(output_file)
            
        return True, f"Decrypted and saved as:\n{output_path}"

    except Exception as e:
        return False, f"Decryption Error: {e}"

# --- GUI APPLICATION CLASS ---

class PDFSecurityApp:
    def __init__(self, master):
        self.master = master
        master.title("PDF Encrypter/Decrypter")
        # Increased height slightly to accommodate the new label
        master.geometry("450x330") 
        
        self.input_file_path = tk.StringVar()
        self.user_pass = tk.StringVar()
        self.owner_pass = tk.StringVar()

        # 1. File Selection Section
        tk.Label(master, text="Select PDF File:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.file_entry = tk.Entry(master, textvariable=self.input_file_path, width=40)
        self.file_entry.grid(row=0, column=1, padx=5, pady=10)
        tk.Button(master, text="Browse", command=self.browse_file).grid(row=0, column=2, padx=5, pady=10)
        
        # 2. Password Entry Section (User/Open Password)
        tk.Label(master, text="User/Open Password:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(master, textvariable=self.user_pass, show="*", width=30).grid(row=1, column=1, padx=5, pady=5)

        # 3. Owner/Admin Password 
        tk.Label(master, text="Owner/Admin Password:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(master, textvariable=self.owner_pass, show="*", width=30).grid(row=2, column=1, padx=5, pady=5)
        
        # 4. Action Buttons Section
        button_frame = tk.Frame(master)
        button_frame.grid(row=3, column=0, columnspan=3, pady=20)
        
        tk.Button(button_frame, text="🔒 ENCRYPT PDF", command=self.handle_encrypt, 
                  bg="lightblue", padx=10, pady=5).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="🔓 DECRYPT PDF", command=self.handle_decrypt, 
                  bg="lightgreen", padx=10, pady=5).pack(side=tk.LEFT, padx=10)

        # 5. Author Credit Label
        tk.Label(
            master, 
            text="Made By Soriful Islam Sk", 
            fg="gray", 
            font=("Arial", 9, "italic")
        ).grid(row=4, column=0, columnspan=3, pady=(10, 5))

    def browse_file(self):
        """Opens a dialog to select the input PDF file."""
        file_path = filedialog.askopenfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file_path:
            self.input_file_path.set(file_path)

    def get_output_path(self, operation):
        """Generates the output file path based on the operation."""
        input_path = self.input_file_path.get()
        if not input_path:
            return None
        
        base, ext = os.path.splitext(input_path)
        default_output = f"{base}_{operation}{ext}"
        
        return filedialog.asksaveasfilename(
            defaultextension=ext,
            initialfile=default_output,
            filetypes=[("PDF files", "*.pdf")]
        )

    def handle_encrypt(self):
        """Handles the Encrypt button click."""
        input_path = self.input_file_path.get()
        user_p = self.user_pass.get()
        owner_p = self.owner_pass.get()
        
        if not input_path or not user_p:
            messagebox.showerror("Input Error", "Please select a file and enter a User Password.")
            return

        # Use user password as owner password if owner field is left empty
        if not owner_p:
            owner_p = user_p 

        output_path = self.get_output_path("encrypted")
        if not output_path:
            return

        success, message = encrypt_pdf_file(input_path, output_path, user_p, owner_p)
        
        if success:
            messagebox.showinfo("Success", f"Encryption Complete! {message}")
        else:
            messagebox.showerror("Error", message)

    def handle_decrypt(self):
        """Handles the Decrypt button click by trying both passwords."""
        input_path = self.input_file_path.get()
        user_p = self.user_pass.get()
        owner_p = self.owner_pass.get()
        
        # Check that at least one password is provided for decryption attempt
        if not input_path or (not user_p and not owner_p):
            messagebox.showerror(
                "Input Error", 
                "Please select a file and enter at least one password (User or Owner) for decryption."
            )
            return

        output_path = self.get_output_path("decrypted")
        if not output_path:
            return

        # Pass both entered passwords for sequential trial in the decryption function
        success, message = decrypt_pdf_file(input_path, output_path, user_p, owner_p)

        if success:
            messagebox.showinfo("Success", f"Decryption Complete! {message}")
        else:
            messagebox.showerror("Error", message)


# --- RUN THE APPLICATION ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PDFSecurityApp(root)
    root.mainloop()