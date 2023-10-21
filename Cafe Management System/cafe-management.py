from tkinter import *
import tkinter as tk
from datetime import datetime
from PIL import ImageTk, Image
from tkinter import messagebox

class cafe_management():

# coded by Manithj

        # ============== Total Bill Code =================

        def Total_Bill(self):
                self.tea_price = 10
                self.coffee_price = 20
                self.sandwitch_price = 50
                self.cake_price = 100
                self.burger_price = 50
                self.pizza_price = 150
                self.fries_price = 80
                self.pepsi_price = 80
                
                if self.tea_item.get() != "":
                        self.tea_cost = self.tea_price * int(self.tea_item.get())
                else:
                        self.tea_cost = 0
                if self.coffee_item.get() != "":
                        self.coffee_cost = self.coffee_price * int(self.coffee_item.get())
                else:
                        self.coffee_cost = 0
                if self.sandwitch_item.get() != "":
                                self.sandwitch_cost = self.sandwitch_price * int(self.sandwitch_item.get())
                else:
                        self.sandwitch_cost = 0
                if self.cake_item.get() != "":
                                self.cake_cost = self.cake_price * int(self.cake_item.get())
                else:
                        self.cake_cost = 0
                if self.burger_item.get() != "":
                                self.burger_cost = self.burger_price * int(self.burger_item.get())
                else:
                        self.burger_cost = 0
                if self.pizza_item.get() != "":
                                self.pizza_cost = self.pizza_price * int(self.pizza_item.get())
                else:
                        self.pizza_cost = 0
                if self.fries_item.get() != "":
                                self.fries_cost = self.fries_price * int(self.fries_item.get())
                else:
                        self.fries_cost = 0
                if self.pepsi_item.get() != "":
                                self.pepsi_cost = self.pepsi_price * int(self.pepsi_item.get())
                else:
                        self.pepsi_cost = 0


                self.Total_Bill = self.pepsi_cost + self.fries_cost + self.pizza_cost +  self.burger_cost + self.cake_cost + self.sandwitch_cost + self.coffee_cost + self.tea_cost 
                
                if self.items_cost != "":
                        self.items_cost.delete(0,END)
                        self.items_cost.insert(END,self.Total_Bill)
                else:
                        self.items_cost.insert(END,self.Total_Bill)
                if self.service_cost != "":
                        self.service_cost.delete(0,END)
                        self.service_cost.insert(END,10.0)
                else:
                        self.service_cost.insert(END,10.0)
                if self.sub_cost != "":
                        self.sub_cost.delete(0,END)
                        self.sub_cost.insert(END,int(self.items_cost.get()) + float(self.service_cost.get()))
                else:
                        self.sub_cost.insert(END,int(self.items_cost.get()) + float(self.service_cost.get()))
                if self.paid_tax != "":
                        self.paid_tax.delete(0,END)
                        self.paid_tax.insert(END,float(self.sub_cost.get())*8/100)
                else:
                        self.paid_tax.insert(END,float(self.sub_cost.get())*8/100)

                if self.total_bill != "":
                        self.total_bill.delete(0,END)
                        self.total_bill.insert(END,float(self.sub_cost.get())+float(self.paid_tax.get()))
                else:
                        self.total_bill.insert(END,float(self.sub_cost.get())+float(self.paid_tax.get()))
                







        # ===== Calculator code ================

        def nine(self):
                if 'error' in self.result.get() or '=' in self.result.get():
                        self.result.delete(0,"end")
                        self.result.insert("end","9")
                else:
                        self.result.insert("end","9")
                        
                

        def eight(self):
                if 'error' in self.result.get() or '=' in self.result.get():
                        self.result.delete(0,"end")
                        self.result.insert("end","8")
                else:
                        self.result.insert("end","8")

        def seven(self):
                if 'error' in self.result.get() or '=' in self.result.get():
                        self.result.delete(0,"end")
                        self.result.insert("end","7")
                else:
                        self.result.insert("end","7")

        def six(self):
                if 'error' in self.result.get() or '=' in self.result.get():
                        self.result.delete(0,"end")
                        self.result.insert("end","6")
                else:
                        self.result.insert("end","6")

        def five(self):
                if 'error' in self.result.get() or '=' in self.result.get():
                        self.result.delete(0,"end")
                        self.result.insert("end","5")
                else:
                        self.result.insert("end","5")

        def four(self):
                if 'error' in self.result.get() or '=' in self.result.get():
                        self.result.delete(0,"end")
                        self.result.insert("end","4")
                else:
                        self.result.insert("end","4")

        def three(self):
                if 'error' in self.result.get() or '=' in self.result.get():
                        self.result.delete(0,"end")
                        self.result.insert("end","3")
                else:
                        self.result.insert("end","3")

        def two(self):
                if 'error' in self.result.get() or '=' in self.result.get():
                        self.result.delete(0,"end")
                        self.result.insert("end","2")
                else:
                        self.result.insert("end","2")

        def one(self):
                if 'error' in self.result.get() or '=' in self.result.get():
                        self.result.delete(0,"end")
                        self.result.insert("end","1")
                else:
                        self.result.insert("end","1")

        def zero(self):
                if 'error' in self.result.get() or '=' in self.result.get():
                        self.result.delete(0,"end")
                        self.result.insert("end","0")
                else:
                        self.result.insert("end","0")

        def plus(self):
                if 'error' in self.result.get() or '=' in self.result.get():
                        self.result.delete(0,"end")
                        self.result.insert("end","+")
                else:
                        self.result.insert("end","+")

        def minus(self):
                if 'error' in self.result.get() or '=' in self.result.get():
                        self.result.delete(0,"end")
                        self.result.insert("end","-")
                else:
                        self.result.insert("end","-")

        def mul(self):
                if 'error' in self.result.get() or '=' in self.result.get():
                        self.result.delete(0,"end")
                        self.result.insert("end","*")
                else:
                        self.result.insert("end","*")

        def divide(self):
                if 'error' in self.result.get() or '=' in self.result.get():
                        self.result.delete(0,"end")
                        self.result.insert("end","/")
                else:
                        self.result.insert("end","/")

        def equal(self):


                if self.result.get() == "":
                        self.result.insert("end","error")
                elif self.result.get()[0] == "0" or self.result.get()[0] == "+" or self.result.get()[0] == "*" or self.result.get()[0] == "/":
                        self.result.delete(0,"end")
                        self.result.insert("end","error")
                elif 'error' in self.result.get() or '=' in self.result.get():
                        self.result.delete(0,"end")


                else:
                        self.res = self.result.get()
                        self.res = eval(self.res)
                        self.result.insert("end"," = ")
                        self.result.insert("end",self.res)

        # =================== Clear Fields =============== 
        def clear(self):
                self.result.delete(0,"end")
        def Clear(self):
                self.tea_item.delete(0,"end")
                self.coffee_item.delete(0,"end")
                self.sandwitch_item.delete(0,"end")
                self.burger_item.delete(0,"end")
                self.cake_item.delete(0,"end")
                self.fries_item.delete(0,"end")
                self.pizza_item.delete(0,"end")
                self.pepsi_item.delete(0,"end")
                self.items_cost.delete(0,"end")
                self.service_cost.delete(0,"end")
                self.sub_cost.delete(0,"end")
                self.paid_tax.delete(0,"end")
                self.total_bill.delete(0,"end")
        
                
        # ==== Exit button code =================
        def Quit(self):
                self.message = messagebox.askquestion('Exit',"Do you want to exit the application")
                if self.message == "yes":
                        self.root.destroy()
                else:
                        "return"

                #========== end ========================


        def __init__(self):
                self.root = tk.Tk()
                self.root.geometry('500x300')
                self.root.title("Cafe Management System")
                self.root.maxsize(500,300)
                self.root.minsize(500,300)
                self.root['bg'] = "white"

                self.heading = Label(self.root,text="Cafe Management System",font=('verdana',20,'bold'),fg="#248aa2",bg="white")
                self.heading.place(x=60,y=5)
                
                self.style1 = Label(self.root,bg="#248aa2",height=1,width=17)
                self.style1.place(x=0,y=50)
                self.style2 = Label(self.root,bg="#248aa2",height=1,width=30)
                self.style2.place(x=380,y=50)
                self.date = Label(self.root,text=datetime.now(),font=('verdana',10,'bold'),bg="white")
                self.date.place(x=140,y=50)

                self.cafe_icon = ImageTk.PhotoImage(Image.open('cafe.png'))
                self.logo = Label(self.root,image=self.cafe_icon,bg="white")
                self.logo.place(x=230,y=70)

                # ================== Items ===================
                self.frame1 = LabelFrame(self.root,text="Cafe Items",width=150,height=200,font=('verdana',10,'bold'),borderwidth=3,relief=RIDGE,highlightthickness=4,bg="white",highlightcolor="white",highlightbackground="white",fg="#248aa2")
                self.frame1.place(x=30,y=90)
                
                self.tea = Label(self.frame1,text="Tea",font=('verdana',10,'bold'),bg="white")
                self.tea.place(x=3,y=1)
                self.tea_item = Entry(self.frame1,width=7,borderwidth=4,relief=SUNKEN,bg="#248aa2")
                self.tea_item.place(y=1,x=85)

                self.coffee = Label(self.frame1,text="Coffee",font=('verdana',10,'bold'),bg="white")
                self.coffee.place(x=3,y=20)
                self.coffee_item = Entry(self.frame1,width=7,borderwidth=4,relief=SUNKEN,bg="#248aa2")
                self.coffee_item.place(y=20,x=85)

                self.sandwitch = Label(self.frame1,text="Sandwitch",font=('verdana',10,'bold'),bg="white")
                self.sandwitch.place(x=3,y=40)
                self.sandwitch_item = Entry(self.frame1,width=7,borderwidth=4,relief=SUNKEN,bg="#248aa2")
                self.sandwitch_item.place(y=40,x=85)

                self.cake = Label(self.frame1,text="Cake",font=('verdana',10,'bold'),bg="white")
                self.cake.place(x=3,y=60)
                self.cake_item = Entry(self.frame1,width=7,borderwidth=4,relief=SUNKEN,bg="#248aa2")
                self.cake_item.place(y=60,x=85)

                self.burger = Label(self.frame1,text="Burger",font=('verdana',10,'bold'),bg="white")
                self.burger.place(x=3,y=80)
                self.burger_item = Entry(self.frame1,width=7,borderwidth=4,relief=SUNKEN,bg="#248aa2")
                self.burger_item.place(y=80,x=85)

                self.pizza = Label(self.frame1,text="Pizza",font=('verdana',10,'bold'),bg="white")
                self.pizza.place(x=3,y=100)
                self.pizza_item = Entry(self.frame1,width=7,borderwidth=4,relief=SUNKEN,bg="#248aa2")
                self.pizza_item.place(y=100,x=85)

                self.fries = Label(self.frame1,text="Fries",font=('verdana',10,'bold'),bg="white")
                self.fries.place(x=3,y=120)
                self.fries_item = Entry(self.frame1,width=7,borderwidth=4,relief=SUNKEN,bg="#248aa2")
                self.fries_item.place(y=120,x=85)

                self.pepsi = Label(self.frame1,text="Pepsi",font=('verdana',10,'bold'),bg="white")
                self.pepsi.place(x=3,y=140)
                self.pepsi_item = Entry(self.frame1,width=7,borderwidth=4,relief=SUNKEN,bg="#248aa2")
                self.pepsi_item.place(y=140,x=85)

                # ============ Items Bill =================

                self.frame2 = LabelFrame(self.root,text="Cafe Items Bills",width=180,height=160,font=('verdana',10,'bold'),borderwidth=3,relief=RIDGE,highlightthickness=4,bg="white",highlightcolor="white",highlightbackground="white",fg="#248aa2")
                self.frame2.place(x=180,y=120)

                self.item_cost_lb = Label(self.frame2,text="Items Cost",font=('verdana',10,'bold'),bg="white")
                self.item_cost_lb.place(x=3,y=1)
                self.items_cost = Entry(self.frame2,width=9,borderwidth=4,relief=SUNKEN,bg="#248aa2")
                self.items_cost.place(y=1,x=100)

                self.service_cost_lb = Label(self.frame2,text="Service Cost",font=('verdana',10,'bold'),bg="white")
                self.service_cost_lb.place(x=3,y=20)
                self.service_cost = Entry(self.frame2,width=9,borderwidth=4,relief=SUNKEN,bg="#248aa2")
                self.service_cost.place(y=20,x=100)

                self.sub_cost_lb = Label(self.frame2,text="Sub Cost",font=('verdana',10,'bold'),bg="white")
                self.sub_cost_lb.place(x=3,y=40)
                self.sub_cost = Entry(self.frame2,width=9,borderwidth=4,relief=SUNKEN,bg="#248aa2")
                self.sub_cost.place(y=40,x=100)

                self.paid_tax_lb = Label(self.frame2,text="Paid Tax",font=('verdana',10,'bold'),bg="white")
                self.paid_tax_lb.place(x=3,y=80)
                self.paid_tax = Entry(self.frame2,width=9,borderwidth=4,relief=SUNKEN,bg="#248aa2")
                self.paid_tax.place(y=80,x=100)

                self.total_bill_lb = Label(self.frame2,text="Total Bill",font=('verdana',10,'bold'),bg="white")
                self.total_bill_lb.place(x=3,y=100)
                self.total_bill = Entry(self.frame2,width=9,borderwidth=4,relief=SUNKEN,bg="#248aa2")
                self.total_bill.place(y=100,x=100)

                # ================== Calculator ============
                self.frame3 = LabelFrame(self.root,text="Calculator",font=('verdana',10,'bold'),fg="#248aa2",bg="white",highlightbackground="white",width=135,height=150,borderwidth=3,relief=RIDGE)
                self.frame3.place(x=360,y=90)

                self.result = Entry(self.frame3,width=19,relief=SUNKEN,borderwidth=3)
                self.result.place(x=2,y=0)

                self.nine = Button(self.frame3,text="9",padx=6,relief=RAISED,borderwidth=2,font=('verdana',10,'bold'),bg='#248aa2',fg="white",command=self.nine)
                self.nine.place(x=0,y=24)
                self.eight = Button(self.frame3,text="8",padx=6,relief=RAISED,borderwidth=2,font=('verdana',10,'bold'),bg='#248aa2',fg="white",command=self.eight)
                self.eight.place(x=32,y=24)
                self.seven = Button(self.frame3,text="7",padx=6,relief=RAISED,borderwidth=2,font=('verdana',10,'bold'),bg='#248aa2',fg="white",command=self.seven)
                self.seven.place(x=64,y=24)
                self.plus = Button(self.frame3,text="+",padx=6,relief=RAISED,borderwidth=2,font=('verdana',10,'bold'),bg='white',fg="black",command=self.plus)
                self.plus.place(x=96,y=24)


                self.six = Button(self.frame3,text="6",padx=6,relief=RAISED,borderwidth=2,font=('verdana',10,'bold'),bg='#248aa2',fg="white",command=self.six)
                self.six.place(x=0,y=50)
                self.five = Button(self.frame3,text="5",padx=6,relief=RAISED,borderwidth=2,font=('verdana',10,'bold'),bg='#248aa2',fg="white",command=self.five)
                self.five.place(x=32,y=50)
                self.four = Button(self.frame3,text="4",padx=6,relief=RAISED,borderwidth=2,font=('verdana',10,'bold'),bg='#248aa2',fg="white",command=self.four)
                self.four.place(x=64,y=50)
                self.minus = Button(self.frame3,text="-",padx=8,relief=RAISED,borderwidth=2,font=('verdana',10,'bold'),bg='white',fg="black",command=self.minus)
                self.minus.place(x=96,y=50)

                self.three = Button(self.frame3,text="3",padx=6,relief=RAISED,borderwidth=2,font=('verdana',10,'bold'),bg='#248aa2',fg="white",command=self.three)
                self.three.place(x=0,y=76)
                self.two = Button(self.frame3,text="2",padx=6,relief=RAISED,borderwidth=2,font=('verdana',10,'bold'),bg='#248aa2',fg="white",command=self.two)
                self.two.place(x=32,y=76)
                self.one = Button(self.frame3,text="1",padx=6,relief=RAISED,borderwidth=2,font=('verdana',10,'bold'),bg='#248aa2',fg="white",command=self.one)
                self.one.place(x=64,y=76)
                self.multiply = Button(self.frame3,text="*",padx=7,relief=RAISED,borderwidth=2,font=('verdana',10,'bold'),bg='white',fg="black",command=self.mul)
                self.multiply.place(x=96,y=76)

                self.zero = Button(self.frame3,text="0",padx=6,relief=RAISED,borderwidth=2,font=('verdana',10,'bold'),bg='#248aa2',fg="white",command=self.zero)
                self.zero.place(x=0,y=102)
                self.clear = Button(self.frame3,text="C",padx=6,relief=RAISED,borderwidth=2,font=('verdana',10,'bold'),bg='#248aa2',fg="white",command=self.clear)
                self.clear.place(x=32,y=102)
                self.equal = Button(self.frame3,text="=",padx=6,relief=RAISED,borderwidth=2,font=('verdana',10,'bold'),bg='#248aa2',fg="white",command=self.equal)
                self.equal.place(x=64,y=102)
                self.divide = Button(self.frame3,text="/",padx=7,relief=RAISED,borderwidth=2,font=('verdana',10,'bold'),bg='white',fg="black",command=self.divide)
                self.divide.place(x=96,y=102)

                self.Total_Bills_btn = Button(self.root,text="Total",relief=RAISED,borderwidth=2,font=('verdana',10,'bold'),bg='#248aa2',fg="white",command=self.Total_Bill)
                self.Total_Bills_btn.place(x=360,y=245)
                
                self.Clear_btn = Button(self.root,text="Clear",relief=RAISED,borderwidth=2,font=('verdana',10,'bold'),bg='#248aa2',fg="white",command=self.Clear)
                self.Clear_btn.place(x=410,y=245)
        
                self.icon = ImageTk.PhotoImage(Image.open('false.png'))
                self.Quit_btn = Button(self.root,image=self.icon,relief=RAISED,borderwidth=2,font=('verdana',10,'bold'),bg='#248aa2',fg="white",padx=5,command=self.Quit)
                self.Quit_btn.place(x=463,y=245)

                self.root.mainloop()


if __name__ == '__main__':
            cafe_management()
    


