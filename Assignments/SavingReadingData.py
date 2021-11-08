import tkinter
from tkinter import ttk

window = tkinter.Tk()
window.title("How was your day")
window.geometry("700x500")
frame = ttk.Frame(window)

try:
    with open("journal.txt", "r") as file:
        previous_day = file.readlines()[-1]
        ttk.Label(window, text=f"Last time, you had a {previous_day} day", font=("Arial", 25)).pack(ipady=60)
except FileNotFoundError:
    ttk.Label(window, text="Last time, you had a *nonexistent* day", font=("Arial", 25)).pack(ipady=60)

ttk.Label(window, text="How was your day today?", font=("Arial", 20)).pack()


def remark(day_type):
    with open("journal.txt", "w") as write:
        write.write(day_type)
    frame.destroy()
    if day_type == "good":
        ttk.Label(window, font=("Arial", 75), text="Be stay", foreground="#0000ff").pack(ipady=30)
    elif day_type == "bad":
        ttk.Label(window, font=("Arial", 75), text="Be gone", foreground="#ff0000").pack(ipady=30)


good_button = ttk.Button(frame, text="Good", command=lambda: remark("good")).pack()
bad_button = ttk.Button(frame, text="Bad", command=lambda: remark("bad")).pack()

frame.pack()
tkinter.mainloop()
