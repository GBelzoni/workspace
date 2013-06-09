/*
 * LinearZeroesInnerCurve.cpp
 *
 *  Created on: Jun 5, 2013
 *      Author: phcostello
 */

#include "LinearZeroesInnerCurve.h"
#include <exception>
#include <vector>
#include <iostream>


LinearZeroesInnerCurve::LinearZeroesInnerCurve()
{
	 fitted = false;
}

LinearZeroesInnerCurve::~LinearZeroesInnerCurve() {
}


void LinearZeroesInnerCurve::add_DF(const InstrumentDF df) {

	//If first instrument then also add o.n. rate so 2-points to interp with
	if(this->length() ==  0)
	{
		double thisCcr = df.getCcr();
		InstrumentDF overnight_Df;
		overnight_Df.fromCcr(thisCcr, 0.004); //0.004 = 1/250 = approx dayfrac for one trading day
		curve_dfs.push_back(overnight_Df);


	}
	curve_dfs.push_back(df);
	std::sort( curve_dfs.begin(), curve_dfs.end(), InstrumentDF::ExpiryLessThan);

}

InstrumentDF LinearZeroesInnerCurve::get_DF(double Expiry) const
{
	///This return InstrumentDF constructed using interpped zero

	//Check if curve has bee fitted yet
	if( !fitted)
	{
		throw CurveNotFitted();
	}
	//

	double ccr;
	ccr = (*fitted_linear_interpolator)(Expiry,true);
	InstrumentDF df;
	df.fromCcr(ccr,Expiry);
	return(df);


}

void LinearZeroesInnerCurve::fit_curve() {

	x.resize( this->length());
	y.resize( this->length());

	//Check if length of df vector is > 1
	if( this->length() < 2)
	{
		throw NeedMoreDfs();

	}
	//If so read in expiries into x and ccr's into ys
	std::vector< InstrumentDF>::iterator it;

	//Below loops over it1 which is rows of result table, and pushback the
	//the member getters from it2 which loops over the dfs in the inner curve
	int i;
	for(it = curve_dfs.begin(), i=0 ; it != curve_dfs.end(); ++it, ++i)
	{

		x[i] = it->getExpiry();
		y[i] = it->getCcr();

	}
	//Then make interpolator and point to shared pointer data member
	//we do this by setting the shared pointer equal to new interpolator
	//maybe swap this for wrappper pointer
	fitted_linear_interpolator.reset(new QuantLib::LinearInterpolation( x.begin() , x.end() , y.begin()));
	fitted = true;

}

BaseInnerCurve* LinearZeroesInnerCurve::clone() const {

	return new LinearZeroesInnerCurve(*this);
}

BaseInnerCurve* LinearZeroesInnerCurve::clone() {

	return new LinearZeroesInnerCurve(*this);
}
