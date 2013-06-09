/*
 * Test.cpp
 *
 *  Created on: Apr 6, 2013
 *      Author: phcostello
 */


#include <armadillo>
#include <iostream>


using namespace std;
using namespace arma;

int main(int argc, char** argv)
{
	mat A = randu<mat>(4,5);
	mat B = randu<mat>(4,5);

	cout << A*B.t() << endl;

	return 0;
}


