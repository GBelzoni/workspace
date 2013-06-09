/*
 * BaseInnerCurve.h
 *
 *  Created on: Jun 5, 2013
 *      Author: phcostello
 */

#ifndef BASEINNERCURVE_H_
#define BASEINNERCURVE_H_

#include<vector>
#include<map>
#include<string>
#include"InstrumentDF.h"

class BaseInnerCurve {
public:

	BaseInnerCurve();
	virtual ~BaseInnerCurve();

	virtual void add_DF( InstrumentDF df);
	virtual std::vector<std::vector<double> > GetDFList();
	virtual InstrumentDF get_DF( double Expiry) const= 0;
	virtual void fit_curve() = 0;
	virtual bool is_fitted() const;


	//Cloners
	virtual BaseInnerCurve* clone() const=0;
	//Need to have this if we want to modify curve later
	virtual BaseInnerCurve* clone() = 0;

	virtual void reset();

	int length();

protected:

	std::vector< InstrumentDF > curve_dfs;
	int number_dfs;
	bool fitted;

};


class InnerCurveForBaseTest : public BaseInnerCurve {

public:

	InnerCurveForBaseTest();

	virtual InstrumentDF get_DF( double Expiry) const;
	virtual void fit_curve();
	virtual BaseInnerCurve* clone() const;

	//Need to have this if we want to modify curve later
	virtual BaseInnerCurve* clone();

};



#endif /* BASEINNERCURVE_H_ */
