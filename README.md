 # Swig v0.4.7
 Swig is a transpiler that compiles to HTML and JavaScript.  It has some special features that maximize efficiency and add new functionality to the standard vanilla web development tools.

 # Features:

 * Html component file system.
 * Tab-based scope for html elements.
 * Shortened get element syntax for JavaScript.

 # Component file structure:
	In Swig, there are 3 file types: *.swigh*, *.swig*, and *.swigs* .

 * _.swigh_ files acts as the root of your component tree and is where you place your custom components. Do not try to place javaScript in these files.  JavaScript should be placed in your component files after a _=SRC=_ tag.
 * _.swig_ files are where you create your component elements.
 * _.swigs_ is for style components, style components have not yet been implemented.

 # The Swig IDE:

 * _The swig IDE is still in an early development build and may have many bugs, freezes, and crashes (Especially if using SwigEditorHeavy.py). Keep this in mind._
The swig IDE allows you to quickly test your web pages by recompiling them every time you press save. It also provides syntax highlighting and an html3 display for the _SwigEditorHeavy.py_.