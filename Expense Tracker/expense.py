import datetime
import sqlite3
from tkcalendar import DateEntry
from tkinter import *
import tkinter.messagebox as tb
import tkinter.ttk as ttk

# Functions
def list_all_expenses():
  global connector, table

  table.delete(*table.get_children())

  all_data = connector.execute('SELECT * FROM ExpenseTracker')
  data = all_data.fetchall()

  for values in data:
     table.insert('', END, values=values)

def clear_fields():
  global Desc, payee, amnt, MoP, date, table

  today_date = datetime.datetime.now().date()

  Desc.set('') ; payee.set('') ; amnt.set(0.0) ; MoP.set('Cash'), date.set_date(today_date)
  table.selection_remove(*table.selection())

def remove_expense():
  if not table.selection():
     tb.showerror('No record selected!', 'Please select a record to delete!')
     return

  current_selected_expense = table.item(table.focus())
  values_selected = current_selected_expense['values']

  surety = tb.askyesno('Are you sure?', f'Are you sure that you want to delete the record of {values_selected[2]}')

  if surety:
     connector.execute('DELETE FROM ExpenseTracker WHERE ID=%d' % values_selected[0])
     connector.commit()

     list_all_expenses()
     tb.showinfo('Record deleted successfully!', 'The record you wanted to delete has been deleted successfully')

def remove_all_expenses():
  surety = tb.askyesno('Are you sure?', 'Are you sure that you want to delete all the expense items from the database?', icon='warning')

  if surety:
     table.delete(*table.get_children())

     connector.execute('DELETE FROM ExpenseTracker')
     connector.commit()

     clear_fields()
     list_all_expenses()
     tb.showinfo('All Expenses deleted', 'All the expenses were successfully deleted')
  else:
     tb.showinfo('Ok then', 'The task was aborted and no expense was deleted!')

def add_another_expense():
  global date, payee, Desc, amnt, MoP
  global connector

  if not date.get() or not payee.get() or not Desc.get() or not amnt.get() or not MoP.get():
     tb.showerror('Fields empty!', "Please fill all the missing fields before pressing the add button!")
  else:
     connector.execute(
     'INSERT INTO ExpenseTracker (Date, Payee, Description, Amount, ModeOfPayment) VALUES (?, ?, ?, ?, ?)',
     (date.get_date(), payee.get(), Desc.get(), amnt.get(), MoP.get())
     )
     connector.commit()

     clear_fields()
     list_all_expenses()
     tb.showinfo('Expense added', 'The expense whose details you just entered has been added to the database')

def expense_to_words_before_adding():
  global date, Desc, amnt, payee, MoP

  if not date or not Desc or not amnt or not payee or not MoP:
     tb.showerror('Incomplete data', 'The data is incomplete, meaning fill all the fields first!')

  message = f'Your expense can be read like: \n"You paid {amnt.get()} to {payee.get()} for {Desc.get()} on {date.get_date()} via {MoP.get()}"'

  add_question = tb.askyesno('Read your record like: ', f'{message}\n\nShould I add it to the database?')

  if add_question:
     add_another_expense()
  else:
     tb.showinfo('Ok', 'Please take your time to add this record')

# Connecting to the Database
connector = sqlite3.connect("Expense Tracker.db")
cursor = connector.cursor()

connector.execute(
  'CREATE TABLE IF NOT EXISTS ExpenseTracker (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Date DATETIME, Payee TEXT, Description TEXT, Amount FLOAT, ModeOfPayment TEXT)'
)
connector.commit()

# Backgrounds and Fonts
dataentery_frame_bg = 'light blue'
buttons_frame_bg = 'tomato'
hlb_btn_bg = 'Indianred'

lbl_font = ('Georgia', 13)
entry_font = 'Times 13 bold'
btn_font = ('Gill Sans MT', 13)

# Initializing the GUI window
root = Tk()
root.title('DebEx')
root.geometry('1200x550')
root.resizable(0, 0)

Label(root, text='DebEx', font=('white', 21, 'bold'), bg=hlb_btn_bg).pack(side=TOP, fill=X)

# StringVar and DoubleVar variables
Desc = StringVar()
amnt = DoubleVar()
payee = StringVar()
MoP = StringVar(value='Cash')

# Frames
data_entry_frame = Frame(root, bg=dataentery_frame_bg)
data_entry_frame.place(x=0, y=35, relheight=0.95, relwidth=0.25)

buttons_frame = Frame(root, bg=buttons_frame_bg)
buttons_frame.place(relx=0.25, rely=0.063, relwidth=0.75, relheight=0.12)

tree_frame = Frame(root)
tree_frame.place(relx=0.25, rely=0.18, relwidth=0.75, relheight=0.8)

# Data Entry Frame
Label(data_entry_frame, text='Date (M/DD/YY) :', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=50)
date = DateEntry(data_entry_frame, date=datetime.datetime.now().date(), font=entry_font)
date.place(x=160, y=50)

Label(data_entry_frame, text='Payee\t             :', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=230)
Entry(data_entry_frame, font=entry_font, width=31, text=payee).place(x=10, y=260)

Label(data_entry_frame, text='Description           :', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=100)
Entry(data_entry_frame, font=entry_font, width=31, text=Desc).place(x=10, y=130)

Label(data_entry_frame, text='Amount\t             :', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=180)
Entry(data_entry_frame, font=entry_font, width=14, text=amnt).place(x=160, y=180)

Label(data_entry_frame, text='Mode of Payment:', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=310)
dd1 = OptionMenu(data_entry_frame, MoP, *['Cash', 'Cheque', 'Credit Card', 'Debit Card', 'Paytm', 'Google Pay', 'Razorpay'])
dd1.place(x=160, y=305)     ;     dd1.configure(width=10, font=entry_font)

Button(data_entry_frame, text='Add expense', command=add_another_expense, font=btn_font, width=30,
      bg=hlb_btn_bg).place(x=10, y=395)

# Buttons' Frame
Button(buttons_frame, text='Delete Expense', font=btn_font, width=25, bg=hlb_btn_bg, command=remove_expense).place(x=30, y=5)

Button(buttons_frame, text='Clear Fields in DataEntry Frame', font=btn_font, width=25, bg=hlb_btn_bg,
      command=clear_fields).place(x=335, y=5)

Button(buttons_frame, text='Delete All Expenses', font=btn_font, width=25, bg=hlb_btn_bg, command=remove_all_expenses).place(x=640, y=5)

# Treeview Frame
table = ttk.Treeview(tree_frame, selectmode=BROWSE, columns=('ID', 'Date', 'Payee', 'Description', 'Amount', 'Mode of Payment'))

X_Scroller = Scrollbar(table, orient=HORIZONTAL, command=table.xview)
Y_Scroller = Scrollbar(table, orient=VERTICAL, command=table.yview)
X_Scroller.pack(side=BOTTOM, fill=X)
Y_Scroller.pack(side=RIGHT, fill=Y)

table.config(yscrollcommand=Y_Scroller.set, xscrollcommand=X_Scroller.set)

table.heading('ID', text='S No.', anchor=CENTER)
table.heading('Date', text='Date', anchor=CENTER)
table.heading('Payee', text='Payee', anchor=CENTER)
table.heading('Description', text='Description', anchor=CENTER)
table.heading('Amount', text='Amount', anchor=CENTER)
table.heading('Mode of Payment', text='Mode of Payment', anchor=CENTER)

table.column('#0', width=0, stretch=NO)
table.column('#1', width=50, stretch=NO)
table.column('#2', width=95, stretch=NO)  # Date column
table.column('#3', width=150, stretch=NO)  # Payee column
table.column('#4', width=325, stretch=NO)  # Title column
table.column('#5', width=135, stretch=NO)  # Amount column
table.column('#6', width=125, stretch=NO)  # Mode of Payment column

table.place(relx=0, y=0, relheight=1, relwidth=1)

list_all_expenses()
# Finalizing the GUI window
root.update()
root.mainloop()
