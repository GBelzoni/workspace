/*
 * BaseInnerCurve_test.cpp
 *
 *  Created on: Jun 5, 2013
 *      Author: phcostello
 */

#define BOOST_TEST_DYN_LINK
#include <boost/test/unit_test.hpp>
#include <BaseInnerCurve.h>
#include <InstrumentDF.h>
#include <vector>

using namespace std;

BOOST_AUTO_TEST_SUITE( InnerCurve)

BOOST_AUTO_TEST_CASE( basic_tests )
{
	InstrumentDF df(0.95,0.5);
	InnerCurveForBaseTest curve;
	curve.add_DF(df);
	int len = curve.length();
	BOOST_CHECK_EQUAL(len, 1);
	vector<vector<double> > list = curve.GetDFList();
	BOOST_CHECK_CLOSE(list[0][0], 0.95, 0.01); //Check df
	BOOST_CHECK_CLOSE(list[0][1], 0.5, 0.01); //Check expiry
	BOOST_MESSAGE("Added one df instrument: Check df and expiry ok");

	//Adding an second instrument checks that sorts by expiry ok
	InstrumentDF df2(0.90,0.3);
	curve.add_DF(df2);
	len = curve.length();
	BOOST_CHECK_EQUAL(len, 2);
	list = curve.GetDFList();
	BOOST_CHECK_CLOSE(list[0][0], 0.90, 0.01); //Check df, and that has been sorted
	BOOST_CHECK_CLOSE(list[0][1], 0.3, 0.01); //Check expiry, and that has been sorted

	//Checking reset
	curve.reset();
	len = curve.length();
	BOOST_CHECK_EQUAL(len, 0);
	curve.GetDFList();
	BOOST_CHECK_EQUAL(curve.GetDFList().size(),0); //Check df, and that has been sorted



}


BOOST_AUTO_TEST_SUITE_END()
