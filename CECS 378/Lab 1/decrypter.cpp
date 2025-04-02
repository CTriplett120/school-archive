//#include <C:\Users\theco\Desktop\CSULB\CECS_378\Lab_1\cipher.h>
//#include <C:\Users\theco\Desktop\CSULB\CECS_378\Lab_1\cipher.cpp>
#include <iostream>

// takes in a string of encrypted text and a cipher as a key, and returns the plain text decrypted by that key
std::string decrypt(std::string code_text, cipher key)
{
    std::string plain_text; // it's a surprise tool that can help us later
    
    for (auto i = code_text.begin(); i != code_text.end(); i++) // iterates through plain_text
    {
        for(char k = 'a'; k <= 'z'; k++) // iterates through cipher
        {
            if (key[k] == *i) // if text matches
            {    
                plain_text.push_back(k); // save in plain_text
                break; // may as well not keep going
            }
            else if (*i > 'z' || *i < 'a') // if non-alphabetical
            {
                plain_text.push_back(*i); // save that in plain_text
                break; // let's not put in 26 whitespaces (based on a true story)
            }
        }
        
    }
    return plain_text;

}