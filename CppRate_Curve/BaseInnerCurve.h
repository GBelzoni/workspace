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
	virtual double get_DF( double Expiry) = 0;
	virtual void fit_curve() = 0;

	int length();

private:

	std::vector< InstrumentDF > curve_dfs;
	int number_dfs;

};


class InnerCurveForBaseTest : public BaseInnerCurve {

public:

	InnerCurveForBaseTest();

	virtual double get_DF( double Expiry);
	virtual void fit_curve();

};



#endif /* BASEINNERCURVE_H_ */
