from tkinter import *
from tkinter import messagebox, simpledialog

"""
Author:  Jack Frank
Date written: 07/15/2024
Assignment:   Module7 Final Project, "Goody Burger Interprises"
Short Desc:   This is the end result of 
the GUI, used for creating a simulation
of ordering a menu from a fake restaurant
called "Goody Burger Interprises."
"""

root = Tk()
root.title("Goody Burger Interprises: Food For Thought")
order_summary_window = None
remaining_money = 0
order_summary_text = ""  # Initialize global variable for order summary text

# Display order summary with image
def show_order_summary_with_image(selected_items, total_cost, coupons, discount_percent, discounted_cost, money_leftover):
    global order_summary_window, order_summary_text
    if order_summary_window and order_summary_window.winfo_exists():
        order_summary_window.destroy()

    order_summary_window = Toplevel(root)
    order_summary_window.title("Order Summary")

    # Create a canvas for the image
    canvas = Canvas(order_summary_window, width=400, height=300)
    canvas.pack()

    # Load and display the image
    try:
        image_path = "money.gif"  # Path to your money image
        money_image = PhotoImage(file=image_path)
        canvas.create_image(200, 150, anchor=CENTER, image=money_image)
        canvas.image = money_image
    except FileNotFoundError:
        messagebox.showerror("Error", f"Image file '{image_path}' not found.")

    # Create a frame for the text summary
    summary_frame = Frame(order_summary_window)
    summary_frame.pack(padx=10, pady=10)
    
    # Display the order summary
    order_summary_text = (
        f"You ordered:\n\n" + "\n".join(selected_items) +
        f"\n\nTotal Cost: ${total_cost:.2f}\n" +
        f"Discount Applied: {coupons} coupons ({discount_percent * 100}%)\n" +
        f"Final Cost: ${discounted_cost:.2f}\n" +
        f"Money Leftover: ${money_leftover:.2f}"
    )
    
    # Change the font of the summary text
    order_summary_label = Label(
        summary_frame, 
        text=order_summary_text,
        padx=20, pady=20,
        font=("Helvetica", 12)
    )
    order_summary_label.pack()

    # Header for the order summary
    money_label = Label(
        summary_frame,
        text="Order Summary",
        font=("Algerian", 18, "bold"),
        padx=20, pady=10
    )
    money_label.pack()

    # Button to close the window
    close_button = Button(
        order_summary_window, 
        text="Close", 
        command=order_summary_window.destroy,
        font=("Helvetica", 10)
    )
    close_button.pack(pady=10)

# Menu items with prices
menu_items = {
    "Burger": 5.99,
    "Fries": 2.49,
    "Soda": 1.99,
    "Salad": 4.99,
    "GUI Burger": 12.99,
    "Chicken Sandwich": 5.99,
    "Chocolate Shake": 3.99,
    "Vanilla Shake": 3.99,
    "Soft Drink": 1.99,
    "Soft-Served Sundae": 4.99
}

def ViewMenu():
    menu_window = Toplevel(root)
    menu_window.title("Menu")

    canvas = Canvas(menu_window, width=400, height=300)
    canvas.pack()

    try:
        image_path = "Menu Item Options.gif"  # Path to your image
        food_image = PhotoImage(file=image_path)
        canvas.create_image(200, 150, anchor=CENTER, image=food_image)
        canvas.image = food_image
    except FileNotFoundError:
        messagebox.showerror("Error", f"Image file '{image_path}' not found.")

    # Display menu items with prices
    menu_label = Label(menu_window, text="Menu", font=("Algerian", 24, "bold"), padx=20, pady=20)
    menu_label.pack()

    for item, price in menu_items.items():
        item_label = Label(menu_window, text=f"{item}: ${price:.2f}", font=("Helvetica", 16))
        item_label.pack()

    backButton = Button(menu_window, text="Go back?", command=menu_window.destroy)
    backButton.pack()

def submit_inputs():
    global remaining_money
    try:
        money = float(money_entry.get())
        coupons = int(coupons_entry.get())

        if money < 0 or coupons < 0:
            raise ValueError("Please enter valid amounts.")
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return

    remaining_money = money  # Initialize remaining money
    input_dialog.destroy()  # Close the input dialog

    # Process order with the entered money and coupons
    OrderUp(coupons)

def OrderUp(coupons):
    global remaining_money

    selected_items = []

    while True:
        user_choice = simpledialog.askstring("Order Items", "Enter item number to add to order (press Cancel to finish):")

        if user_choice is None:
            break

        try:
            item_number = int(user_choice)
            if 1 <= item_number <= len(menu_items):
                items = list(menu_items.keys())  # Extracting keys (items) from menu_items dictionary
                selected_items.append(items[item_number - 1])
            else:
                messagebox.showinfo("Invalid Selection", f"Please enter a number between 1 and {len(menu_items)}.")
        except ValueError:
            messagebox.showinfo("Invalid Input", "Please enter a valid number.")

    if selected_items:
        total_cost = sum([menu_items[item] for item in selected_items])
        if total_cost > remaining_money:
            # If funds are insufficient, show an error and restart the ordering process
            messagebox.showerror("Insufficient Funds", "You do not have enough money to complete this order. Please try again.")
            OrderUp(coupons)  # Restart the order process with the current coupons
            return  # Exit the current function to prevent further processing

        # Calculate discount based on coupons
        discount_percent = coupons * 0.05
        discounted_cost = total_cost * (1 - discount_percent)
        remaining_money -= discounted_cost  # Update remaining money

        # Show order summary and money image
        show_order_summary_with_image(selected_items, total_cost, coupons, discount_percent, discounted_cost, remaining_money)

        answer = messagebox.askyesno("Continue Ordering", "Do you want to place another order?")
        if answer:
            messagebox.showinfo("Continue Ordering", f"You have ${remaining_money:.2f} remaining.")
            OrderUp(coupons)  # Restart the ordering process with the remaining money and same coupons
        else:
            Exit()  # Close the application with thank you message

def Exit():
    global order_summary_text
    messagebox.showinfo("Thank you for ordering!", "Thank you for ordering at Goody Burger Interprises, where we send good input your way!")
    if order_summary_text:
        print(order_summary_text)  # Print the order summary text
    root.destroy()

# Create input dialog for money and coupons
def input_dialog():
    global money_entry, coupons_entry, input_dialog

    input_dialog = Toplevel(root)
    input_dialog.title("Input Money and Coupons")

    Label(input_dialog, text="Enter amount of money available:").pack(padx=10, pady=5)
    money_entry = Entry(input_dialog)
    money_entry.pack(padx=10, pady=5)

    Label(input_dialog, text="Enter number of coupons:").pack(padx=10, pady=5)
    coupons_entry = Entry(input_dialog)
    coupons_entry.pack(padx=10, pady=5)

    Button(input_dialog, text="Submit", command=submit_inputs).pack(padx=10, pady=10)

# Labels and Buttons
myLabel1 = Label(root, text="Welcome to Goody Burger Interprises")
myLabel2 = Label(root, text="Would you like to review the menu?")
myLabel3 = Label(root, text="...Or would you like to leave?")

myButton1 = Button(root, text="View Menu", command=ViewMenu)
myButton2 = Button(root, text="Place Order", command=input_dialog)  # Opens input dialog
myButton3 = Button(root, text="Exit", command=Exit)

# Grid layout
myLabel1.grid(row=0, column=0, columnspan=3, pady=15, sticky='nsew')
myLabel2.grid(row=1, column=0, columnspan=3, pady=15, sticky='nsew')
myLabel3.grid(row=2, column=0, columnspan=3, pady=15, sticky='nsew')
myButton1.grid(row=3, column=0, padx=20, pady=15, sticky='nsew')
myButton2.grid(row=3, column=1, padx=20, pady=15, sticky='nsew')
myButton3.grid(row=3, column=2, padx=20, pady=15, sticky='nsew')

# Configure grid to center
for row in range(4):
    root.grid_rowconfigure(row, weight=1)
for col in range(3):
    root.grid_columnconfigure(col, weight=1)

root.mainloop()
