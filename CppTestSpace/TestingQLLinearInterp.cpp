/*
 * TestingQLLinearInterp.cpp
 *
 *  Created on: Jun 5, 2013
 *      Author: phcostello
 */


#include <vector>
#include <iostream>
#include <ql/math/interpolations/linearinterpolation.hpp>
#include <exception>


using namespace std;
using namespace QuantLib;


int main()
{
	try
	{
		std :: vector < Real > xVec (5) , yVec ( xVec . size ());
		xVec[0]=0.0;
		xVec[1]=1.0;
		xVec[2]=2.0;
		xVec[3]=3.0;
		xVec[4]=4.0;

		yVec[0]= std::exp(0.0);
		yVec[1]= std::exp(1.0);
		yVec[2]= std::exp(2.0);
		yVec[3]= std::exp(3.0);
		yVec[4]= std::exp(4.0);
		LinearInterpolation linInt( xVec.begin() , xVec.end() , yVec.begin());
		std::cout << "Exp at 0.0 " << linInt(0.0) << std::endl;
		std::cout << "Exp at 0.5 " << linInt(0.5) << std::endl;
		std::cout << "Exp at 1.0 " << linInt(1.0) << std::endl;

		std::cout << "Exp at 5.0 extrapolated " << linInt(5.0,true) << std::endl ;
		std::cout << "Exp at 5.0 actual " << std::exp(5.0) << std::endl ;
	}
	catch(exception& e)
	{
		std::cout << e.what() << std::endl;
	}



	return(0);
}
