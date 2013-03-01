/*
 * Exceptions.cpp
 *
 *  Created on: Feb 28, 2013
 *      Author: phcostello
 */

#include<iostream>
#include<string>
#include<fstream>


using namespace std;

int main()
{
	string strIn;
	double doubleIn = 5;
	double* p = new double;
	unsigned int uI;
	char a[0];


	cout<< "Number:" << *p << endl;

	try
	{
		cout << "a" << endl;
		a[5] = 'a';
		cout << a[5] << endl;
		throw("stufff!");
	}
	catch (...)
	{
		cout<<"Error!"<< endl;
	}

	cout<< "end"<< endl;
	return 0;




}



