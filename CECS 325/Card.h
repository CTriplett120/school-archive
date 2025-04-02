// Name: Cole Triplett
// Class: CECS 325-01
// Project Name: Prog 1 - One Card War
// Due Date: 9/19/24
//
// I certify that this program is my own original work. I did not copy any part of this program from
// any other source. I further certify that I typed each and every line of code in this program.



#ifndef CARD_H
#define CARD_H


using namespace std;



class Card
{
private:
	char suit;
	int val;
	
	
public:
	Card(char suit, char val);			// card constructor, sets suit and rank
	Card();								// default card
	void print();						// displays card (ex: AS, 10C, JD)
	int compare(Card);					// compares to another card, returns 1 for win, 0 for tie, and -1 for loss
};
#endif
