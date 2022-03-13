style @ "filename.swigs"
Component:
	#div (exampleComponent) style [border-style<solid>] href [argument]:
		#p:
		This is a component.
		#div:
		This another part of the component

Script:
exampleComponent.hover
{
	exampleComponentClass.style += background-color<red>;
}

exampleComponent.click
{
	exampleComponentClass.style += background-color<green>;
}