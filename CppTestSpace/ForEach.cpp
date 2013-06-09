/*
 * ForEach.cpp
 *
 *  Created on: Apr 23, 2013
 *      Author: phcostello
 */

#include <vector>
#include <boost/foreach.hpp>
#include <iostream>


using namespace std;

int main()
{

	vector<double> SpotSeq(10);
	vector<double> StrikeSeq(10);


	BOOST_FOREACH( double& y, StrikeSeq)
	{
		y=10;
		BOOST_FOREACH( double &x, SpotSeq)
			{
				x=20;
			}
	}

	BOOST_FOREACH( double y, StrikeSeq)
		BOOST_FOREACH( double x, SpotSeq)
			cout << "(X,Y) = "<< x<< " , "<< y << endl;








	return 0;
}


