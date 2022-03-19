import subprocess
import threading
import time
import tkinter as tk
from tkinter import Frame, Menu, Menubutton, ttk
import tkinter.scrolledtext as tkscrolled
from tkinter.filedialog import askopenfilename, asksaveasfilename
import keyboard

#USES python 3.6
#SWIG IDE
# VER 0.8.5

#################
#Now available on linux


##TKINTER CLOSEABLE NOTEBOOK TABS
textEditorWidth = 50

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
		if self.tab(self.select())['text'] != "Notes":
			self.select("@%d,%d" % (event.x, event.y))
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

window.title("Swig IDE")
window.state(tk.NORMAL)
window.grid_rowconfigure(0, weight=1)
tabs = CustomNotebook(window)
terminal = tkscrolled.ScrolledText(state=tk.DISABLED, pady=5, padx=5, bg="black", insertbackground="white", fg="white", height=10)
txt_edit = tkscrolled.ScrolledText(window,  bg="#222940", fg="grey", font=("Fixedsys", 11), insertbackground="white")
window.grid_columnconfigure(0, weight=1)

def scrollHorizontally(textWidget, event):
    textWidget.xview_scroll((event.delta/120), "units")

def open_file():
	global currentFilepath
	"""Open a file for editing."""
	filepath = askopenfilename(
		filetypes=[("Text Files", "*.swig"), ("Text Files", "*.swigh"), ("Text Files", "*.swigs"), ("Text Files", "*.txt"), ("All Files", "*.*")]
	)
	if not filepath:
		return
	with open(filepath, "r") as input_file:
		#currentFilepath = filepath
		try:
			if tabs.tab(tabs.select(), "text") == "Untitled.swigh":
				textbox = (tabs.nametowidget(tabs.select()).winfo_children()[1]).winfo_children()[1]
				#print((tabs.nametowidget(tabs.select()).winfo_children()[1]).winfo_children()[1])
				tabs.tab(tabs.select(), text=filepath)
				text = input_file.read()
				textbox.insert(tk.END, text)
			else:
				newWindowFrame = Frame(window)
				newWindowLineNums = tk.Text(newWindowFrame,  bg="#222940", fg="grey", font=("Fixedsys", 11), insertbackground="white",width=7)
				newWindow = tkscrolled.ScrolledText(newWindowFrame, wrap="none",  bg="#222940", fg="grey", font=("Fixedsys", 11), insertbackground="white")#, width=textEditorWidth)
				newWindow.bind('<Shift-MouseWheel>', lambda:scrollHorizontally(newWindow))
				newWindowFrame.grid(row=0, column=0, sticky="nsew")
				newWindowFrame.grid_rowconfigure(0, weight=1)
				newWindowFrame.grid_columnconfigure(0, weight=0)
				newWindowFrame.grid_columnconfigure(1, weight=1)
				newWindowLineNums.grid(row=0, column=0, sticky="nsew")
				newWindow.grid(row=0, column=1, sticky="nsew")
				tabNames[filepath] = tabs.add(newWindowFrame, text=filepath)
				tabs.select(tabNames[filepath])
				text = input_file.read()
				newWindow.insert(tk.END, text)
		except:
			newWindowFrame = Frame(window)
			newWindowLineNums = tk.Text(newWindowFrame,  bg="#222940", fg="grey", font=("Fixedsys", 11), insertbackground="white",width=7)
			newWindow = tkscrolled.ScrolledText(newWindowFrame, wrap="none",  bg="#222940", fg="grey", font=("Fixedsys", 11), insertbackground="white")#, width=textEditorWidth)
			newWindow.bind('<Shift-MouseWheel>', lambda:scrollHorizontally(newWindow))
			newWindowFrame.grid(row=0, column=0, sticky="nsew")
			newWindowFrame.grid_rowconfigure(0, weight=1)
			newWindowFrame.grid_columnconfigure(0, weight=0)
			newWindowFrame.grid_columnconfigure(1, weight=1)
			newWindowLineNums.grid(row=0, column=0, sticky="nsew")
			newWindow.grid(row=0, column=1, sticky="nsew")
			tabNames[filepath] = tabs.add(newWindowFrame, text=filepath)
			tabs.select(tabNames[filepath])
			text = input_file.read()
			newWindow.insert(tk.END, text)
		time.sleep(0.001)
	time.sleep(0.001)
	window.title(f"Swig Editor - {filepath}")



def save_file(saveAs = False):
	global currentFilepath
	if tabs.tab(tabs.select())['text'] != "Notes":
		if currentFilepath != "" and saveAs == False and tabs.tab(tabs.select())['text'] != "Untitled.swigh":
			currentFilepath = tabs.tab(tabs.select(), "text")
			if not currentFilepath:
				tk.messagebox.showerror(title="ERROR", message="Something went wrong when trying to find your file.")
				return
			with open(currentFilepath, "w") as output_file:
				active_object = (tabs.nametowidget(tabs.select()).winfo_children()[1]).winfo_children()[1]
				text = active_object.get(1.0, tk.END)
				output_file.write(text)
			if (currentFilepath.split('.')[1]) == "swigh":
				result = subprocess.Popen(["./Swig.exe", "-sh", f"{currentFilepath.split('.')[0]}"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
				out, err = result.communicate()
				terminal.config(state=tk.NORMAL)
				terminal.delete(1.0,"end")
				terminal.insert(1.0, err)
			terminal.config(state=tk.DISABLED)
			window.title(f"Swig Editor - {currentFilepath}")
			print(f"currentFilepath = {(currentFilepath.split('.')[0])}.html")
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
				result = subprocess.Popen(["./Swig.exe", "-sh", f"{filepath.split('.')[0]}"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
				out, err = result.communicate()
				terminal.config(state=tk.NORMAL)
				terminal.delete(1.0,"end")
				terminal.insert(1.0, err)
			terminal.config(state=tk.DISABLED)
			window.title(f"Swig Editor - {filepath}")

def newFileThread():
	newWindowFrame = Frame(window)
	newWindowLineNums = tk.Text(newWindowFrame,  bg="#222940", fg="grey", font=("Fixedsys", 11), insertbackground="white",width=7)
	newWindow = tkscrolled.ScrolledText(newWindowFrame, wrap="none",  bg="#222940", fg="grey", font=("Fixedsys", 11), insertbackground="white")#, width=textEditorWidth)
	newWindow.bind('<Shift-MouseWheel>', lambda:scrollHorizontally(newWindow))
	newWindowFrame.grid(row=0, column=0, sticky="nsew")
	newWindowFrame.grid_rowconfigure(0, weight=1)
	newWindowFrame.grid_columnconfigure(0, weight=0)
	newWindowFrame.grid_columnconfigure(1, weight=1)
	newWindowLineNums.grid(row=0, column=0, sticky="nsew")
	newWindow.grid(row=0, column=1, sticky="nsew")
	time.sleep(0.1)
	newtab = tabs.add(child=newWindowFrame, text="Untitled.swigh", state='normal')
	time.sleep(0.1)
	tabs.select(newtab)
	print((tabs.nametowidget(tabs.select(newtab)).winfo_children()))
def newFile():
	threading.Thread(target=newFileThread, name='newFileThread', daemon=True).start()


#fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2, bg="black")

#btn_open = tk.Button(fr_buttons, text="Open", command=open_file, bg="black", fg="white")
#btn_save = tk.Button(fr_buttons, text="Save As...", command=lambda: save_file(True), bg="black", fg="white")


tabs.grid(row=0, column=0, sticky="nsew")
terminal.grid(row=1, column=0, sticky="nsew")
tabs.add(txt_edit, text='Notes')

my_menu=Menu(window, background='#000000', foreground='white', activebackground='grey', activeforeground='black', tearoff=0)
file_menu= Menu(my_menu, background='#000000', foreground='white', activebackground='grey', activeforeground='black',tearoff=0)
language_menu= Menu(my_menu, background='#000000', foreground='white', activebackground='grey', activeforeground='black',tearoff=0)

my_menu.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="New",command=newFile)

file_menu.add_command(label="Open...",command=open_file)

file_menu.add_command(label="Save",command=save_file)

file_menu.add_command(label="Save As...",command=lambda:save_file(True))

file_menu.add_command(label="Exit",command=window.quit)

my_menu.add_cascade(label="Language", menu=language_menu)

language_menu.add_command(label="Swig")

language_menu.add_command(label="Noodle")



window.config(menu=my_menu)


#IDE FUNCTIONALITY
def handle_tab_changed(event):
	global currentFilepath
	selection = event.widget.select()
	tab = event.widget.tab(selection, "text")
	window.title(f"Swig Editor - {tab}")
	if str(tab) != "Notes" and str(tab) != "Untitled.swigh":
		currentFilepath = str(tab)
	time.sleep(1)


tabs.bind("<<NotebookTabChanged>>", handle_tab_changed)
keyboard.add_hotkey("ctrl+s", lambda: save_file())
highlighting = True
#syntax
def syntaxHighlightThread():
	global currentFilepath
	global highlighting
	if tabs.tab(tabs.select(), "text") != "Notes" and highlighting:
		highlighting = False
		currentFilepath = tabs.select()
		active_tab = (tabs.nametowidget(tabs.select()).winfo_children()[1]).winfo_children()[1]
		active_tab.tag_configure("element", foreground="#ee00ff")
		active_tab.tag_configure("default", foreground="white")
		active_tab.tag_configure("tag", foreground="#7fc6db")
		active_tab.tag_configure("tagparameter", foreground="#10ff00")
		active_tab.tag_configure("id", foreground="#cf6380")
		active_tab.tag_configure("class", foreground="#75e6e4")
		#active_tab.tag_add("default", "1.0", "end-1c")
		addLinenum = False
		lineNum = 1
		columnNum = 0
		syntax = 'n'
		editorText = active_tab.get("1.0",tk.END)
		for i in range(0,len(editorText)):
			char = editorText[i]
			addLinenum = False
			if char == '\n':
				syntax = 'n'
				columnNum = 0
				addLinenum = True
			elif char == '\r':
				syntax = 'n'
				columnNum = 0
				addLinenum = True
			elif char == '\t':
				syntax = 'n'
			elif char == '#':
				syntax = 'e'
			elif char == ':':
				syntax = 'n'
			elif char == '[':
				syntax = 't'
			elif char == ']':
				syntax = 'e'
			elif char == '{':
				syntax = 'i'
			elif char == '}':
				syntax = 'e'
			elif char == '(':
				syntax = 'c'
			elif char == ')':
				syntax = 'e'
			elif char == '<':
				syntax = 'p'
			elif char == '>':
				syntax = 't'

			if syntax == 'n':
				active_tab.tag_add("default", f"{lineNum}.{columnNum}", f"{lineNum}.{columnNum+1}")
			elif syntax == 'e':
				active_tab.tag_add("element", f"{lineNum}.{columnNum-1}", f"{lineNum}.{columnNum+1}")
			elif syntax == 't':
				active_tab.tag_add("tag", f"{lineNum}.{columnNum-1}", f"{lineNum}.{columnNum+1}")
			elif syntax == 'c':
				active_tab.tag_add("class", f"{lineNum}.{columnNum-1}", f"{lineNum}.{columnNum+1}")
			elif syntax == 'i':
				active_tab.tag_add("id", f"{lineNum}.{columnNum-1}", f"{lineNum}.{columnNum+1}")
			elif syntax == 'p':
				active_tab.tag_add("tagparameter", f"{lineNum}.{columnNum-1}", f"{lineNum}.{columnNum+1}")
			if addLinenum == True:
				lineNum += 1
			columnNum += 1
		time.sleep(0.1)
		highlighting = True
		

def syntaxHighlight(event):
	threading.Thread(target=syntaxHighlightThread, daemon=True).start()


#line numbers
def drawLineNumsThread():
	global currentFilepath
	#tempLinenum = 1
	currentLN = 0
	#NewLineNumbers = ""
	#while True:
	if tabs.tab(tabs.select(), "text") != "Notes":
		#time.sleep(0.5)
		inactive_tab = (tabs.nametowidget(tabs.select()).winfo_children()[0])
		active_tab = (tabs.nametowidget(tabs.select()).winfo_children()[1]).winfo_children()[1]
		editorText = active_tab.get("1.0",tk.END)
		lineNum = len(editorText.split('\n'))
		if currentLN != lineNum:
			inactive_tab.delete("1.0","end")
			for i in range(1,lineNum):
				inactive_tab.insert("end", (f"{i}".ljust(6,'-')) + "|")
		currentLN = lineNum
		inactive_tab = (tabs.nametowidget(tabs.select()).winfo_children()[0])
		scrollbarElem = (tabs.nametowidget(tabs.select()).winfo_children()[1]).winfo_children()[1]
		codepos = scrollbarElem.yview()
		threading.Thread(target=inactive_tab.yview_moveto(codepos[0]), daemon=True).start()

def drawLineNums(event):
	drawLineNumsThread()
#



#t2 = threading.Thread(target=drawLineNums, name='t2', daemon=True)
#t2.start()

window.bind_all('<Key>', drawLineNums, add="+")
window.bind('<Motion>', drawLineNums, add="+")
window.bind_all('<MouseWheel>', drawLineNums, add="+")
window.bind_all('<Key>', syntaxHighlight, add="+")
#t3 = threading.Thread(target=linkScrollbar, name='t3', daemon=True)
#t3.start()

#

window.mainloop()
