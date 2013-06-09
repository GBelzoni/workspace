/*
 * GeneralCurveInstrument.h
 *
 *  Created on: Jun 8, 2013
 *      Author: phcostello
 */

#ifndef GENERALCURVEINSTRUMENT_H_
#define GENERALCURVEINSTRUMENT_H_

#include "BaseInstrument.h"

class GeneralCurveInstrument: public BaseInstrument {
public:

	GeneralCurveInstrument(double observed_rate_,
								double initial_target_rate_,
								double t_start_,
								double t_end_,
								double num_fixed_legs_,
								double num_float_legs_);

	virtual ~GeneralCurveInstrument();

	virtual BaseInstrument* clone() const;
	virtual BaseInstrument* clone() ;

};

#endif /* GENERALCURVEINSTRUMENT_H_ */



