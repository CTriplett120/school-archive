// Name: Cole Triplett
// Class: CECS 325-01
// Project Name: Prog 1 - One Card War
// Due Date: 9/19/24
//
// I certify that this program is my own original work. I did not copy any part of this program from
// any other source. I further certify that I typed each and every line of code in this program.




#include "Card.h"
#include "Deck.h"
#include <iostream>
using namespace std;



int main()
{
	// setup

	Deck d;
	string players[2];
	

	// player input

	cout << "Enter p1 name: ";
	cin >> players[0];

	cout << "Enter p2 name: ";
	cin >> players[1];


	// display

	cout << endl << " Original Deck" << endl;
	d.print();
	d.shuffle();

	cout << " Shuffled Deck" << endl;
	d.print();


	// dealing

	Card deck1[26];
	Card deck2[26];

	for (int i = 0; i < 26; i++)
	{
		deck1[i] = d.deal();
		deck2[i] = d.deal();
	}


	// games

	int wins1 = 0;
	int wins2 = 0;
	int ties = 0;



	for (int i = 0; i < 26; i++)
	{
		cout << "Game " << i + 1 << endl << "-----------" << endl;
		cout << players[0] << " => ";
		deck1[i].print();
		cout << endl;
		cout << players[1] << " => ";
		deck2[i].print();
		cout << endl;


		int result = deck1[i].compare(deck2[i]);
		if (result == 1)
		{
			wins1 += 1;
			cout << players[0] << ": Winner" << endl << endl;
		}
		else if (result == 0)
		{
			ties += 1;
			cout << "Tie" << endl << endl;
		}
		else
		{
			wins2 += 1;
			cout << players[1] << ": Winner" << endl << endl;
		}

	}
	

	// final stats

	cout << "-----Final Stats-----" << endl;
	cout << players[0] << " vs. " << players[1] << endl;
	cout << "Wins:   " << wins1 << "     " << wins2 << endl;
	cout << "Losses: " << wins2 << "     " << wins1 << endl;
	cout << "Ties:   " << ties << "      " << ties << endl;
}