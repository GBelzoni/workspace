/*
 * AnalyticFormulas.cpp
 *
 *  Created on: Feb 14, 2013
 *      Author: phcostello
 */

#include <cmath>
#include "AnalyticFormulas.h"

#if !defined(_MSC_VER)
using namespace std;
#endif

double ZCB( double r,
			double Expiry)
{
	return exp( -r * Expiry);

}

double ForwardContract( double r,
				double d,
				double Spot,
				double Strike,
				double Expiry)
{
	return exp(-r*Expiry) * (exp((r-d)*Expiry)*Spot-Strike);
}
