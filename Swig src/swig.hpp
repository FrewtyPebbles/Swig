#include <string>
#include <sstream>
#include <fstream>
#include <vector>
#include <iostream>
#pragma once

class component
{
private:
	std::string script;
	std::string element;
public:
	component();
	component(std::string _script, std::string _element);
	~component() =default;
	std::string getScript();
	std::string getElement();
	std::string setScript(std::string _script);
	std::string setElement(std::string _element);
};

component compileComponent(std::string componentName, bool SRCparsing = false);
