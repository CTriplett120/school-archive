// Name: Cole Triplett
// Class: CECS 325-01
// Project Name: Prog 1 - One Card War
// Due Date: 9/19/24
//
// I certify that this program is my own original work. I did not copy any part of this program from
// any other source. I further certify that I typed each and every line of code in this program.



#include "Card.h"
#include <iostream>
#include <string>

using namespace std;





		Card::Card()
		{
			suit = 'S';
			val = 0;
			
		}

		Card::Card(char s, char v)
		{
			suit = s;
			if (v > 47 && v < 58)
			{
				val = v - 48;
			}
			else if (v == 'J')
			{
				val = 10;
			}
			else if (v == 'Q')
			{
				val = 11;
			}
			else
			{
				val = 12;
			}


		}


		void Card::print()
			
		{
			string vstring = "0";
			
			if (val == 0)
			{
				vstring[0] = 'A';
			}
			else if (val < 9)
			{
				vstring[0] = val + 49;
				
			}
			else if (val == 9)
			{
				vstring = "10";
				
			}

			else if (val == 10)
			{
				vstring = "J";
			}
			else if (val == 11)
			{
				vstring = "Q";
			}
			else if (val == 12)
			{
				vstring = "K";
			}
			else { vstring = "0"; }

			cout << vstring << suit << ' ';
			
		}

		int Card::compare(Card c)
		{
			if (c.val < val)
			{
				return 1;
			}
			else if (c.val == val)
			{
				return 0;
			}
			else { return -1; }
		}
