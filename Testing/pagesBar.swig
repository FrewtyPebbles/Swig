#div {PageBar} style[display<flex> justify-content<space-evenly> background-color<black> color<white>]:
	#div:
	#div {HomeButton}:
	`#HOME`#
	#div {AboutButton}:
	`#ABOUT`#
	#div {DocumentationButton}:
	`#DOCUMENTATION`#
	#div {ContactButton}:
	`#CONTACT`#
	#div:

=SRC=

HomeButton.addEventListener("mouseover", function() {
	HomeButton.innerHTML = "=>HOME<=";
});
AboutButton.addEventListener("mouseover", function() {
	AboutButton.innerHTML = "=>ABOUT<=";
});
DocumentationButton.addEventListener("mouseover", function() {
	DocumentationButton.innerHTML = "=>DOCUMENTATION<=";
});
ContactButton.addEventListener("mouseover", function() {
	ContactButton.innerHTML = "=>CONTACT<=";
});

HomeButton.addEventListener("mouseout", function() {
	HomeButton.innerHTML = "#HOME#";
});
AboutButton.addEventListener("mouseout", function() {
	AboutButton.innerHTML = "#ABOUT#";
});
DocumentationButton.addEventListener("mouseout", function() {
	DocumentationButton.innerHTML = "#DOCUMENTATION#";
});
ContactButton.addEventListener("mouseout", function() {
	ContactButton.innerHTML = "#CONTACT#";
});
