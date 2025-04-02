#include <C:\Users\theco\Desktop\CSULB\CECS_378\Lab_1\message_guesser.cpp>
#include <C:\Users\theco\Desktop\CSULB\CECS_378\Lab_1\encrypter.cpp>
#include <C:\Users\theco\Desktop\CSULB\CECS_378\Lab_1\decrypter.cpp>
#include <iostream>
#include <vector>

int main()
{
	// Part 1
	/*
	cout << "Part 1:" << endl;

	std::vector<string> file_paths = { "C:\\Users\\theco\\Desktop\\CSULB\\CECS_378\\Lab_1\\words_alpha.txt" };

	std::vector<string> x = letter_combinations(file_paths, 4, 50); // 4-letter combos

	std::vector<string> z = letter_combinations(file_paths, 3, 100); // 3-letter combos

	cout << "Letter combinations determined." << endl;

	// converting strings of combinations into candidate ciphers
	std::vector<cipher> y = convert_letter_combinations(read_in_crypto_code(1, "encrypted_text.txt"), x);

	std::vector<cipher> a = convert_letter_combinations(read_in_crypto_code(1, "encrypted_text.txt"), z);



	y.insert(y.end(), a.begin(), a.end()); // combining candidate ciphers together


	y = recombine_ciphers(y); // cipher recombination

	cout << "Cipher recombining resulted in " << y.size() << " candidate keys." << endl;

	*/






	// Part 2

	cipher key;
	for (char c = 'a'; c < 'z'; c++) // he did it! he said the name of the language!
		// this iterates from a to y btw
	{
		key[c] = c + 1;
	}
	key['z'] = 'a';
	// now we have a simple +1 transposition key



	// let's switch some random things around

	key['j'] = 'd' + 1;
	key['d'] = 'j' + 1;
	key['n'] = 'v' + 1;
	key['v'] = 'n' + 1;

	cout << "Key: " << endl;
	key.print();



	for (int i = 1; i < 4; i++) // for phrases 1-3
	{
		std::string temp;
		char check;
		std::string plaintext;
		std::ifstream fin;
		fin.open("C:\\Users\\theco\\Desktop\\CSULB\\CECS_378\\Lab_1\\plaintext_code.txt");

		// loops until the problem number has been found
		while (true)
		{
			check = fin.get();
			if (check == i + '0')
			{
				fin.get(); // goes past the .
				break;
			}
		}
		while (fin >> temp)
		{
			
			plaintext += temp;
			check = fin.get();
			if (check != '\n')
			{
				plaintext.push_back(' ');
			}
			else
			{
				break;
			}
			
		}



		cout << "Plaintext: \n" << plaintext << '\n' << endl;
		

		std::string codetext = encrypt(plaintext, key);

		cout << "Encrypted text: \n" << codetext << '\n' << endl;
		
		std::string decryptedtext = decrypt(codetext, key);

		cout << "Decrypted text: \n" << decryptedtext << '\n' << endl;

	}







	return 0;
};