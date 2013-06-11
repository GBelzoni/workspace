/*
 * SimpleBootStrap.h
 *
 *  Created on: Jun 6, 2013
 *      Author: phcostello
 */

#ifndef SIMPLEBOOTSTRAP_H_
#define SIMPLEBOOTSTRAP_H_

#include "BaseSimpleCurve.h"
#include "BaseInnerCurve.h"
#include "CurveExceptions.hpp"
#include <wrapper.h>
#include <boost/shared_ptr.hpp>


class SimpleBootStrap: public BaseSimpleCurve {

public:

	SimpleBootStrap();
	SimpleBootStrap( BaseInnerCurve& inner_curve ); //Choose your Interptype with inner_curve
		virtual ~SimpleBootStrap();

	//Getter
	virtual InstrumentDF get_DF_instrument( double Expiry) const;
	virtual double getDF( double Expiry) const;
	virtual double getRate( double t1, double t2, int numFixedLegs = 2, int numFloatLegs = 2) const;

	//Clone
	virtual BaseSimpleCurve* clone() const;
	virtual BaseSimpleCurve* clone();

	//Fitter
	virtual void fit();

	//For resetting shared_pointers to stack variables. make_shared not option with abc as can't construct due to virtual functions
	static void do_nothing_deleter(BaseInnerCurve*);

	void GapInDatesFinder();

protected:



	class BootStrapFitter
		{

		public:

		BootStrapFitter( BaseInstrument& thisInstrument, BaseInnerCurve& theInnerCurve );
		virtual ~BootStrapFitter();

		//This returns difference between target rate and final rate
		double operator()( double thisFinalDf );

		private:
		//data curve for calcs
		boost::shared_ptr<BaseInnerCurve> origCurve, tempCurve;

		BaseInstrument& innerInstrument;

		};

	friend class BootStrapFitter;


};

#endif /* SIMPLEBOOTSTRAP_H_ */
