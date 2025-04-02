#include <map>
#include <C:\Users\theco\Desktop\CSULB\CECS_378\Lab_1\cipher.h>
#include <iostream>

cipher::cipher()
{
    /*
    for (char i = 'a'; i < 'z' + 1; i++)
    {
        sub_storage[i] = char(0);
    }
      */  
}

bool cipher::operator==(const cipher other)
{
    return this->sub_storage == other.sub_storage;
}


char& cipher::operator[](char i)
{
    return sub_storage[i];
}


cipher combine(cipher x, cipher y)
{
    cipher z;
    cipher null;

    for(char i = 'a'; i < 'z' + 1; i++) // for every letter
    {
        if (x[i] != y[i]) // if there is a mismatch
        {  
            if (x[i] != 0 && y[i] != 0) // if both have an non-null value
            {
                return null;
            }
            else if (x[i] != 0) // if x has the non-null value
            {
                z.sub_storage[i] = x[i]; // copy in x's value
            }
            else // if y has the non-null value
            {
                z.sub_storage[i] = y[i]; // copy in y's value
            }

        }
        else
        {
            if (x[i] != 0)
            {
                z.sub_storage[i] = x[i]; // copy in the agreed-upon (non-null) value
            }
        }
        
    }
    
    
    z.integrity_check();
    
    
    return z; // I can't believe this took me like 3 hours of debugging to figure out
}


void cipher::integrity_check()
{
    // check for multiple letters mapping to the same new letter
    std::map<char, bool> reference; // stores whether a letter has been mapped to
    cipher null;
    for (char i = 'a'; i < 'z' + 1; i++) // for every letter
    {
        if (sub_storage[i] != 0) // if there is a mapping
        {
            if (! reference[sub_storage[i]]) // if the letter hasn't been mapped to
            {
                reference[sub_storage[i]] = true; // store this letter as having been mapped to
            }
            else // reset cipher (I would throw an exepction but my try blocks were refusing to work)
            {
                this->sub_storage = null.sub_storage;
                break;
            }
        }
    }




    
}


void cipher::print()
{
    for (char i = 'a'; i < 'z' + 1; i++)
    {
        if (sub_storage[i] != 0)
        {
            std::cout << i << " -> " << sub_storage[i] << std::endl;  
        }
    }
}