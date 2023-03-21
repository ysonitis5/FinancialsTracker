import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
import csv
import os
import datetime
import random



#functions


#right side buttons
def add_investment():
    name = simpledialog.askstring("Add Investment", "Enter Investment Name:")
    investment_type = simpledialog.askstring("Add Investment", "Enter Investment Type:")
    amount = simpledialog.askfloat("Add Investment", "Enter Investment Amount:")

    if name and investment_type and amount:
        with open("investments.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([name, investment_type, amount])
        # Update the chart data and redraw the chart
        data["Net Worth"] += amount
        update_chart()

def add_debt():
    name = simpledialog.askstring("Add Debt", "Enter Debt Name:")
    debt_type = simpledialog.askstring("Add Debt", "Enter Debt Type:")
    amount = simpledialog.askfloat("Add Debt", "Enter Debt Amount:")

    if name and debt_type and amount:
        with open("debt.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([name, debt_type, amount])
        # Update the chart data and redraw the chart
        data["Debt"] += amount
        update_chart()

def add_payment():
    name = simpledialog.askstring("Add Payment", "Enter Payment Name:")
    payment_type = simpledialog.askstring("Add Payment", "Enter Payment Type:")
    amount = simpledialog.askfloat("Add Payment", "Enter Payment Amount:")
    due_date = simpledialog.askstring("Add Payment", "Enter Payment Due Date (MM/DD/YYYY):")

    if name and payment_type and amount and due_date:
        with open("payments.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([name, payment_type, amount, due_date])
        # Update the upcoming payments list
        upcoming_payments_list.append({"Name": name, "Type": payment_type, "Amount": amount, "Due Date": due_date})
        update_upcoming_payments()

def add_income():
    name = simpledialog.askstring("Add Income", "Enter Income Name:")
    income_type = simpledialog.askstring("Add Income", "Enter Income Type:")
    amount = simpledialog.askfloat("Add Income", "Enter Income Amount:")
    date_received = simpledialog.askstring("Add Income", "Enter Income Date Received (MM/DD/YYYY):")

    if name and income_type and amount and date_received:
        with open("income.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([name, income_type, amount, date_received])
        # Update the chart data and redraw the chart
        data["Net Worth"] += amount
        update_chart()

#charts
def update_chart():
    ax.clear()
    for name, values in data.items():
        ax.plot(range(len(values)), values, label=name)
    ax.set_ylim(0, max(max(data["Net Worth"]), max(data["Debt"])) * 1.2)
    ax.legend()
    canvas.draw()


today = datetime.date.today()
one_year_ago = today - datetime.timedelta(days=365)

sample_dates = [one_year_ago + datetime.timedelta(days=i) for i in range(365)]
sample_data = {"Net Worth": [random.randint(900, 1500) for _ in range(365)],
               "Debt": [random.randint(300, 700) for _ in range(365)]}

def update_chart_time_range():
    time_range = time_range_var.get()

    if time_range == "1day":
        start_date = today
    elif time_range == "1week":
        start_date = today - datetime.timedelta(days=7)
    elif time_range == "1month":
        start_date = today - datetime.timedelta(days=30)
    elif time_range == "1year":
        start_date = one_year_ago
    else:
        return

    filtered_data = {k: [(d, v) for d, v in zip(sample_dates, v) if d >= start_date] for k, v in sample_data.items()}

    ax.clear()
    for name, values in filtered_data.items():
        if values:  # Check if the filtered data is not empty
            dates, amounts = zip(*values)
            ax.plot(dates, amounts, label=name)

    # Set y-axis limits only when there is data available
    if any(values for values in filtered_data.values()):
        ax.set_ylim(0, max(max(a for _, a in filtered_data["Net Worth"]), max(a for _, a in filtered_data["Debt"])) * 1.2)

    ax.legend()
    fig.autofmt_xdate()  # Auto-format the x-axis date labels
    canvas.draw()

def update_display():
    selected_option = display_option_var.get()

    # Clear the current display
    display_text.delete(1.0, tk.END)

    # Update the display based on the selected option
    if selected_option == "Investments":
        display_text.insert(tk.END, "Investment data here")
    elif selected_option == "Debts":
        display_text.insert(tk.END, "Debt data here")
    elif selected_option == "Incomes":
        display_text.insert(tk.END, "Income data here")




def update_upcoming_payments():
    for i in upcoming_payments_tree.get_children():
        upcoming_payments_tree.delete(i)
    for payment in upcoming_payments_list:
        upcoming_payments_tree.insert("", "end", values=(payment["Name"], payment["Type"], payment["Amount"], payment["Due Date"]))



def create_csv_files():
    if not os.path.isfile("investments.csv"):
        with open("investments.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Name", "Type", "Amount"])

    if not os.path.isfile("debt.csv"):
        with open("debt.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Name", "Type", "Amount"])

    if not os.path.isfile("payments.csv"):
        with open("payments.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Name", "Type", "Amount", "Due Date"])

    if not os.path.isfile("income.csv"):
        with open("income.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Name", "Type", "Amount", "Date Received"])

# Call the function to create CSV files if they don't exist
create_csv_files()



#design
window = tk.Tk()
window.title("Finance Tracker")
window.geometry("1200x800")

chart_frame = ttk.Frame(window)
chart_frame.place(x=10, y=10)

fig, ax = plt.subplots(figsize=(5, 5))
data = {"Net Worth": [1000, 1100, 1200, 1300], "Debt": [500, 550, 600, 650]}
names = list(data.keys())

# Create line plots for each data series
for name, values in data.items():
    ax.plot(range(len(values)), values, label=name)

ax.set_ylim(0, max(max(data["Net Worth"]), max(data["Debt"])) * 1.2)
ax.legend()

canvas = FigureCanvasTkAgg(fig, master=chart_frame)
canvas.draw()
canvas.get_tk_widget().pack()

# Create a frame for the line chart radio buttons
radio_frame = ttk.Frame(window)
radio_frame.place(x=10, y=500)

# Create a StringVar to hold the selected time range
time_range_var = tk.StringVar(value="1day")

# Create radio buttons for each time range option
ttk.Radiobutton(radio_frame, text="1 Day", variable=time_range_var, value="1day").grid(row=0, column=0)
ttk.Radiobutton(radio_frame, text="1 Week", variable=time_range_var, value="1week").grid(row=0, column=1)
ttk.Radiobutton(radio_frame, text="1 Month", variable=time_range_var, value="1month").grid(row=0, column=2)
ttk.Radiobutton(radio_frame, text="1 Year", variable=time_range_var, value="1year").grid(row=0, column=3)

ttk.Radiobutton(radio_frame, text="1 Day", variable=time_range_var, value="1day", command=update_chart_time_range).grid(row=0, column=0)
ttk.Radiobutton(radio_frame, text="1 Week", variable=time_range_var, value="1week", command=update_chart_time_range).grid(row=0, column=1)
ttk.Radiobutton(radio_frame, text="1 Month", variable=time_range_var, value="1month", command=update_chart_time_range).grid(row=0, column=2)
ttk.Radiobutton(radio_frame, text="1 Year", variable=time_range_var, value="1year", command=update_chart_time_range).grid(row=0, column=3)

update_chart_time_range()

#changeable display right bottom
display_frame = ttk.Frame(window)
display_frame.place(x=600, y=450)

display_option_var = tk.StringVar(value="Investments")


ttk.Radiobutton(display_frame, text="Investments", variable=display_option_var, value="Investments", command=update_display).grid(row=0, column=0)
ttk.Radiobutton(display_frame, text="Debts", variable=display_option_var, value="Debts", command=update_display).grid(row=0, column=1)
ttk.Radiobutton(display_frame, text="Incomes", variable=display_option_var, value="Incomes", command=update_display).grid(row=0, column=2)

display_text = tk.Text(display_frame, width=60, height=17)
display_text.grid(row=1, column=0, columnspan=3, padx=5, pady=5)



#paymets
upcoming_payments_frame = ttk.Frame(window)
upcoming_payments_frame.place(x=600, y=10)

upcoming_payments_list = deque(maxlen=10)
upcoming_payments_list.append({"Name": "Sample Payment", "Type": "Sample Type", "Amount": 100, "Due Date": "01/01/2023"})

upcoming_payments_tree = ttk.Treeview(upcoming_payments_frame, columns=("Name", "Type", "Amount", "Due Date"), show="headings")
upcoming_payments_tree.heading("Name", text="Name")
upcoming_payments_tree.heading("Type", text="Type")
upcoming_payments_tree.heading("Amount", text="Amount")
upcoming_payments_tree.heading("Due Date", text="Due Date")
upcoming_payments_tree.pack(side="left")

for payment in upcoming_payments_list:
    upcoming_payments_tree.insert("", "end", values=(payment["Name"], payment["Type"], payment["Amount"], payment["Due Date"]))

scrollbar = ttk.Scrollbar(upcoming_payments_frame, orient="vertical", command=upcoming_payments_tree.yview)
scrollbar.pack(side="right", fill="y")

button_frame = ttk.Frame(window)
button_frame.place(x=600, y=400)

add_investment_button = ttk.Button(button_frame, text="Add Investment", command=add_investment)
add_investment_button.pack(side="left", padx=10)

add_debt_button = ttk.Button(button_frame, text="Add Debt", command=add_debt)
add_debt_button.pack(side="left", padx=10)

add_payment_button = ttk.Button(button_frame, text="Add Payment", command=add_payment)
add_payment_button.pack(side="left", padx=10)

add_income_button = ttk.Button(button_frame, text="Add Income", command=add_income)
add_income_button.pack(side="left", padx=10)

window.mainloop()
