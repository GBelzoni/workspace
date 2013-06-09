/*
 * BaseInstrument.cpp
 *
 *  Created on: Jun 8, 2013
 *      Author: phcostello
 */

#include "BaseInstrument.h"

BaseInstrument::BaseInstrument() : observed_rate(0.0),
									initial_target_rate(0.0),
									t_start(0.0),
									t_end(0.0),
									num_fixed_legs(0.0),
									num_float_legs(0.0)
{
	// TODO Auto-generated constructor stub

}

BaseInstrument::~BaseInstrument() {
	// TODO Auto-generated destructor stub
}

bool BaseInstrument::ExpiryLessThan( const BaseInstrument & inst1, const BaseInstrument & inst2)
{
	//Compares Expiry so can sort by expiries
	bool tf;
	inst1.getEnd() < inst2.getEnd()  ? (tf = true) : (tf = false);
	return(tf);

}
