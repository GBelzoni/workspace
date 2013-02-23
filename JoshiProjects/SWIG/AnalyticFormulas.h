/*
 * AnalyticFormulas.h
 *
 *  Created on: Feb 14, 2013
 *      Author: phcostello
 */

#ifndef ANALYTICFORMULAS_H_
#define ANALYTICFORMULAS_H_

double ZCB( double r,
			double Expiry);

double ForwardContract( double r,
				double d,
				double Spot,
				double Strike,
				double Expiry);


#endif /* ANALYTICFORMULAS_H_ */


