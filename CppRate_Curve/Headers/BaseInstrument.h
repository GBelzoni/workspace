/*
 * BaseInstrument.h
 *
 *  Created on: Jun 8, 2013
 *      Author: phcostello
 */

#ifndef BASEINSTRUMENT_H_
#define BASEINSTRUMENT_H_

class BaseInstrument {
public:
	BaseInstrument();
	virtual ~BaseInstrument();
	virtual BaseInstrument* clone() const=0;
	virtual BaseInstrument* clone() =0;

	double getInitialTargetRate() const {
		return initial_target_rate;
	}

	double getNumFixedLegs() const {
		return num_fixed_legs;
	}

	double getNumFloatLegs() const {
		return num_float_legs;
	}

	double getObservedRate() const {
		return observed_rate;
	}

	double getEnd() const {
		return t_end;
	}

	double getStart() const {
		return t_start;
	}


	//Comparison for sorting instruments
	static bool ExpiryLessThan( const BaseInstrument & inst1, const BaseInstrument & inst2);


protected:

	double observed_rate;
	double initial_target_rate;
	double t_start;
	double t_end;
	double num_fixed_legs;
	double num_float_legs; //Redundant until there is cost of tenor


};

#endif /* BASEINSTRUMENT_H_ */
