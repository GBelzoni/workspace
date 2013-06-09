/*
 * InstrumentDF_test.cpp
 *
 *  Created on: Jun 3, 2013
 *      Author: phcostello
 */


#define BOOST_TEST_DYN_LINK
#include <boost/test/unit_test.hpp>
#include "InstrumentDF.h"
#include <cmath>

BOOST_AUTO_TEST_SUITE( InstrumentDF_suite)

BOOST_AUTO_TEST_CASE( constructors_test )
{
	InstrumentDF df0 = InstrumentDF();
	BOOST_CHECK_EQUAL(df0.getDf(), 1.0);
	BOOST_CHECK_EQUAL(df0.getExpiry(), 0.0);

}

BOOST_AUTO_TEST_CASE( setters_test )
{
	InstrumentDF df0 = InstrumentDF();
	double r = 0.05;
	double m = 2;
	double t =1;

	//Check all setters - next time use BOOST_REQUIRE_CLOSE
	df0.setDf(0.95, 0.5);
	BOOST_REQUIRE(df0.getDf() == 0.95);
	BOOST_CHECK_EQUAL(df0.getExpiry(), 0.5);

	df0.fromSr(r,t);
	BOOST_REQUIRE(round((df0.getDf())*1000) == 952);

	df0.fromAr(r,t,m);
	BOOST_REQUIRE(round((df0.getDf())*100000) == 95181);

	df0.fromCcr(r,t);
	BOOST_REQUIRE(round((df0.getDf()*100000)) == 95123);


	//Check all getters
	df0.setDf(0.95, 1);
	double sr = df0.getSr();
	BOOST_REQUIRE_CLOSE(sr, 0.05263, 1e-2);

	double ar = df0.getAr(2);
	BOOST_REQUIRE_CLOSE(ar, 0.05195, 2e-2);

	double ccr = df0.getCcr();
	BOOST_REQUIRE_CLOSE(ccr, 0.05129, 2e-2);


}


BOOST_AUTO_TEST_CASE( other_members )
{
	InstrumentDF df0 = InstrumentDF(0.95,0.1);
	InstrumentDF df1 = InstrumentDF(0.99,0.5);

	BOOST_REQUIRE( InstrumentDF::ExpiryLessThan(df0, df1));

}


BOOST_AUTO_TEST_SUITE_END()
