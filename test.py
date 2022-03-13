import tkinterweb
import tkinter as tk
root = tk.Tk()
frame = tkinterweb.HtmlFrame(root)
frame.load_website(r"index.html")
frame.pack(fill="both", expand=True)
root.mainloop()