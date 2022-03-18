#div style[font-family<sansserif> border-color<hotpink> width<300px>text-align<center>background-color<pink>border-style<solid> border-radius<20px>]:
	#h1:
	LOGIN
Username `: 
	#input {username} style[border-color<hotpink> width<230px> border-radius<5px> padding<10px> margin<10px>]:
Password `: 
	#input {password} style[border-color<hotpink> width<230px> border-radius<5px> padding<10px> margin<10px>]:
	#br:
	#button onclick[login()] style[padding<10px>]:
	Login
	#br:

=SRC=

function login()
{

	alert("Welcome " + document.getElementById("username").value + "!");

}

