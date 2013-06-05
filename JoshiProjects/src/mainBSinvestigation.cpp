/*
 * main.cpp


 *
 *  Created on: Feb 14, 2013
 *      Author: phcostello
 */

#include <iostream>

#include <BlackScholesFormulas.h>
#include "AnalyticFormulas.h"
#include <vector>
#include <fstream>
#include <iostream>
#include <string>
#include <sstream>


int main__()
{

	double Spot = 100;
	double Strike = 100;
    double r = 0.05;
    double d = 0.0;
    double Vol = 0.1;
    double Expiry = 1.0;


    //Calculating functions
    double BSCprice = BlackScholesCall( Spot,
                             Strike,
                             r,
                             d,
                             Vol,
                             Expiry);

    double BSPprice = BlackScholesPut( Spot,
                                 Strike,
                                 r,
                                 d,
                                 Vol,
                                 Expiry);


    double ForwardPrice = ForwardContract( r,
		   	   	   	   	   	   	   d,
		   	   	   	   	   	   	   Spot,
		   	   	   	   	   	   	   Strike,
		   	   	   	   	   	   	   Expiry);


    std::cout << "BSC price: " << BSCprice << std::endl;
    std::cout << "BSP price: " << BSPprice << std::endl;
    std::cout << "Forward price: " << ForwardPrice << std::endl;
    std::cout << "BSC - BSP (put call parity): " << BSCprice - BSPprice << std::endl;

    //Generating vol sequences

    typedef std::vector<double>::iterator vit;

    std::vector<double> StrikeSequence;
    std::vector<double> CallvsStrike;



    for( double i=0.0 ; i <= 100; i++)
    {
    	double val = 0 + i*0.002;
    	StrikeSequence.push_back(val);
    }

    //double theStrike = 50.0;
    //Vol = 0.01;
    for( vit it = StrikeSequence.begin() ; it != StrikeSequence.end(); it++)
    {

    	double thisVol = *it;
    	double thisResult = BlackScholesDigitalCall( Spot,
    							 Strike,
    							 r,
    							 d,
    							 thisVol,
    							 Expiry);

    	CallvsStrike.push_back(thisResult);
    }

    std::string thisResult;

    std::ofstream outfile("SpotvsDigitalCallPrice_vol_1pc.csv");
    for( int i =0 ; i<= 100; i++)
    {
    	std::ostringstream sstream;
    	//Seem to have problems converting 0 to value (get very large number) so add 0.000001

    	sstream << StrikeSequence[i] << ',' << CallvsStrike[i] +0.0000001 << ' \n';
    	outfile << sstream.str() << std::endl;

    }
    outfile.close();



}



