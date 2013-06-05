/*
 * BaseInnerCurve.cpp
 *
 *  Created on: Jun 5, 2013
 *      Author: phcostello
 */


#include "BaseInnerCurve.h"
#include <algorithm>
#include "InstrumentDF.h"

BaseInnerCurve::BaseInnerCurve() : number_dfs(0) {

}

BaseInnerCurve::~BaseInnerCurve() {
	// TODO Auto-generated destructor stub
}

void BaseInnerCurve::add_DF(InstrumentDF df) {

	curve_dfs.push_back(df);
	std::sort( curve_dfs.begin(), curve_dfs.end(), InstrumentDF::ExpiryLessThan);

}

std::vector<std::vector<double> > BaseInnerCurve::GetDFList() {


	std::vector<std::vector<double> >  rtrn;
	rtrn.resize( curve_dfs.size());


	std::vector<std::vector<double> >::iterator it1;
	std::vector< InstrumentDF>::iterator it2;

	//Below loops over it1 which is rows of result table, and pushback the
	//the member getters from it2 which loops over the dfs in the inner curve
	for( it1 = rtrn.begin(), it2=curve_dfs.begin(); it1 != rtrn.end(); ++it1, ++it2)
	{
		it1->push_back(it2->getDf());
		it1->push_back(it2->getExpiry());

	}
	return(rtrn);

}

int BaseInnerCurve::length() {

	return( curve_dfs.size());
}


//Derived class with empty implementation of virtual functions for testing of base class
InnerCurveForBaseTest::InnerCurveForBaseTest() {
}

double InnerCurveForBaseTest::get_DF(double Expiry) {

	return(0);
}

void InnerCurveForBaseTest::fit_curve() {
}
