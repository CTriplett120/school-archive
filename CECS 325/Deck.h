// Name: Cole Triplett
// Class: CECS 325-01
// Project Name: Prog 1 - One Card War
// Due Date: 9/19/24
//
// I certify that this program is my own original work. I did not copy any part of this program from
// any other source. I further certify that I typed each and every line of code in this program.



#ifndef DECK_H
#define DECK_H
#include "Card.h"

class Deck
{
private:
	Card deck[52];
public:
	
	Deck();
	Card deal();
	void print();
	void shuffle();
};







#endif // !DECK_H

