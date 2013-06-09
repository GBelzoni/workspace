/*
 * GeneralCurveInstrument.cpp
 *
 *  Created on: Jun 8, 2013
 *      Author: phcostello
 */

#include "GeneralCurveInstrument.h"

GeneralCurveInstrument::GeneralCurveInstrument(double observed_rate_,
													double initial_target_rate_,
													double t_start_,
													double t_end_,
													double num_fixed_legs_,
													double num_float_legs_)
{

	observed_rate = observed_rate_;
	initial_target_rate = initial_target_rate_;
	t_start = t_start_;
	t_end = t_end_;
	num_fixed_legs = num_fixed_legs_;
	num_float_legs = num_float_legs_;

}

GeneralCurveInstrument::~GeneralCurveInstrument() {
	// TODO Auto-generated destructor stub
}

BaseInstrument* GeneralCurveInstrument::clone() const {

	return new GeneralCurveInstrument(*this);
}

BaseInstrument* GeneralCurveInstrument::clone() {

	return new GeneralCurveInstrument(*this);
}
