from tkinter import *
from cryptography.fernet import Fernet


def get_password():
    """Open Tkinter box to enter password, return password entered. Encode password using Fernet.
    """
    root = Tk()

    e = Entry(root, show="*", width=50)
    e.pack()

    key = Fernet.generate_key()
    crypt = Fernet(key)

    # Class to store password
    class PW:
        pw = ""

        @staticmethod
        def my_click():

            get = crypt.encrypt(e.get().encode())
            PW.pw = get

            root.destroy()

    myButton = Button(root, text="Enter the password", command=PW.my_click)
    myButton.pack()

    myLabel = Label(root)
    myLabel.pack()

    root.mainloop()

    # Assert this regarding password length.
    if len(crypt.decrypt(bytes(PW.pw)).decode()) != 9:
        return get_password()

    return crypt.decrypt(bytes(PW.pw)).decode()
