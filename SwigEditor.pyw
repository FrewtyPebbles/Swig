import subprocess
import threading
import time
import tkinter as tk
from tkinter import Frame, Menu, Menubutton, ttk
import tkinter.scrolledtext as tkscrolled
from tkinter.filedialog import askopenfilename, asksaveasfilename
from turtle import width
from tkinterweb import HtmlFrame
import keyboard

##TKINTER CLOSEABLE NOTEBOOK TABS
class CustomNotebook(ttk.Notebook):
	"""A ttk Notebook with close buttons on each tab"""

	__initialized = False

	def __init__(self, *args, **kwargs):
		if not self.__initialized:
			self.__initialize_custom_style()
			self.__inititialized = True

		kwargs["style"] = "CustomNotebook"
		time.sleep(0.001)
		ttk.Notebook.__init__(self, *args, **kwargs)

		self._active = None
		time.sleep(0.001)
		self.bind("<ButtonPress-1>", self.on_close_press, True)
		time.sleep(0.001)
		self.bind("<ButtonRelease-1>", self.on_close_release)

	def on_close_press(self, event):
		"""Called when the button is pressed over the close button"""

		element = self.identify(event.x, event.y)

		if "close" in element:
			index = self.index("@%d,%d" % (event.x, event.y))
			self.state(['pressed'])
			self._active = index
			return "break"

	def on_close_release(self, event):
		"""Called when the button is released"""
		self.select("@%d,%d" % (event.x, event.y))
		if self.tab(self.select())['text'] != "Notes":
			if not self.instate(['pressed']):
				return

			element =  self.identify(event.x, event.y)
			if "close" not in element:
				# user moved the mouse off of the close button
				return

			index = self.index("@%d,%d" % (event.x, event.y))

			if self._active == index:
				self.forget(index)
				self.event_generate("<<NotebookTabClosed>>")

			self.state(["!pressed"])
			self._active = None

	def __initialize_custom_style(self):
		style = ttk.Style()
		self.images = (
			tk.PhotoImage("img_close", data='''
				R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
				d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
				5kEJADs=
				'''),
			tk.PhotoImage("img_closeactive", data='''
				R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
				AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
				'''),
			tk.PhotoImage("img_closepressed", data='''
				R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
				d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
				5kEJADs=
			''')
		)

		style.element_create("close", "image", "img_close",
							("active", "pressed", "!disabled", "img_closepressed"),
							("active", "!disabled", "img_closeactive"), border=8, sticky='')
		style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
		style.layout("CustomNotebook.Tab", [
			("CustomNotebook.tab", {
				"sticky": "nswe",
				"children": [
					("CustomNotebook.padding", {
						"side": "top",
						"sticky": "nswe",
						"children": [
							("CustomNotebook.focus", {
								"side": "top",
								"sticky": "nswe",
								"children": [
									("CustomNotebook.label", {"side": "left", "sticky": ''}),
									("CustomNotebook.close", {"side": "left", "sticky": ''}),
								]
						})
					]
				})
			]
		})
	])
######


currentFilepath = ""

tabNames = {}

window = tk.Tk()

window.title("Swig Editor")
style=ttk.Style()
style.theme_use('classic')
style.configure("Vertical.TScrollbar", background="black", bordercolor="red", arrowcolor="white")

window.rowconfigure(0, minsize=100, weight=1)
window.columnconfigure(1, minsize=100, weight=1)
tabs = CustomNotebook(window)
terminal = tkscrolled.ScrolledText(state=tk.DISABLED, pady=5, padx=5, bg="black", insertbackground="white", fg="white", height=7)
txt_edit = tkscrolled.ScrolledText(window,  bg="#222940", fg="grey", font=("Fixedsys", 11), insertbackground="white")
projectDisplay = HtmlFrame(window, horizontal_scrollbar="auto")

def open_file():
	global currentFilepath
	"""Open a file for editing."""
	filepath = askopenfilename(
		filetypes=[("Text Files", "*.swig"), ("Text Files", "*.swigh"), ("Text Files", "*.swigs"), ("Text Files", "*.txt"), ("All Files", "*.*")]
	)
	if not filepath:
		return
	with open(filepath, "r") as input_file:
		currentFilepath = filepath
		try:
			if tabs.tab(tabs.select(), "text") == "Untitled.swigh":
				textbox = (tabs.nametowidget(tabs.select()).winfo_children()[1]).winfo_children()[1]
				#print((tabs.nametowidget(tabs.select()).winfo_children()[1]).winfo_children()[1])
				tabs.tab(tabs.select(), text=currentFilepath)
				text = input_file.read()
				textbox.insert(tk.END, text)
			else:
				newWindowFrame = Frame(window)
				newWindowLineNums = tk.Text(newWindowFrame,  bg="#222940", fg="grey", font=("Fixedsys", 11), insertbackground="white",width=7)
				newWindow = tkscrolled.ScrolledText(newWindowFrame,  bg="#222940", fg="grey", font=("Fixedsys", 11), insertbackground="white")
				newWindowFrame.grid(row=0, column=0, sticky="nsew")
				newWindowLineNums.grid(row=0, column=0, sticky="ns")
				newWindow.grid(row=0, column=1, sticky="nsew")
				tabNames[currentFilepath] = tabs.add(newWindowFrame, text=currentFilepath)
				tabs.select(tabNames[currentFilepath])
				text = input_file.read()
				newWindow.insert(tk.END, text)
		except:
			newWindowFrame = Frame(window)
			newWindowLineNums = tk.Text(newWindowFrame,  bg="#222940", fg="grey", font=("Fixedsys", 11), insertbackground="white",width=7)
			newWindow = tkscrolled.ScrolledText(newWindowFrame,  bg="#222940", fg="grey", font=("Fixedsys", 11), insertbackground="white")
			newWindowFrame.grid(row=0, column=0, sticky="nsew")
			newWindowLineNums.grid(row=0, column=0, sticky="ns")
			newWindow.grid(row=0, column=1, sticky="nsew")
			tabNames[currentFilepath] = tabs.add(newWindowFrame, text=currentFilepath)
			tabs.select(tabNames[currentFilepath])
			text = input_file.read()
			newWindow.insert(tk.END, text)
		time.sleep(0.001)
		projectDisplay.load_html(open(((filepath.split('.')[0]) + ".html"), "r").read())
	time.sleep(0.001)
	window.title(f"Swig Editor - {filepath}")
	
	

def save_file(saveAs = False):
	global currentFilepath
	if tabs.tab(tabs.select())['text'] != "Notes":
		if currentFilepath != "" and saveAs == False and tabs.tab(tabs.select())['text'] != "Untitled.swigh":
			currentFilepath = tabs.tab(tabs.select())['text']
			if not currentFilepath:
				tk.messagebox.showerror(title="ERROR", message="Something went wrong when trying to find your file.")
				return
			with open(currentFilepath, "w") as output_file:
				active_object = (tabs.nametowidget(tabs.select()).winfo_children()[1]).winfo_children()[1]
				text = active_object.get(1.0, tk.END)
				output_file.write(text)
			if (currentFilepath.split('.')[1]) == "swigh":
				result = subprocess.Popen(["swig", "-sh", f"{currentFilepath.split('.')[0]}"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
				out, err = result.communicate()
				terminal.config(state=tk.NORMAL)
				terminal.delete(1.0,"end")
				terminal.insert(1.0, err)
			terminal.config(state=tk.DISABLED)
			window.title(f"Swig Editor - {currentFilepath}")
			print(f"currentFilepath = {(currentFilepath.split('.')[0])}.html")
			projectDisplay.load_html(open(((currentFilepath.split('.')[0]) + ".html"), "r").read())
		else:
			"""Save the current file as a new file."""
			filepath = asksaveasfilename(
				defaultextension="txt",
				filetypes=[("Text Files", "*.swig"), ("Text Files", "*.swigh"), ("Text Files", "*.swigs"), ("Text Files", "*.txt"), ("All Files", "*.*")],
			)
			if not filepath:
				return
			with open(filepath, "w") as output_file:
				active_object = (tabs.nametowidget(tabs.select()).winfo_children()[1]).winfo_children()[1]
				text = active_object.get(1.0, tk.END)
				output_file.write(text)
				currentFilepath = filepath
				tabs.tab(tabs.select(), text=currentFilepath)
			if (filepath.split('.')[1]) == "swigh":
				result = subprocess.Popen(["swig", "-sh", f"{filepath.split('.')[0]}"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
				out, err = result.communicate()
				terminal.config(state=tk.NORMAL)
				terminal.delete(1.0,"end")
				terminal.insert(1.0, err)
			terminal.config(state=tk.DISABLED)
			projectDisplay.load_html(open(((filepath.split('.')[0]) + ".html"), "r").read())
			window.title(f"Swig Editor - {filepath}")

def newFile():
	newWindowFrame = Frame(window)
	newWindowLineNums = tk.Text(newWindowFrame,  bg="#222940", fg="grey", font=("Fixedsys", 11), insertbackground="white",width=7)
	newWindow = tkscrolled.ScrolledText(newWindowFrame,  bg="#222940", fg="grey", font=("Fixedsys", 11), insertbackground="white")
	newWindowFrame.grid(row=0, column=0, sticky="nsew")
	newWindowLineNums.grid(row=0, column=0, sticky="ns")
	newWindow.grid(row=0, column=1, sticky="nsew")
	time.sleep(1)
	tabNames["Untitled.swigh"] = tabs.add(child=newWindowFrame, text="Untitled.swigh", state='normal')
	time.sleep(1)
	tabs.select(tabNames["Untitled.swigh"])


#fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2, bg="black")

#btn_open = tk.Button(fr_buttons, text="Open", command=open_file, bg="black", fg="white")
#btn_save = tk.Button(fr_buttons, text="Save As...", command=lambda: save_file(True), bg="black", fg="white")
my_menu=Menu(window, background='#000000', foreground='white', activebackground='grey', activeforeground='black')
window.config(menu=my_menu)
file_menu= Menu(my_menu, background='#000000', foreground='white', activebackground='grey', activeforeground='black')
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New",command=lambda:newFile())
file_menu.add_command(label="Open...",command=open_file)
file_menu.add_command(label="Save",command=lambda:save_file())
file_menu.add_command(label="Save As...",command=lambda:save_file(True))
file_menu.add_separator()
file_menu.add_command(label="Exit",command=window.quit)

tabs.grid(row=0, column=1, sticky="nsew")
projectDisplay.grid(row=0, rowspan=3, column=3, sticky="nsew")
terminal.grid(row=2, column=0,columnspan=2, sticky="nsew")
tabs.add(txt_edit, text='Notes')

#IDE FUNCTIONALITY
def handle_tab_changed(event):
	global currentFilepath
	time.sleep(0.001)
	selection = event.widget.select()
	time.sleep(0.001)
	tab = event.widget.tab(selection, "text")
	time.sleep(0.001)
	window.title(f"Swig Editor - {tab}")
	if str(tab) != "Notes" and str(tab) != "Untitled.swigh":
		print(tab)
		currentFilepath = str(tab)
		time.sleep(0.001)
		projectDisplay.load_html(open(((str(tab).split('.')[0]) + ".html"), "r").read())

tabs.bind("<<NotebookTabChanged>>", handle_tab_changed)
keyboard.add_hotkey("ctrl+s", lambda: save_file())
#syntax
def syntaxHighlight():
	global currentFilepath
	tempLinenum = 1
	while True:
		if tabs.tab(tabs.select(), "text") != "Notes":
			currentFilepath = tabs.select()
			active_tab = (tabs.nametowidget(tabs.select()).winfo_children()[1]).winfo_children()[1]
			active_tab.tag_configure("element", foreground="#ee00ff")
			active_tab.tag_configure("default", foreground="white")
			active_tab.tag_configure("tag", foreground="#7fc6db")
			active_tab.tag_configure("tagparameter", foreground="#10ff00")
			active_tab.tag_configure("id", foreground="#cf6380")
			active_tab.tag_configure("class", foreground="#75e6e4")
			addLinenum = False
			lineNum = 1
			columnNum = 0
			syntax = 'n'
			editorText = active_tab.get("1.0",tk.END)
			for i in range(0,len(editorText)):
				char = editorText[i]
				addLinenum = False
				match char:
					case '\n':
						syntax = 'n'
						columnNum = 0
						addLinenum = True
					case '\r':
						syntax = 'n'
						columnNum = 0
						addLinenum = True
					case '\t':
						syntax = 'n'
					case '#':
						syntax = 'e'
					case ':':
						syntax = 'n'
					case '[':
						syntax = 't'
					case ']':
						syntax = 'e'
					case '{':
						syntax = 'i'
					case '}':
						syntax = 'e'
					case '(':
						syntax = 'c'
					case ')':
						syntax = 'e'
					case '<':
						syntax = 'p'
					case '>':
						syntax = 't'
				match syntax:
					case 'n':
						active_tab.tag_add("default", f"{lineNum}.{columnNum}", f"{lineNum}.{columnNum+1}")
					case 'e':
						active_tab.tag_add("element", f"{lineNum}.{columnNum}", f"{lineNum}.{columnNum+1}")
					case 't':
						active_tab.tag_add("tag", f"{lineNum}.{columnNum}", f"{lineNum}.{columnNum+1}")
					case 'c':
						active_tab.tag_add("class", f"{lineNum}.{columnNum}", f"{lineNum}.{columnNum+1}")
					case 'i':
						active_tab.tag_add("id", f"{lineNum}.{columnNum}", f"{lineNum}.{columnNum+1}")
					case 'p':
						active_tab.tag_add("tagparameter", f"{lineNum}.{columnNum}", f"{lineNum}.{columnNum+1}")
				if addLinenum == True:
					lineNum += 1
				columnNum += 1
			inactive_tab = (tabs.nametowidget(tabs.select()).winfo_children()[0])
			NewLineNumbers = ""
			scrollbarElem = (tabs.nametowidget(tabs.select()).winfo_children()[1]).winfo_children()[1]
			codepos = scrollbarElem.yview()
			if tempLinenum < lineNum:
				NewLineNumbers +=(f"{lineNum-1}".ljust(6,'-')) + "|"
				inactive_tab.insert("end", NewLineNumbers)
				print(f"{lineNum} : {tempLinenum}")
			elif tempLinenum > lineNum:
				difference = abs(round((((lineNum-1)*7) - len(inactive_tab.get("1.0", 'end')))/7))
				print(difference)
				for j in range(0,difference):
					inactive_tab.delete("1." + str(len(inactive_tab.get("1.0", 'end')) - 8),"end")
			
			
			inactive_tab.yview_moveto(codepos[0])
			#scrollbarElem.yview_moveto(codepos2[0])
			time.sleep(0.01)
			tempLinenum = lineNum
			
		
		


t1 = threading.Thread(target=syntaxHighlight, name='t1', daemon=True)
t1.start()

#

window.mainloop()
