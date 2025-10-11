# ======== A cleaned-up and working version of Total_Bill(), and a checklist of improvements and missing elements: =======

# Key Fixes and Recommendations:
# Use try...except instead of checking if get() is an empty string.
# Avoid assigning self.Total_Bill as both a method and a variable (naming conflict).
# Combine repetitive cost calculations using a loop or helper function.
# Ensure all UI elements (self.tea_item, self.items_cost, etc.) are defined before calling Total_Bill().


def Total_Bill(self):
    # Item prices
    prices = {
        "tea": 10,
        "coffee": 20,
        "sandwich": 50,
        "cake": 100,
        "burger": 50,
        "pizza": 150,
        "fries": 80,
        "pepsi": 80
    }

    # Calculate individual item costs
    try:
        self.tea_cost = prices["tea"] * int(self.tea_item.get() or 0)
        self.coffee_cost = prices["coffee"] * int(self.coffee_item.get() or 0)
        self.sandwich_cost = prices["sandwich"] * int(self.sandwitch_item.get() or 0)
        self.cake_cost = prices["cake"] * int(self.cake_item.get() or 0)
        self.burger_cost = prices["burger"] * int(self.burger_item.get() or 0)
        self.pizza_cost = prices["pizza"] * int(self.pizza_item.get() or 0)
        self.fries_cost = prices["fries"] * int(self.fries_item.get() or 0)
        self.pepsi_cost = prices["pepsi"] * int(self.pepsi_item.get() or 0)

        total_items_cost = (
            self.tea_cost + self.coffee_cost + self.sandwich_cost +
            self.cake_cost + self.burger_cost + self.pizza_cost +
            self.fries_cost + self.pepsi_cost
        )

        service_charge = 10.0
        subtotal = total_items_cost + service_charge
        tax = subtotal * 0.08
        total = subtotal + tax

        # Update GUI fields
        self.items_cost.delete(0, END)
        self.items_cost.insert(END, total_items_cost)

        self.service_cost.delete(0, END)
        self.service_cost.insert(END, service_charge)

        self.sub_cost.delete(0, END)
        self.sub_cost.insert(END, subtotal)

        self.paid_tax.delete(0, END)
        self.paid_tax.insert(END, round(tax, 2))

        self.total_bill.delete(0, END)
        self.total_bill.insert(END, round(total, 2))

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")
