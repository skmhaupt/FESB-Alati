import tkinter as tk
from tkinter import filedialog

def UploadAction(event=None):
    filename = filedialog.askopenfilename()
    print("Selected:", filename)




root = tk.Tk(screenName="Lab generator")

#Input data fields
button = tk.Button(root, text="'Load participants file.'", command=UploadAction)
button.pack()



root.mainloop()