/*
 * SimpleBootStrap.cpp
 *
 *  Created on: Jun 6, 2013
 *      Author: phcostello
 */

#include "SimpleBootStrap.h"
#include<exception>
#include<wrapper.h>
#include<boost/make_shared.hpp>
#include<Bisection.h>
#include<InstrumentDF.h>



//You need this function to
void SimpleBootStrap::do_nothing_deleter(BaseInnerCurve*)
{
	return;
}

SimpleBootStrap::SimpleBootStrap()//:innerCurve(inner_curve)
{

}


SimpleBootStrap::SimpleBootStrap( BaseInnerCurve& inner_curve)//:innerCurve(inner_curve)
{
	//Set pointer to inner pointer
	innerCurve.reset( inner_curve.clone());//, do_nothing_deleter);


}

SimpleBootStrap::~SimpleBootStrap() {
	// TODO Auto-generated destructor stub
}

//Cloners
BaseSimpleCurve* SimpleBootStrap::clone() const {

	return new SimpleBootStrap(*this);
}

BaseSimpleCurve* SimpleBootStrap::clone() {

	return new SimpleBootStrap(*this);
}

//Getter
InstrumentDF SimpleBootStrap::get_DF_instrument( double Expiry) const
{
	//This function returns InstrumentDF object

	if(!(innerCurve->is_fitted()))
	{
		throw(CurveNotFitted());
	}
	//The inner curve has method to do this
	return( innerCurve->get_DF(Expiry));

}

double SimpleBootStrap::getDF( double Expiry) const
{
	//this returns only the DF value. Use get_DF_instrument for object
	return(get_DF_instrument(Expiry).getDf());
}

double SimpleBootStrap::getRate( double t1, double t2, int numFixedLegs, int numFloatLegs) const
{
	if(!(innerCurve->is_fitted()))
	{
		throw(CurveNotFitted());
	}

	double time_period = t2 - t1;
	//note below that number of accrual periods is one less than number of legs
	//Assume in simple case that all accrual periods are same. NOT REALISTIC ASSUMPTION
	double tau_fixed_legs = time_period/(numFixedLegs-1); //tau is year frac between each leg
	double tau_float_legs = time_period/(numFloatLegs-1); //tau is year frac between each leg

	std::vector<double> fixed_df_times, float_df_times;
	fixed_df_times.resize(numFixedLegs);
	float_df_times.resize(numFloatLegs);

	//Set up df schedule for fixed and floating
	for(int i = 0 ; i < numFixedLegs ; i++)
	{
		fixed_df_times[i] = t1 + i*tau_fixed_legs;
	}
	for(int i = 0 ; i < numFixedLegs ; i++)
	{
		float_df_times[i] = t1 + i*tau_float_legs;
	}


	std::vector<double> fixed_dfs, float_dfs;


	//Below calculations are standard par swap rate calc from Joshi
	//ie. S = [P(T_0) - P(T_1) ]/ [sum_i tau_i * P(T_i)] = NPV_floating/ NPV_fixed
	// where we note sum of NPV starts at i=1
	//Calculate NPV of fixed legs, ie the annuity
	double NPV_fixed = 0;
	double thisDF;
	for(int i = 1 ; i < numFixedLegs ; i++)
	{
		thisDF = this->getDF(fixed_df_times[i]);
		NPV_fixed += tau_fixed_legs*thisDF;
	}
	//Calculate NPV of floating;
	double NPV_floating = (this->getDF(t1) - this->getDF(t2));

	double rate = NPV_floating/NPV_fixed ;


	return rate;

}

void SimpleBootStrap::GapInDatesFinder() {

	//Sort instrument, make sure done in added instruments
	//Check if the curve has no gaps
	std::vector<Wrapper<BaseInstrument> >::iterator it;
	double end_this_i, start_next_i;
	//Need to fix for case when only one instrument
	for (it = vecInstruments.begin(); it != (vecInstruments.end() - 1); ++it) {
		//Check for each instrument that it's expiry is greater equal than the next instruments
		//start, ie no gaps
		end_this_i = (**it).getEnd();
		start_next_i = (**(it + 1)).getStart();
		if (end_this_i < start_next_i) {
			throw(GapInstrumentTimeRange());
		}
	}

}

//Fitter
void SimpleBootStrap::fit()
{
	//Check if curve has at least one instrument
	if(vecInstruments.size() == 0)
	{
		throw(NeedMoreInstruments());
	}


	//TODO: Gap in intruments cashflows not working yet
	//Sort instrument, make sure done in added instruments
	//Check if the curve has no gaps - function throws error if there is gap
	//GapInDatesFinder();

	//Do bootstrap algo
	std::vector<Wrapper<BaseInstrument> >::iterator it;

	for( it = vecInstruments.begin() ; it!=vecInstruments.end(); ++it)
	{

		//Initialise bootstrap fitter with instrument
		BootStrapFitter thisFitter(**it,*innerCurve);

		//Get initial guess from instrument
		//double initial_target_rate = (**it).getInitialTargetRate();
		//double start = (**it).getStart();
		double end = (**it).getEnd();
		//double initial_expiry_df = 1/((1 + initial_target_rate) *( end - start));

		//find root for bs_fitter

		double fitted_expiry_df = Bisection( 0.0 , 0.0 , 1.0 , 1e-5, thisFitter);

		//Make df_final with this rate
		InstrumentDF thisDF(fitted_expiry_df, end);

		//Add to Inner curve
		innerCurve->add_DF(thisDF);

	}

	innerCurve->fit_curve();

}

SimpleBootStrap::BootStrapFitter::BootStrapFitter(
		BaseInstrument& thisInstrument, BaseInnerCurve& theInnerCurve) : innerInstrument(thisInstrument)
{

	origCurve.reset( theInnerCurve.clone()); //Wrapper makes a copy by value
}

SimpleBootStrap::BootStrapFitter::~BootStrapFitter() {
}

double SimpleBootStrap::BootStrapFitter::operator()(double this_final_df) {

	//GeneralCurveInstrument tmpInst(this_final_rate,0.0, 0.0, innerInstrument.getEnd(), 2, 2);
	InstrumentDF thisDf(this_final_df,innerInstrument.getEnd());

	tempCurve.reset(origCurve->clone());

	tempCurve->add_DF(thisDf);

	//Important!!! You need to fit the inner interpolator
	tempCurve->fit_curve();

	SimpleBootStrap tempBSCurve(*tempCurve);

	double t1 = innerInstrument.getStart();
	double t2 = innerInstrument.getEnd();
	double target_rate = innerInstrument.getObservedRate();
	int num_fixed_legs = innerInstrument.getNumFixedLegs();
	int num_float_legs = innerInstrument.getNumFloatLegs();


	double thisRate = tempBSCurve.getRate(t1,t2,num_fixed_legs,num_float_legs);

	return(target_rate - thisRate);


}
