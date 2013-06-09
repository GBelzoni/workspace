/*
 * LinearZeroesInnerCurve.h
 *
 *  Created on: Jun 5, 2013
 *      Author: phcostello
 */

#ifndef LINEARZEROESINNERCURVE_H_
#define LINEARZEROESINNERCURVE_H_

#include "BaseInnerCurve.h"
#include <ql/math/interpolations/linearinterpolation.hpp>
#include <boost/shared_ptr.hpp>
#include <vector>
#include <CurveExceptions.hpp>


class LinearZeroesInnerCurve: public BaseInnerCurve {
public:
	LinearZeroesInnerCurve();
	virtual ~LinearZeroesInnerCurve();

	//Need to add extra overnight df on first addition, as you need to points to interpolate
	virtual void add_DF( InstrumentDF df);

	virtual InstrumentDF get_DF( double Expiry) const;
	virtual void fit_curve();
	virtual BaseInnerCurve* clone() const;
	virtual BaseInnerCurve* clone();

protected:


	std::vector<double> x,y; //You need to define x and y axis as data members as fitted interpolator uses reference so if defined in function then scope issues
	boost::shared_ptr<QuantLib::LinearInterpolation>  fitted_linear_interpolator;


};

#endif /* LINEARZEROESINNERCURVE_H_ */
