#pragma once
#include <map>


class cipher
{
private:
    std::map<char, char> sub_storage;
public:
    cipher();

    char& operator[] (char);
    
    bool operator== (const cipher);
    
    // function that combines two ciphers if they do not conflict. Returns a null cipher if they do.
    friend cipher combine(cipher, cipher);

    void print();

    void integrity_check();
};
