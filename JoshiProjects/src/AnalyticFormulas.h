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

double BlackScholesCallDelta( double Spot,
                             double Strike,
                             double r,
                             double d,
                             double Vol,
                             double Expiry);

double BlackScholesPutDelta( double Spot,
                             double Strike,
                             double r,
                             double d,
                             double Vol,
                             double Expiry);


double BlackScholesCallTheta( double Spot,
                             double Strike,
                             double r,
                             double d,
                             double Vol,
                             double Expiry);

double BlackScholesPutTheta( double Spot,
                             double Strike,
                             double r,
                             double d,
                             double Vol,
                             double Expiry);

double BlackScholesCallRho( double Spot,
                             double Strike,
                             double r,
                             double d,
                             double Vol,
                             double Expiry);

double BlackScholesPutRho( double Spot,
                             double Strike,
                             double r,
                             double d,
                             double Vol,
                             double Expiry);


#endif /* ANALYTICFORMULAS_H_ */
