/*
 * BaseSimpleCurve.h
 *
 *  Created on: Jun 6, 2013
 *      Author: phcostello
 */

#ifndef BASESIMPLECURVE_H_
#define BASESIMPLECURVE_H_

#include<BaseInnerCurve.h>
#include<BaseInstrument.h>
#include<InstrumentDF.h>
#include<wrapper.h>
#include<vector>
#include<boost/shared_ptr.hpp>

class BaseSimpleCurve {
public:

	BaseSimpleCurve();
	virtual ~BaseSimpleCurve();

	//Setter
	virtual void addInstrument (const BaseInstrument & Instrument);

	//Getter
	virtual InstrumentDF get_DF_instrument( double Expiry) const = 0;
	virtual double getDF( double Expiry) const = 0;
	virtual double getRate( double t1, double t2, int numFixedLegs = 2, int numFloatLegs = 2) const = 0;
	int length();

	//Fitter
	virtual void fit() = 0;

	//Cloners
	virtual BaseSimpleCurve* clone() const = 0;
	virtual BaseSimpleCurve* clone() = 0 ;

	//For sorting the instruments when adding to curve
	static bool ExpiryLessThan ( const Wrapper<BaseInstrument> & it1, const Wrapper<BaseInstrument> & it2) ;

protected:

	int length_;
	bool fitted;
	std::vector<Wrapper< BaseInstrument > > vecInstruments;
	boost::shared_ptr<BaseInnerCurve> innerCurve;


	//Instrument Info matrix



};

#endif /* BASESIMPLECURVE_H_ */
