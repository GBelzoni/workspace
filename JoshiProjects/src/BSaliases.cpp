/*
 * BSaliases.cpp
 *
 *  Created on: Apr 6, 2013
 *      Author: phcostello
 */


#include "BSaliases.h"
#include <BlackScholesFormulas.h>


BSCallSpot::BSCallSpot(double r_,
							double d_,
							double T_,
							double Vol_,
							double Strike_)
							:
							r(r_),d(d_),T(T_),Vol(Vol_),Strike(Strike_)
{}

double BSCallSpot::operator ()(double Spot) const {

	return BlackScholesCall(Spot,Strike,r,d,Vol,T);

}
