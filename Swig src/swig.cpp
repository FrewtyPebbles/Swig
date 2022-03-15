#include "swig.hpp"

component::component(){};

component::component(std::string _script, std::string _element)
{
    script = _script;
    element = _element;
};
std::string component::getScript()
{
    return script;
}
std::string component::getElement()
{
    return element;
}
std::string component::setScript(std::string _script)
{
    script = _script;
    return script;
}
std::string component::setElement(std::string _element)
{
    element = _element;
    return element;
}


component compileComponent(std::string componentName)
{
	component htmlComponent;
    std::ifstream componentFile;
    char character;
    std::stringstream compiledElement;
    std::stringstream compiledJavascript;
	//if component file name doesnt exist return failure
	try 
    {
        componentFile = std::ifstream(componentName + ".swig", std::ios::in|std::ios::binary ) ;
        if( !componentFile ) throw std::ios::failure( "" ) ; 
    }
    catch( const std::exception& e )
    {
		return component("null","null");
    }
    ///USER ELEMENT
    while (componentFile >> std::noskipws >> character)
	{
        compiledElement << character;
	}
    htmlComponent.setElement(compiledElement.str());
    htmlComponent.setScript(compiledJavascript.str());
    componentFile.close();
    return htmlComponent;
}