/*
 * SimpleBootStrap_test.cpp
 *
 *  Created on: Jun 6, 2013
 *      Author: phcostello
 */

#include <SimpleBootStrap.h>
#include <LinearZeroesInnerCurve.h>



#define BOOST_TEST_DYN_LINK
#include <boost/test/unit_test.hpp>
#include <InstrumentDF.h>
#include <vector>


using namespace std;

BOOST_AUTO_TEST_SUITE( SimpleBootStrapSuite)

BOOST_AUTO_TEST_CASE( basic_tests )
{

	double expiry1 = 1;
	LinearZeroesInnerCurve inner_curve;
	SimpleBootStrap sp_curve(inner_curve);

    //Check that can't get expiry before fitted
	BOOST_CHECK_THROW(sp_curve.getDF(expiry1), CurveNotFitted );


	//Add two instruments
	InstrumentDF df1,df2,df3;

	df1.fromCcr(0.05,0.5);
	df2.fromCcr(0.01,1.0);
	df3.fromCcr(0.03,0.2);

//	sp_curve.addInstrument(df1);
//	sp_curve.addInstrument(df2);
//	sp_curve.addInstrument(df3);
//	BOOST_MESSAGE("df1's df = " << df1.getDf());
//	BOOST_MESSAGE("df2's df = " << df2.getDf());
//	BOOST_MESSAGE("df3's df = " << df3.getDf());
//
//
//	int len = sp_curve.length();
//	BOOST_CHECK_EQUAL(len, 3);
//
////	vector<vector<double> > list = sp_curve.GetDFList();
////	BOOST_CHECK_CLOSE(list[0][0], 0.994018, 0.01); //Check df
////	BOOST_CHECK_CLOSE(list[0][1], 0.2, 0.01); //Check expiry
////	BOOST_MESSAGE("Added one df instrument: Check df and expiry ok");
//
//	//Fit curve
//	//QuantLib::LinearInterpolation LinInt = curve.fit_curve();
//	sp_curve.fit();
//	BOOST_MESSAGE("Curve Fitted");
//	InstrumentDF df;
//	double dfval;
//
//	df = sp_curve.get_DF_instrument(0.3);
//	dfval = df.getCcr();
//	BOOST_MESSAGE("Fitted cc rate is " << dfval);
//	df = sp_curve.get_DF_instrument(0.8);
//	dfval = df.getCcr();
//	BOOST_MESSAGE("Fitted cc rate is " << dfval);




}


BOOST_AUTO_TEST_SUITE_END()