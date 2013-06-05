/*
 * VanillaPayOffs.cpp
 *
 *  Created on: Apr 6, 2013
 *      Author: phcostello
 */

#include "VanillaPayOffs.h"


// Digital Call PayOff
PayOffDigitalCall::PayOffDigitalCall(double Strike_): Strike(Strike_)
{
}

double PayOffDigitalCall::operator ()(double Spot) const
{
	return Spot > Strike ? 1 : 0;
}

PayOff* PayOffDigitalCall::clone() const
{
 return new PayOffDigitalCall(*this);

}

//Digital Put PayOff
PayOffDigitalPut::PayOffDigitalPut(double Strike_): Strike(Strike_)
{
}

double PayOffDigitalPut::operator ()(double Spot) const
{
	return Spot > Strike ? 0 : 1;
}

PayOff* PayOffDigitalPut::clone() const
{
 return new PayOffDigitalPut(*this);

}

