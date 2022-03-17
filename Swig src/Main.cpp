#include <vector>
#include <new>
#include <memory>
#include <algorithm>
#include "swigh.hpp"
#include "swig.hpp"
#include "swigs.hpp"

const std::string VERSION_NUM = "0.1.0";

int main(int argc, char *argv[])
{
	std::string sourceCIN;
	std::string fileName;

	std::vector<std::string> CMDArguments(argv, argv + argc);
	unsigned i = 0;
	std::string inLine = "";

	i = 0;
	for (const auto& separateCIN : CMDArguments)
    {
		if (i == 1)
		{
			if (separateCIN == "-sh" || separateCIN == "-s" || separateCIN == "-ss")
			{
				//-sh = Heirchy  -s = Component  -ss = Style
				inLine = separateCIN;
			}
			if (inLine == "") break;
		}
		else if (i == 2 && (inLine == "-sh" || inLine == "-s" || inLine == "-ss"))
		{
			fileName = separateCIN;
			break;
		}
		++i;
    }
	//Terminal command arguments
	if(inLine == "-sh")//Heirchy File
	{
		std::fstream fin(fileName + ".swigh", std::fstream::in);
		std::string source = compileHeirchy(fin).str();
		fin.close();
		std::ofstream ofs;
		ofs.open(fileName+".html", std::ofstream::out | std::ofstream::trunc);
		ofs.close();
		std::fstream compiledFile(fileName + ".html", std::ofstream::out | std::ofstream::trunc);
		compiledFile << source;
		compiledFile.close();
	}
	else if(inLine == "-s")//Component file
	{
		std::fstream fin(fileName + ".swig", std::fstream::in);
	}
	else if(inLine == "-ss")//Style file
	{
		std::fstream fin(fileName + ".swigs", std::fstream::in);
	}
	else
	{
		std::cout << "Swig - VER:" << VERSION_NUM << "\n\n   Commands:\n \"-sh\" - Compile a swig heirchy file.  (This will compile all linked files aswel.)\n \"-s\" - Compile a component file.  (This will compile only your specified component file.)\n \"-ss\" - Compile a style file.  (This will compile only your specified style file.)\n\n";
		system("pause");
	}
}
