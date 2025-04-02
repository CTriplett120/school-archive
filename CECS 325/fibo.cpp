// Author: Cole Triplett
// CECS 325-02 Prog 0
// Due 9/5/24
#include <iostream> //library for cin and cout
using namespace std; // allows shortcuts

// Fibo functino
int fibo(int n)
{
	if (n == 1 || n == 0)
		return 1;
	else
		return fibo(n - 1) + fibo(n - 2);

}

int main()
{
	for (int i = 0; i <= 20; i++)
		cout << i << ':' << fibo(i) << endl;

	return 0;


}

