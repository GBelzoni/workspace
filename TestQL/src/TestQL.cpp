//============================================================================
// Name        : TestQL.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include <fstream>
#include <vector>
#include <boost/timer.hpp>
#include "ql/quantlib.hpp"


using namespace std;
using namespace QuantLib;

int maintt() {
	boost::timer time;
	Date settlementDate(22, September, 2004);
	cout << settlementDate;

	vector < int > vec;
	cout << "!!!Hello World!!!" << endl; // prints !!!Hello World!!!
	return 0;
}
