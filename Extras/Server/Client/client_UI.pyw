import tkinter
import client
import threading
from tkinter import ttk


DISCONNECT_MESSAGE = "!DISCONNECT"
FORMAT = 'utf-8'


class Login:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("Login")
        self.window.geometry('500x500')

        self.username = tkinter.StringVar()
        self.password = tkinter.StringVar()

        tkinter.Label(self.window, text="Not a Login Page", font=("Comic Sans", 45),
                      fg='#000080').pack(ipadx=40, ipady=10, padx=20, pady=40)

        ttk.Label(text="Username", font=("Comic Sans", 15)).pack()
        ttk.Entry(self.window, textvariable=self.username).pack()

        ttk.Label(text="Password", font=("Comic Sans", 15)).pack()
        ttk.Entry(self.window, textvariable=self.password, show="*").pack()
        ttk.Button(self.window, text="Login", command=lambda: self.check_login()).pack()
        self.login_label_text = tkinter.StringVar()
        self.login_label = tkinter.Label(self.window, textvariable=self.login_label_text, font=("Arial", 13), fg='#f00')
        self.login_label.pack_forget()

        self.window.mainloop()

    def check_login(self):
        temp_connection = client.Connection()
        temp_connection.send("!LOGIN")
        temp_connection.send(self.username.get())
        temp_connection.send(self.password.get())
        response = temp_connection.receive()
        if response == "!PASSWORD_CORRECT":
            self.messages()
        elif response == "!PASSWORD_INCORRECT":
            self.login_label_text.set("Password Incorrect")
            self.login_label.pack(pady=10)

        elif response == "!USERNAME_INCORRECT":
            self.login_label_text.set("Username Not Recognized")
            self.login_label.pack(pady=10)
        temp_connection.send(DISCONNECT_MESSAGE)

    def messages(self):
        self.window.destroy()
        MessageUI()


class MessageUI:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("Message System")
        self.window.geometry("500x700")

        self.connection = ""
        self.terminated = False
        self.msg_var = tkinter.StringVar()

        ttk.Label(self.window, text="Send a Message!", font=("Comic Sans", 30)).pack(ipady=20)
        self.message_box = ttk.Entry(self.window, textvariable=self.msg_var, width=40)
        self.message_box.configure(state='disabled')
        self.message_box.pack(pady=20)
        ttk.Button(self.window, text="Send", command=lambda: self.send()).pack()
        self.text_box = tkinter.Text(self.window)
        self.text_box.configure(state='disabled')
        self.text_box.pack()

        ttk.Button(self.window, text="Connect", command=lambda: self.connect()).pack(pady=10)
        self.disconnect_button = ttk.Button(self.window, text="Disconnect", command=lambda: self.disconnect())
        self.disconnect_button.pack()
        self.name_button = ttk.Button(self.window, text="Change Name", command=lambda: self.change_name())
        self.name_button.configure(state='disabled')
        self.name_button.pack(pady=10)

        self.thread = threading.Thread(target=self.receive)
        self.thread.start()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def send(self):
        if self.connection != "":
            if len(self.msg_var.get()) != 0:
                self.connection.send(self.msg_var.get())

        self.message_box.delete(0, 'end')

    def receive(self):
        while not self.terminated:
            if self.connection != "":
                msg = self.connection.receive()
                if msg is not None:
                    self.text_box.configure(state='normal')
                    self.text_box.insert(tkinter.END, f"{msg}\n")
                    self.text_box.configure(state='disabled')

    def connect(self):
        if self.connection == "":
            self.connection = client.Connection()
            self.connection.send("!CONNECTED")
            self.message_box.configure(state='normal')
            self.name_button.configure(state='normal')

    def disconnect(self):
        if self.connection != "":
            self.connection.send(DISCONNECT_MESSAGE)
            self.text_box.configure(state='normal')
            self.text_box.delete("1.0", tkinter.END)
            self.text_box.configure(state='disabled')
            self.name_button.configure(state='disabled')
            self.message_box.configure(state='disabled')
            self.connection = ""

    def change_name(self):
        if self.connection != "":
            self.disconnect_button.configure(state='disabled')
            self.name_button.configure(state='disabled')
            ChangeName(self.connection, self.name_button, self.disconnect_button)

    def on_closing(self):
        self.terminated = True
        self.disconnect()
        self.window.destroy()


class ChangeName:
    def __init__(self, conn, name_button, disconnect_button):
        self.window = tkinter.Tk()
        self.window.title("Change Name")
        self.window.geometry("500x200")

        self.conn = conn
        self.name_button = name_button
        self.disconnect_button = disconnect_button

        ttk.Label(self.window, text="Change Name Here", font=("Comic Sans", 40)).pack()
        self.username = tkinter.StringVar(self.window)
        self.entry = ttk.Entry(self.window, textvariable=self.username)
        self.entry.pack()
        ttk.Button(self.window, text="Change", command=lambda: self.change_name()).pack()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def change_name(self):
        username = self.username.get()

        if username != "":
            self.conn.send(f"!NAME {username}")
            self.on_closing()

    def on_closing(self):
        self.window.destroy()
        self.disconnect_button.configure(state='normal')
        self.name_button.configure(state='normal')


if __name__ == '__main__':
    Login()
    exit()
