/*
 * GeneralCurveInstrument_test.cpp
 *
 *  Created on: Jun 8, 2013
 *      Author: phcostello
 */

#include "GeneralCurveInstrument.h"


#define BOOST_TEST_DYN_LINK
#include <boost/test/unit_test.hpp>

using namespace std;

BOOST_AUTO_TEST_SUITE( Instruments)

BOOST_AUTO_TEST_CASE( GeneralInstrument )
{

	double observed_rate = 0.05;
	double initial_target_rate =0.05;
	double t_start = 0.25;
	double t_end = 1.0;
	double num_fixed_legs=2.0;
	double num_float_legs=2.0;

	GeneralCurveInstrument GCV = GeneralCurveInstrument( observed_rate,
															initial_target_rate,
															t_start,
															t_end,
															num_fixed_legs,
															num_float_legs);
	//Check Getters
	BOOST_REQUIRE_CLOSE(observed_rate, GCV.getObservedRate(), 0.01);
	BOOST_REQUIRE_CLOSE(initial_target_rate, GCV.getInitialTargetRate(), 0.01);
	BOOST_REQUIRE_CLOSE(t_start, GCV.getStart(), 0.01);
	BOOST_REQUIRE_CLOSE(t_end, GCV.getEnd(), 0.01);
	BOOST_REQUIRE_CLOSE(num_fixed_legs, GCV.getNumFixedLegs(), 0.01);
	BOOST_REQUIRE_CLOSE(num_float_legs, GCV.getNumFloatLegs(), 0.01);

	BOOST_MESSAGE("Getters are all ok");





}


BOOST_AUTO_TEST_CASE( DepoInstrument_test )
{

	double observed_rate = 0.05;
	double t_end = 1.0;

	DepoInstrument Depo1 = DepoInstrument( observed_rate, t_end );

	//Check Getters
	BOOST_REQUIRE_CLOSE(observed_rate, Depo1.getObservedRate(), 0.01);
	BOOST_REQUIRE_CLOSE(observed_rate, Depo1.getInitialTargetRate(), 0.01);
	BOOST_REQUIRE_CLOSE(0.0, Depo1.getStart(), 0.01);
	BOOST_REQUIRE_CLOSE(t_end, Depo1.getEnd(), 0.01);
	BOOST_REQUIRE_CLOSE(2.0, Depo1.getNumFixedLegs(), 0.01);
	BOOST_REQUIRE_CLOSE(2.0, Depo1.getNumFloatLegs(), 0.01);

	BOOST_MESSAGE("Getters are all ok");





}




BOOST_AUTO_TEST_SUITE_END()
