#include <C:\Users\theco\Desktop\CSULB\CECS_378\Lab_1\cipher.h>
#include <C:\Users\theco\Desktop\CSULB\CECS_378\Lab_1\cipher.cpp>
#include <iostream>
#include <vector>
#include <map>
#include <fstream>
#include <queue>
#include <cmath>

using namespace std;

// scans files in file_paths for words and outputs a vector of strings containing the N most common combinations of length cardinality.
vector<string> letter_combinations(vector<string> file_paths, int cardinality, int n)

{

    // setup

    map<string, int>* ranking = new map<string, int>; // stores frequency of cardinality-letter combos
    
    ifstream fin; // file input stream
    string storage;
    
    
    fin >> noskipws; // this disables the automatic skipping over of whitespaces/newlines during file input, which will be important shortly
    

    // main loop
    
    for(int i = 0; i < file_paths.size(); i++) // for every file we want to look at
    {
        fin.open(file_paths[i]); // open said file

        while (fin >> storage) // copies one section (seperated by a whitespace/newline) into storage at a time
        // this will seperate every word in a dictionary (like words_alpha) but leave paragraphs together in written works
        // we want this behavior, as spaces will be removed in our encrypted message, making words that often follow others part of our analysis
        {
            storage += fin.get(); // this copies the whitespace/newline itself into our storage array 
            
            
            if (storage[storage.size() - 1] == '\n') // if we've reached the end of our section (paragraph or word)
            {
                storage.erase(remove(storage.begin(), storage.end(), ' ')); // let's get rid of those spaces
                
                for (int k = 0; k < int(storage.size()) - cardinality; k++) // iterates through storage, covering letter combinations until there isn't any more room 
                {
                    
                    // combo stores the cardinality-length letter combo at storage[k]
                    string combo;
                    for (int l = 0; l < cardinality; l++)
                    {
                        combo += storage[k + l];
                    }
                    (*ranking)[combo]++; // increment the rank of that combo by 1
                    
                }
                
            }

            fin >> ws; // skips over whitespace, allowing us to move on to the next word
            
        }
        
        
        fin.close(); // close the file
    }
    
    
    
    vector<string> candidate_combos; // stores the combinations to be returned
    


// copilot helped me design this part

///////////////////////////////////////////////////////////////////////////////////

            
    // Priority queue to keep track of top n key-value pairs
    // We use a min-heap to keep the smallest value at the top
    auto cmp = [](const pair<string, int>& left, const pair<string, int>& right) // this defines the lambda function that sorts the things in the queue
    {
        return left.second > right.second;
    };
    priority_queue<pair<string, int>, vector<pair<string, int>>, decltype(cmp)> pq(cmp);

    // Iterate through the map and push key-value pairs into the priority queue
    for (const auto& kv : *ranking)
    {
        pq.push(kv);
        // Maintain the size of the heap to be n
        if (pq.size() > n)
        {
            pq.pop();
        }
    }

    // After our top n have been determined, extract them from the priority queue into candidate_combos
    
    while (!pq.empty()) {
        candidate_combos.push_back(pq.top().first);
        pq.pop();
    }

    reverse(candidate_combos.begin(), candidate_combos.end());


///////////////////////////////////////////////////////////////////////////////////
    
            

    // cleanup (aka the no memory leaks zone)
    delete ranking;
    ranking = nullptr;

    return candidate_combos;
}

// reads in code from designated text file for the specified problem (I don't want to rewrite this every time I need to do it)
string read_in_crypto_code(int problem, string file)

{
    if (problem > 4)
    {
        throw "Invalid problem number";
    }

    ifstream fin;
    fin.open("C:\\Users\\theco\\Desktop\\CSULB\\CECS_378\\Lab_1\\" + file);
    string code;
    char current;
    bool satisfied = false;
    int tracker = 0;

    while (!satisfied) // loop until we find the problem we want
    {
        current = fin.get();

        if (current == '.') // check for the "." that appear after problem #'s
        {
            if (++tracker == problem) // increment tracker, then check it against problem #
            {
                fin.get(); // skips the newline right after the "." 
                
                while(current != '\n') // goes until next line
                {
                    current = fin.get();
                    if (current != ' ') // let's not include whitespace
                    {
                        if (current > 'a') // if lowercase
                        {
                            code += current;
                        }
                        else // if uppercase
                        {
                            code += current + 32; // copy in lowercase value
                        }

                    }
                }
                satisfied = true;
            }
        }
    }
    return code;

}

// takes in a vector of candidate ciphers and combines those that have no conflicts
vector<cipher> recombine_ciphers(vector<cipher> starting_list)
{
    vector<cipher> new_list;
    cipher null;


    int total = 0;
    for(auto i = starting_list.begin(); i != starting_list.end(); i++) // for every entry in the list
    {
        
        new_list.push_back(*i); // add the entry itself
        for (auto j = i + 1; j != starting_list.end(); j++) // for every entry later on in the list (prevets redoing existing combos and combo with self)
        {
            
            
            cipher candidate = combine(*i, *j);
            if(!(candidate == null)) // if the combine was successful
            {
                new_list.push_back(candidate);
                //cout << ++total << ": candidate added\n";
            }
            
            
            
            
            
        }
    }

    return new_list;
}

// takes in a string of encrypted text and a vector of strings from letter_combinations, and generates cipers for common phrases in the encrypted text
vector<cipher> convert_letter_combinations(string crypto_code, vector<string> combinations)
{
    map<string, int> ranking; // this works very similarly to letter_combinations, but this time we're scanning the crypto_code string

    for (int k = 0; k < int(crypto_code.size()) - int(combinations[0].size()); k++) // iterates through crypto_code, covering letter combinations until there isn't any more room 
    {
                    
        // combo stores the combination-length letter combo at storage[k]
        string combo;
        for (int l = 0; l < combinations[0].size(); l++)
        {
            combo += crypto_code[k + l];
        }
        ranking[combo]++; // increment the rank of that combo by 1
         
        
    }
    vector<cipher> ciphers; // this will store our ciphers to be returned


    // iterate through the map and check for things with high ranking ()
    for (auto i = ranking.begin(); i != ranking.end(); i++) // for every spot in the ranking
    {
        if (i->second > 1) // if the phrase appears above our threshold (more than once)
        {
            //cout << "Phrase: " << i->first << endl;            
            for(int j = 0; j < combinations.size(); j++) // iterate though all letter combinations
            {
                cipher candidate;
                for(int k = 0; k <combinations[j].size(); k++) // for the letters in combination j
                {
                    candidate[i->first[k]] = combinations[j][k];
                }
                ciphers.push_back(candidate); // add cipher into list
            }
        }
    }

    

    return ciphers;

}


// takes in a string of encoded text and decodes it using a cipher. decoded text will be uppercase to allow for differentiaton of partially decoded sections
string decoder(string text, cipher key)
{
    string decoded_text;
    for (auto i = text.begin(); i != text.end(); i++) // iterate through the text
    {
        if(key[*i]) // if there is a valid mapping in our key
        {
            decoded_text.push_back(key[*i] - 32); // adds uppercase version of mapping to output string
        }
        else
        {
            decoded_text.push_back(*i); // adds unchanged text to output string
        }
    }
    return decoded_text;
}


// takes in partially decoded text and checks for a threshold% that belong to coherent words
bool success_checker(string text, float threshold)
{
    if (threshold > 1.0 || threshold < 0.0)
    {
        throw "Threshold must be a fraction";
    }




}



