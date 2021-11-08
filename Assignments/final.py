import tkinter
from tkinter import ttk
import datetime

number_of_currency = [i for i in range(351)]


class UI:
    def __init__(self):
        try:
            with open('stores.txt', 'r') as file:
                found = False
                for line in file:
                    if 'Running Total' in line:
                        self.running_total_value = float(line[15:-1])
                        found = True
                if not found:
                    self.running_total_value = 0

        except FileNotFoundError:
            with open('stores.txt', 'w') as file:
                file.write('')
                self.running_total_value = 0

        self.stores = {}

        self.window = tkinter.Tk()
        self.window.title("Store Manager")
        self.window.geometry("500x600")

        self.store_button = tkinter.Button(self.window, text="Add another store", command=lambda: self.add_store())
        self.store_button.pack(pady=10)

        tkinter.Label(self.window, text="Location : Total").pack()
        self.location_total = tkinter.Text(self.window)
        self.location_total.configure(state='disabled')
        self.location_total.pack(padx=20)

        self.frame = tkinter.Frame(self.window)
        tkinter.Label(self.frame, text="Running Total").pack()
        self.running_total = tkinter.Text(self.frame)
        self.running_total.configure(state='disabled')
        self.running_total.pack()

        self.frame.pack(pady=30, padx=100)
        self.window.mainloop()

    def add_store(self):
        self.store_button.configure(state='disabled')
        AddStore(self.stores, self.store_button, self)

    def update_display(self):
        with open('stores.txt', 'a') as file:
            self.location_total.configure(state='normal')
            for key in self.stores:
                current_time = datetime.datetime.now().strftime('%M:%H:%S %m/%d/%Y')
                self.location_total.insert(tkinter.END, f"{current_time}\n{key} : ${self.stores[key]:.2f}\n\n")
                file.write(f"{current_time}\n{key} : ${self.stores[key]:.2f}\n")
                self.running_total_value += float(self.stores[key])
            self.stores = {}
            self.running_total.configure(state='normal')
            self.running_total.delete("1.0", tkinter.END)
            self.running_total.insert(tkinter.END, f"${self.running_total_value:.2f}")
            file.write(f"Running Total ${self.running_total_value:.2f}\n\n")
            self.location_total.configure(state='disabled')


class AddStore:
    def __init__(self, stores_dict, store_button, first_screen):
        self.window = tkinter.Tk()
        self.window.title("Add Store")
        self.window.geometry("200x100")

        self.stores_dict = stores_dict
        self.store_button = store_button
        self.first_screen = first_screen
        self.next_init = False

        self.location = tkinter.StringVar(self.window)
        tkinter.Label(self.window, text="Enter Store Location").pack()
        self.entry = tkinter.Entry(self.window, textvariable=self.location)
        self.entry.pack()
        self.enter_button = tkinter.Button(self.window, text="Enter", command=lambda: self.add_store())
        self.enter_button.pack()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def on_closing(self):
        if not self.next_init:
            self.window.destroy()
            self.store_button.configure(state='normal')

    def add_store(self):
        location = self.location.get()
        if location != "":
            self.enter_button.configure(state='disabled')
            self.entry.configure(state='disabled')
            Currency(self.stores_dict, self.entry, self.enter_button, self.location.get(), self.window,
                     self.store_button, self.next_init, self.first_screen)


class Currency:
    def __init__(self, stores_dict, previous_entry, enter_button, store_location, previous_window,
                 another_store_button, initialized, first_screen):

        self.initialized = True
        self.window = tkinter.Tk()
        self.window.title("Currencies")
        self.window.geometry("400x350")

        self.initialized = initialized
        self.stores_dict = stores_dict
        self.previous_entry = previous_entry
        self.enter_button = enter_button
        self.store_location = store_location
        self.previous_window = previous_window
        self.another_store_button = another_store_button
        self.first_screen = first_screen

        self.submitted = False
        range_validation = self.window.register(self.validate)

        tkinter.Label(self.window, text=store_location, font=("Arial", 30), fg='#00c').grid(column=1, row=0)
        tkinter.Button(self.window, text="submit", command=lambda: self.submit()).grid(column=4, row=14, padx=15)

        tkinter.Label(self.window, text="Hundreds:").grid(column=1, row=8, padx=20)
        self.hundreds = ttk.Spinbox(self.window, values=number_of_currency, from_=0, to=350)
        self.hundreds.configure(validate="key", validatecommand=(range_validation, '%P'))
        self.hundreds.grid(column=1, row=9, padx=20)

        tkinter.Label(self.window, text="Fifties:").grid(column=1, row=10, padx=5)
        self.fifties = ttk.Spinbox(self.window, values=number_of_currency, from_=0, to=350)
        self.fifties.configure(validate="key", validatecommand=(range_validation, '%P'))
        self.fifties.grid(column=1, row=11, padx=5)

        tkinter.Label(self.window, text="Twenties:").grid(column=1, row=12)
        self.twenties = ttk.Spinbox(self.window, values=number_of_currency, from_=0, to=350)
        self.twenties.configure(validate="key", validatecommand=(range_validation, '%P'))
        self.twenties.grid(column=1, row=13)

        tkinter.Label(self.window, text="Tens:").grid(column=1, row=14)
        self.tens = ttk.Spinbox(self.window, values=number_of_currency, from_=0, to=350)
        self.tens.configure(validate="key", validatecommand=(range_validation, '%P'))
        self.tens.grid(column=1, row=15)

        tkinter.Label(self.window, text="Fives:").grid(column=1, row=16)
        self.fives = ttk.Spinbox(self.window, values=number_of_currency, from_=0, to=350)
        self.fives.configure(validate="key", validatecommand=(range_validation, '%P'))
        self.fives.grid(column=1, row=17)

        tkinter.Label(self.window, text="Ones:").grid(column=1, row=18)
        self.ones = ttk.Spinbox(self.window, values=number_of_currency, from_=0, to=350)
        self.ones.configure(validate="key", validatecommand=(range_validation, '%P'))
        self.ones.grid(column=1, row=19)

        tkinter.Label(self.window, text="Quarters:").grid(column=2, row=10)
        self.quarters = ttk.Spinbox(self.window, values=number_of_currency, from_=0, to=350)
        self.quarters.configure(validate="key", validatecommand=(range_validation, '%P'))
        self.quarters.grid(column=2, row=11)

        tkinter.Label(self.window, text="Dimes:").grid(column=2, row=12)
        self.dimes = ttk.Spinbox(self.window, values=number_of_currency, from_=0, to=350)
        self.dimes.configure(validate="key", validatecommand=(range_validation, '%P'))
        self.dimes.grid(column=2, row=13)

        tkinter.Label(self.window, text="Nickels:").grid(column=2, row=14)
        self.nickels = ttk.Spinbox(self.window, values=number_of_currency, from_=0, to=350)
        self.nickels.configure(validate="key", validatecommand=(range_validation, '%P'))
        self.nickels.grid(column=2, row=15)

        tkinter.Label(self.window, text="Pennies:").grid(column=2, row=16)
        self.pennies = ttk.Spinbox(self.window, values=number_of_currency, from_=0, to=350)
        self.pennies.configure(validate="key", validatecommand=(range_validation, '%P'))
        self.pennies.grid(column=2, row=17)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    @staticmethod
    def validate(user_input):
        if user_input.isdigit():
            min_val = 0
            max_val = 351
            if int(user_input) not in range(min_val, max_val):
                return False
            return True
        elif user_input == "":
            return True
        else:
            return False

    def on_closing(self):
        self.enter_button.configure(state='normal')
        self.previous_entry.configure(state='normal')

        if self.submitted:
            self.previous_window.destroy()
            self.another_store_button.configure(state='normal')
        self.first_screen.update_display()
        self.window.destroy()

    def submit(self):
        self.submitted = True
        total = 0
        if self.hundreds.get() != "":
            total += int(self.hundreds.get()) * 100
        if self.fifties.get() != "":
            total += int(self.fifties.get()) * 50
        if self.twenties.get() != "":
            total += int(self.twenties.get()) * 20
        if self.tens.get() != "":
            total += int(self.tens.get()) * 10
        if self.fives.get() != "":
            total += int(self.fives.get()) * 5
        if self.ones.get() != "":
            total += int(self.ones.get()) * 1
        if self.quarters.get() != "":
            total += int(self.quarters.get()) * .25
        if self.dimes.get() != "":
            total += int(self.dimes.get()) * .1
        if self.nickels.get() != "":
            total += int(self.nickels.get()) * .05
        if self.pennies.get() != "":
            total += int(self.pennies.get()) * .01
        self.stores_dict[self.store_location] = total
        self.on_closing()


if __name__ == '__main__':
    UI()
