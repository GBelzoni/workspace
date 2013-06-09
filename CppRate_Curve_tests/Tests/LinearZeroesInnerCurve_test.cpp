/*
 * LinearZeroesInnerCurve_test.cpp
 *
 *  Created on: Jun 5, 2013
 *      Author: phcostello
 */

#include "LinearZeroesInnerCurve.h"


#define BOOST_TEST_DYN_LINK
#include <boost/test/unit_test.hpp>
#include "InstrumentDF.h"
#include <vector>
//#include "BaseInnerCurve.h"

using namespace std;

BOOST_AUTO_TEST_SUITE( LinerZeroInnerCurve)

BOOST_AUTO_TEST_CASE( basic_tests )
{

	double expiry1 = 1;
	LinearZeroesInnerCurve curve;

	//Check that can't get expiry before fitted
	BOOST_CHECK_THROW(curve.get_DF(expiry1), CurveNotFitted );


	//Add two instruments
	InstrumentDF df1,df2,df3;

	df1.fromCcr(0.05,0.5);
	df2.fromCcr(0.01,1.0);
	df3.fromCcr(0.03,0.2);


	curve.add_DF(df1);
	curve.add_DF(df2);
	curve.add_DF(df3);
	BOOST_MESSAGE("df1's df = " << df1.getDf());
	BOOST_MESSAGE("df2's df = " << df2.getDf());
	BOOST_MESSAGE("df3's df = " << df3.getDf());


	int len = curve.length();
	BOOST_CHECK_EQUAL(len, 3);

	vector<vector<double> > list = curve.GetDFList();
	BOOST_CHECK_CLOSE(list[0][0], 0.994018, 0.01); //Check df
	BOOST_CHECK_CLOSE(list[0][1], 0.2, 0.01); //Check expiry
	BOOST_MESSAGE("Added one df instrument: Check df and expiry ok");

	//Fit curve
	//QuantLib::LinearInterpolation LinInt = curve.fit_curve();
	curve.fit_curve();
	BOOST_MESSAGE("Curve Fitted");
	InstrumentDF df;
	double dfval;


	df = curve.get_DF(0.3);
	dfval = df.getCcr();
	BOOST_MESSAGE("Fitted cc rate is " << dfval);
	df = curve.get_DF(0.8);
	dfval = df.getCcr();
	BOOST_MESSAGE("Fitted cc rate is " << dfval);

	//Check that extrapolation is working
	df = curve.get_DF(0.00001);
	dfval = df.getCcr();
	BOOST_MESSAGE("Fitted cc rate is " << dfval);
	//works but a little strange as can't tell how extrapolating.
	//Not holding constant zero rate outside of interp range

	//Can get around by adding overnight depo
	InstrumentDF df4;
	df4.fromCcr(0.01,0.004); //Overnight Depo
	curve.reset();
	curve.add_DF(df1);
	curve.add_DF(df2);
	curve.add_DF(df3);
	curve.add_DF(df4);

	curve.fit_curve();

	//Check that extrapolation is working
	df = curve.get_DF(0.1); //Halfway to first rate
	dfval = df.getCcr();
	BOOST_MESSAGE("Fitted final cc rate is " << dfval);






}


BOOST_AUTO_TEST_SUITE_END()
