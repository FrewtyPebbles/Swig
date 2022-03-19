@LOGIN!
@Username!
@Password!
#div {login} style[font-family<sansserif> border-color<hotpink> width<300px>text-align<center>background-color<pink>border-style<solid> border-radius<20px>]:
	#h1:
	LOGIN^
Username^ `: 
	#input {username} style[border-color<hotpink> width<230px> border-radius<5px> padding<10px> margin<10px>]:
Password^ `: 
	#input {password} style[border-color<hotpink> width<230px> border-radius<5px> padding<10px> margin<10px>]:
	#br:
	#button onclick[login()] style[padding<10px>]:
	Login
	#br:
	#list |TODO LIST&Go to the store.&Eat lunch.&Study for exams.&Organize repo.&Make documentation website.|:
=SRC=

function login()
{
	
	login.innerHTML ="<h4>Welcome " + username.value+ "</h4>";
	alert("Welcome " + username.value + "!");

}











