/*
 * BaseSimpleCurve.cpp
 *
 *  Created on: Jun 6, 2013
 *      Author: phcostello
 */

#include "BaseSimpleCurve.h"
#include <algorithm>

BaseSimpleCurve::BaseSimpleCurve(): length_(0),
										fitted(false)
{

}

BaseSimpleCurve::~BaseSimpleCurve() {
}


bool BaseSimpleCurve::ExpiryLessThan (const Wrapper<BaseInstrument> & it1,const Wrapper<BaseInstrument> & it2)
{
	return BaseInstrument::ExpiryLessThan(*it1, *it2);
}


void BaseSimpleCurve::addInstrument( const BaseInstrument& Instrument) {

	Wrapper< BaseInstrument> pInstrument(Instrument);

	vecInstruments.push_back( pInstrument);
	sort(vecInstruments.begin(),vecInstruments.end(), ExpiryLessThan);

	length_ += 1;

}

int BaseSimpleCurve::length() {

	return length_;
}
