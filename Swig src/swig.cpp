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

std::string parseVariables(std::string input, std::vector<std::string> Classvariables, std::vector<std::string> IDvariables)
{
  //std::cerr << input << "\n";
  for(std::string i : Classvariables)
  {
    //std::cerr << i << "\n";
    if(input == i) return "document.getElementsByClassName(\"" + input + "\")";
  }
  for(std::string i : IDvariables)
  {
    //std::cerr << i << "\n";
    if(input == i) return "document.getElementById(\"" + input + "\")";
  }
  return input;
}

std::string compileScript(char character, std::vector<std::string> & elementIDVariables, std::vector<std::string> & elementClassVariables, std::stringstream & compiledJavascript, std::string & scriptWordStream)
{
  switch(character)
  {
    case ' ':
      compiledJavascript << parseVariables(scriptWordStream, elementClassVariables, elementIDVariables);
      scriptWordStream = "";
      compiledJavascript << std::string(1, character);
      break;
    case '\t':
      compiledJavascript << parseVariables(scriptWordStream, elementClassVariables, elementIDVariables);
      scriptWordStream = "";
      compiledJavascript << std::string(1, character);
      break;
    case '\n':
      compiledJavascript << parseVariables(scriptWordStream, elementClassVariables, elementIDVariables);
      scriptWordStream = "";
      compiledJavascript << std::string(1, character);
      break;
    case '+':
      compiledJavascript << parseVariables(scriptWordStream, elementClassVariables, elementIDVariables);
      scriptWordStream = "";
      compiledJavascript << std::string(1, character);
      break;
    case '=':
      compiledJavascript << parseVariables(scriptWordStream, elementClassVariables, elementIDVariables);
      scriptWordStream = "";
      compiledJavascript << std::string(1, character);
      break;
    case '.':
      compiledJavascript << parseVariables(scriptWordStream, elementClassVariables, elementIDVariables);
      scriptWordStream = "";
      compiledJavascript << std::string(1, character);
      break;
    case '[':
      compiledJavascript << parseVariables(scriptWordStream, elementClassVariables, elementIDVariables);
      scriptWordStream = "";
      compiledJavascript << std::string(1, character);
      break;
    case '-':
      compiledJavascript << parseVariables(scriptWordStream, elementClassVariables, elementIDVariables);
      scriptWordStream = "";
      compiledJavascript << std::string(1, character);
      break;
    default:
      scriptWordStream.push_back(character);
  }

}


component compileComponent(std::string componentName, std::vector<std::string> & elementIDVariables, std::vector<std::string> & elementClassVariables, bool SRCparsing)
{
  std::string IDString = "";
  std::string ClassString = "";
    std::string scriptWordStream;
    component htmlComponent;
    component userComponent;
    std::stringstream compiledElement;
    std::stringstream compiledJavascript;
    std::ifstream componentFile;
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
    bool sqrbrackets = false;
    bool escape = false;

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
    if (SRCparsing)
    {
      compileScript(character, elementIDVariables, elementClassVariables, compiledJavascript, scriptWordStream);
    }
    else
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
          if (sqrbrackets == false)
          {
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
                  compiledElement << "</"<< scopeElement[i] << ">\n";
                  scopeElement[i] = "";
                }
              }
            }
            else if (scope == lastscope)
            {
              if (scopeElement[scope] != "")
              {
                compiledElement << "</"<< scopeElement[scope] << ">\n";
              }
            }
            characterCheck = true;
            element = true;
          }
          else
          {
            contentString.append("#");
          }
          break;
        case '(':
          if (characterCheck && sqrbrackets == false)
          {
            ClassString = "";
            contentString.append(" class = \"");
          }
          else
          {
            contentString.push_back(character);
          }
          break;
        case ')':
          if (characterCheck && sqrbrackets == false)
          {
            elementClassVariables.push_back(ClassString);
            contentString.append("\" ");
          }
          else
          {
            contentString.push_back(character);
          }
          break;
        case '[':
          sqrbrackets = true;
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
          sqrbrackets = false;
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
            IDString = "";
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
            elementIDVariables.push_back(IDString);
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
          if (contentString == "=SRC=" ||
           contentString == "=script=" ||
           contentString == "=Script=" ||
              contentString == "=src=" ||
              contentString == "=Src=" ||
           contentString == "=source=" ||
           contentString == "=Source=" ||
           contentString == "=SOURCE=" ||
           contentString == "=SCRIPT=" ||
               contentString == "=JS=" ||
               contentString == "=js=" ||
       contentString == "=javascript=" ||
       contentString == "=Javascript=" ||
       contentString == "=JavaScript=" ||
          contentString == "=JAVASCRIPT=")
          {
            SRCparsing = true;
          }
          else
          {
            if (element == false)
            {
              contentString.push_back(character);
              appendScope(scopeContent, scope, contentString);
            }
            compiledElement << contentString << "\n";
          }
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


          userComponent = compileComponent(scopeElement[scope], elementIDVariables, elementClassVariables);
          if(userComponent.getElement() != "null")
          {
            compiledElement << userComponent.getElement();
            setScope(scopeElement, scope, "");
            setScope(scopetags, scope, "");
            scopeElement[scope] = "component";
            scopetags[scope] = "";
          }
          else
          {
            compiledElement << "<"<< scopeElement[scope] << scopetags[scope] << ">\n";
            setScope(scopetags, scope, "");
            lastscope = scope;
          }
          //}
          elementString = "";
          contentString = "";
          break;
        default:
          ClassString.push_back(character);
          IDString.push_back(character);
          if (lastCharacter != '\n' && lastCharacter != '\r' && lastCharacter != '\t')
          {
            if (scope < lastscope)
            {
              for (unsigned i = lastscope; i > scope; --i)
              {
                if (scopeElement[i] != "" && scopeElement[i] != "component")
                {
                compiledElement << "</"<< scopeElement[i] << ">\n";
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
	}
  if (element == false)
	{
		contentString.push_back('\n');
		appendScope(scopeContent, scope, contentString);
	}
	compiledElement << contentString << "\n";
	scope = 1;
	for (unsigned i = lastscope; i > scope-1; --i)
	{
		compiledElement << "</"<< scopeElement[i] << ">\n";
		scopeElement[i] = "";
	}
    htmlComponent.setElement(compiledElement.str());
    htmlComponent.setScript(compiledJavascript.str());
    componentFile.close();
    return htmlComponent;
}
