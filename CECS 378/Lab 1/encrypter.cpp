//#include <C:\Users\theco\Desktop\CSULB\CECS_378\Lab_1\cipher.h>
//#include <C:\Users\theco\Desktop\CSULB\CECS_378\Lab_1\cipher.cpp>
#include <iostream>

// takes in a string of plain text and a cipher as a key, and returns the text encrypted by that key
std::string encrypt(std::string plain_text, cipher key)
{
    std::string code_text; // it's a surprise tool that can help us later
    

    for(auto i = plain_text.begin(); i != plain_text.end(); i++) // iterates through plain_text
    {
        char storage;
        
        if (*i >= 'A' && *i <= 'Z') // if uppercase
        {
            storage = key[(*i) + 32]; // store the lowercase encrypted value
        }
        else if (*i >= 'a' && *i <= 'z')// if lowercase
        {
            storage = key[(*i)]; // store the encrypted value
        }
        else // if not a letter
        {
            storage = *i; // copy it over
        }


        code_text.push_back(storage); // save in code_text
    }
    return code_text;
}

