#include "swigh.hpp"
#include "swig.hpp"

template<class T, typename ValueType>
void setScope(T & container, size_t index, ValueType & value)
{
    if (index < container.size())
	{
        container[index] = value;
	}
	else
	{
		container.resize(index+1);
		container[index] = value;
	}
}

template<class T, typename ValueType>
void appendScope(T & container, size_t index, ValueType & value)
{
    if (index < container.size())
	{
        container[index].append(value);
	}
	else
	{
		container.resize(index+1);
		container[index] = "";
		container[index].append(value);
	}
}

std::stringstream compileHeirchy(std::fstream &file)
{
	std::stringstream CompiledHTML;
	char character;
	char lastCharacter = 'a';
	std::vector<std::string> scopeContent;
	std::vector<std::string> scopeElement;
	std::vector<std::string> scopetags;
	std::string contentString = "";
	std::string elementString = "";
	scopeElement.push_back("");
	scopeContent.push_back("");
	scopetags.push_back("");
	unsigned scope = 1;
	unsigned lastscope = 0;
	unsigned linenum = 1;
	bool characterCheck = true;
	bool element = true;
	component userComponent;
  bool escape = false;
	while (file >> std::noskipws >> character)
	{
    //Start of parser
    if(!escape)
    {
  		switch (character)
  		{
  		case ' ':
  			element = false;
  			contentString.push_back(character);
  			break;
  		case ',':
  			if (characterCheck)
  			{
  				contentString.append(" ");
  			}
  			else
  			{
  				contentString.push_back(character);
  			}
  			break;
  		case '#':
  			if (scopeElement[lastscope] == "component" && lastCharacter == '#' && lastscope > scope)
  			{
  				std::cerr << " > ERROR L:" << linenum << " > You are attempting to place an element inside of an invalid scope.\n - ? - If the parent element is a component, please place your elements inside of that component's .swig file.";
  			}
  			if (lastscope >= scope)
  			{
  				for (unsigned i = lastscope; i > scope-1; --i)
  				{
  					if (scopeElement[i] != "" && scopeElement[i] != "component")
  					{
  						CompiledHTML << "</"<< scopeElement[i] << ">\n";
  						scopeElement[i] = "";
  					}
  				}
  			}
  			else if (scope == lastscope)
  			{
  				if (scopeElement[scope] != "")
  				{
  					CompiledHTML << "</"<< scopeElement[scope] << ">\n";
  				}
  			}
  			characterCheck = true;
  			element = true;
  			break;
  		case '(':
  			if (characterCheck)
  			{
  				contentString.append(" class = \"");
  			}
  			else
  			{
  				contentString.push_back(character);
  			}
  			break;
  		case ')':
  			if (characterCheck)
  			{
  				contentString.append("\" ");
  			}
  			else
  			{
  				contentString.push_back(character);
  			}
  			break;
  		case '[':
  			if (characterCheck)
  			{
  				contentString.append(" = \"");
  			}
  			else
  			{
  				contentString.push_back(character);
  			}
  			break;
  		case ']':
  			if (characterCheck)
  			{
  				contentString.append("\" ");
  			}
  			else
  			{
  				contentString.push_back(character);
  			}
  			break;
  		case '{':
  			if (characterCheck)
  			{
  				contentString.append(" id = \"");
  			}
  			else
  			{
  				contentString.push_back(character);
  			}
  			break;
  		case '}':
  			if (characterCheck)
  			{
  				contentString.append("\" ");
  			}
  			else
  			{
  				contentString.push_back(character);
  			}
  			break;
      case '`':
        escape = true;
        break;
  		case '<':
  			if (characterCheck)
  			{
  				contentString.append(":");
  			}
  			else
  			{
  				contentString.push_back(character);
  			}
  			break;
  		case '>':
  			if (characterCheck)
  			{
  				contentString.append(";");
  			}
  			else
  			{
  				contentString.push_back(character);
  			}
  			break;
  		case '\t':
  			scope++;
  			lastCharacter = character;
  			break;
  		case '\n':
  			if (element == false)
  			{
  				contentString.push_back(character);
  				appendScope(scopeContent, scope, contentString);
  			}
  			CompiledHTML << contentString << "\n";
  			scope = 1;
  			++linenum;
  			element = false;
  			contentString = "";
  			lastCharacter = character;
  			break;
  		case ':':
  			if (characterCheck)
  			{
  					appendScope(scopetags, scope, contentString);
  			}
  			element = true;
  			if ( linenum > 0 && elementString == "")
  			{
  				std::cerr << " > ERROR L:" << linenum << " > Element is missing!\n";
  			}
  			characterCheck = false;
  			setScope(scopeElement, scope, elementString);
  			appendScope(scopetags, scope, "");


  			userComponent = compileComponent(scopeElement[scope]);
  			if(userComponent.getElement() != "null")
  			{
  				CompiledHTML << userComponent.getElement();
  				setScope(scopeElement, scope, "");
  				setScope(scopetags, scope, "");
  				scopeElement[scope] = "component";
  				scopetags[scope] = "";
  			}
  			else
  			{
  				CompiledHTML << "<"<< scopeElement[scope] << scopetags[scope] << ">\n";
  				setScope(scopetags, scope, "");
  				lastscope = scope;
  			}
  			//}
  			elementString = "";
  			contentString = "";
  			break;
  		default:
  			if (lastCharacter != '\n' && lastCharacter != '\r' && lastCharacter != '\t')
  			{
  				if (scope < lastscope)
  				{
  					for (unsigned i = lastscope; i > scope; --i)
  					{
  						if (scopeElement[i] != "" && scopeElement[i] != "component")
  						{
  						CompiledHTML << "</"<< scopeElement[i] << ">\n";
  						scopeElement[i] = "";
  						}
  					}
  					lastscope = scope;
  				}
  			}
  			if (lastCharacter == ':')
  			{
  				std::cerr << " > ERROR L:" << linenum << " > Characters found on the right side of ':'.\n";
  			}

  			if (characterCheck)
  			{
  				if (element == true)
  				{
  					elementString.push_back(character);
  				}
  				else
  				{
  					contentString.push_back(character);
  				}
  			}
  			else
  			{
  			contentString.push_back(character);
  			}
  			break;
  		}
      lastCharacter = character;
    }
    else
    {
      contentString.push_back(character);
      escape = false;
    }
    //End of parser
	}
	if (element == false)
	{
		contentString.push_back('\n');
		appendScope(scopeContent, scope, contentString);
	}
	CompiledHTML << contentString << "\n";
	scope = 1;
	for (unsigned i = lastscope; i > scope-1; --i)
	{
		CompiledHTML << "</"<< scopeElement[i] << ">\n";
		scopeElement[i] = "";
	}
	return CompiledHTML;
}
