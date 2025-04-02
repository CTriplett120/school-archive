// Name: Cole Triplett
// Class: CECS 325-01
// Project Name: Prog 1 - One Card War
// Due Date: 9/19/24
//
// I certify that this program is my own original work. I did not copy any part of this program from
// any other source. I further certify that I typed each and every line of code in this program.
// And none caused me more pain than that bastard of a deck constructor.



#include "Deck.h"
#include <cstdlib>
#include <iostream>
#include <time.h>

Deck::Deck() 
{
	Card deck[52] = {}; //card array
	
	
	char suits[4] = { 'H', 'S', 'D', 'C' }; // suits for looping
	char values[13] = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'J', 'Q', 'K' };
	int index = 0; // int for deck traversal
	srand(time(NULL));
	
	
	for (int i = 0; i < 4; i++)
	{
		for (int j = 0; j < 13; j++)
		{
			Card c = Card(suits[i], values[j]);
			//cout << "deck[" << index - 1 << "] = ";
			//this->deck[index -1].print();
			//cout << endl;
			
			//cout << "setting index " << index << " to ";
			//c.print();
			//cout << endl;

			this->deck[index] = c; // this was very very very fun to debug
			
			//cout << "index " << index << " actually equals to ";
			//this->deck[index].print();
			//cout << endl;

			index++;
		}
	}
	
	//cout << "finished setup, final state is:" << endl;
	//cout << "index 35 is ";
	//this->deck[35].print();
	//cout << endl;
	
	
}

void Deck::shuffle()
{
	int range = 52;
	for (int i = 0; i < 52; i++)
	{
		int index1 = rand() % range;
		int index2 = rand() % range;
		Card temp = deck[index1];
		deck[index1] = deck[index2];
		deck[index2] = temp;

	}
	
	
}

Card Deck::deal() 
{
	Card d = deck[0];
	for (int i = 0; i < 52; i++)
	{
		deck[i] = deck[i + 1];
		
	}
	deck[51] = Card();
	return d;
	
}

void Deck::print()
{
	for (int i = 0; i < 4; i++)
	{
		for (int j = 0; j < 13; j++)
		{
			//cout << "printing " << j << " + " << i << " * 13 = " << j + (i * 13) << ' ';
			
			deck[j + i * 13].print();

			//cout << endl;
			//cout << "deck[35] = ";
			//this->deck[35].print();
			//cout << endl;
		}
		cout << endl;
	}
	cout << endl;
}