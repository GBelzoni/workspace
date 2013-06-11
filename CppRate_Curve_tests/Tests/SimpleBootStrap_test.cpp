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
#include <GeneralCurveInstrument.h>


using namespace std;

BOOST_AUTO_TEST_SUITE( SimpleBootStrapSuite)

BOOST_AUTO_TEST_CASE( basic_tests )
{

	double expiry1 = 1;
	LinearZeroesInnerCurve inner_curve;
	SimpleBootStrap sp_curve(inner_curve);

    //Check that can't get expiry before fitted
	BOOST_CHECK_THROW(sp_curve.getDF(expiry1), CurveNotFitted );
	//Check can't fit before have enough instruments
	BOOST_CHECK_THROW(sp_curve.fit(), NeedMoreInstruments)

	//Add two instruments
	DepoInstrument depo1(0.05,0.5);
	DepoInstrument depo2(0.03,1.0);
	DepoInstrument depo3(0.03,0.2);

	sp_curve.addInstrument(depo1);
	sp_curve.addInstrument(depo2);
	sp_curve.addInstrument(depo3);


	//Check length finder
	int len = sp_curve.length();
	BOOST_CHECK_EQUAL(len, 3);



}


BOOST_AUTO_TEST_CASE( gap_instrument_dates_test )
{

	//TODO; this isn't working
	double expiry1 = 1;
	LinearZeroesInnerCurve inner_curve;
	SimpleBootStrap sp_curve(inner_curve);

	//Add three instruments
	DepoInstrument depo1(0.05,0.5);
	DepoInstrument depo2(0.03,1.0);
	DepoInstrument depo3(0.03,0.2);

	sp_curve.addInstrument(depo1);
	sp_curve.addInstrument(depo2);
	sp_curve.addInstrument(depo3);

	//Check Gap finder
	//No gaps in cashflow times so shouldn't throw
	BOOST_CHECK_NO_THROW(sp_curve.GapInDatesFinder());
	GeneralCurveInstrument GCV = GeneralCurveInstrument( 0.06, //observed rate
															0.06, //initial_rate
															2.0, //start_t
															3.0, //end_t
															2.0, //fixed_legs
															2.0); //float_legs

	//Add instrument with gap between last curve expiry, ie depo2_t_end =1.0 and start of
	// is GCV_t_start = 2.0
	//Should throw
	sp_curve.addInstrument(GCV);
	BOOST_CHECK_THROW(sp_curve.GapInDatesFinder(), GapInstrumentTimeRange);

	//Add Intrument to bridge gap and now should be fine
	DepoInstrument depo4(0.05,3.0);
	sp_curve.addInstrument(depo4);
	BOOST_CHECK_NO_THROW(sp_curve.GapInDatesFinder());


}


BOOST_AUTO_TEST_CASE( bootstrap_test_from_depos )
{


	LinearZeroesInnerCurve inner_curve;
	SimpleBootStrap sp_curve(inner_curve);

	//Have caculated
	//Add depos
	DepoInstrument depo1(0.02,1.0);
	DepoInstrument depo2(0.04,2.0);
	DepoInstrument depo3(0.06,3.0);
	DepoInstrument depo4(0.07,4.0);


	sp_curve.addInstrument(depo1);
	sp_curve.addInstrument(depo2);
	sp_curve.addInstrument(depo3);
	sp_curve.addInstrument(depo4);


	//Check if we can fit
	sp_curve.fit();
		//Double fitting problem arghh!!
	//BOOST_CHECK_NO_THROW(sp_curve.fit());

	//Check we get rates back
	BOOST_CHECK_CLOSE(0.02,sp_curve.getRate(0.0,1.0,2.0,2.0),0.1);
	BOOST_CHECK_CLOSE(0.04,sp_curve.getRate(0.0,2.0,2.0,2.0),0.1);
	BOOST_CHECK_CLOSE(0.06,sp_curve.getRate(0.0,3.0,2.0,2.0),0.1);
	BOOST_CHECK_CLOSE(0.07,sp_curve.getRate(0.0,4.0,2.0,2.0),0.1);

	//Check forward rates
	BOOST_CHECK_CLOSE(0.05882,sp_curve.getRate(1.0,2.0,2.0,2.0),0.1);
	BOOST_CHECK_CLOSE(0.09259,sp_curve.getRate(2.0,3.0,2.0,2.0),0.1);
	BOOST_CHECK_CLOSE(0.08474,sp_curve.getRate(3.0,4.0,2.0,2.0),0.1);

	//Check we 4year par swap
	BOOST_CHECK_CLOSE(0.06039,sp_curve.getRate(0.0,4.0,17.0,17.0),0.1);

	GeneralCurveInstrument GCV = GeneralCurveInstrument( 0.06, //observed rate
															0.06, //initial_rate
															2.0, //start_t
															3.0, //end_t
															2.0, //fixed_legs
															2.0); //float_legs



}


BOOST_AUTO_TEST_CASE( bootstrap_test_from_fras )
{


	LinearZeroesInnerCurve inner_curve;
	SimpleBootStrap sp_curve(inner_curve);

	//Have caculated
	//Add depos
	FRAInstrument FRA1(0.02,0.0, 1.0);
	FRAInstrument FRA2(0.05882,1.0, 2.0);
	FRAInstrument FRA3(0.09259,2.0 ,3.0);
	FRAInstrument FRA4(0.08474,3.0, 4.0);


	sp_curve.addInstrument(FRA1);
	sp_curve.addInstrument(FRA2);
	sp_curve.addInstrument(FRA3);
	sp_curve.addInstrument(FRA4);


	//Check if we can fit
	sp_curve.fit();
	//Double fitting problem arghh!!
	//BOOST_CHECK_NO_THROW(sp_curve.fit());

	//Check we get rates back
	BOOST_CHECK_CLOSE(0.02,sp_curve.getRate(0.0,1.0,2.0,2.0),0.1);
	BOOST_CHECK_CLOSE(0.04,sp_curve.getRate(0.0,2.0,2.0,2.0),0.1);
	BOOST_CHECK_CLOSE(0.06,sp_curve.getRate(0.0,3.0,2.0,2.0),0.1);
	BOOST_CHECK_CLOSE(0.07,sp_curve.getRate(0.0,4.0,2.0,2.0),0.1);

	//Check forward rates
	BOOST_CHECK_CLOSE(0.05882,sp_curve.getRate(1.0,2.0,2.0,2.0),0.1);
	BOOST_CHECK_CLOSE(0.09259,sp_curve.getRate(2.0,3.0,2.0,2.0),0.1);
	BOOST_CHECK_CLOSE(0.08474,sp_curve.getRate(3.0,4.0,2.0,2.0),0.1);

	//Check we 4year par swap
	BOOST_CHECK_CLOSE(0.06039,sp_curve.getRate(0.0,4.0,17.0,17.0),0.1);

	GeneralCurveInstrument GCV = GeneralCurveInstrument( 0.06, //observed rate
															0.06, //initial_rate
															2.0, //start_t
															3.0, //end_t
															2.0, //fixed_legs
															2.0); //float_legs



}



BOOST_AUTO_TEST_SUITE_END()
