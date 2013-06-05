/*
 * AnalyticFormulas.cpp
 *
 *  Created on: Feb 14, 2013
 *      Author: phcostello
 */

#include <cmath>
#include <Normals.h>
#include "AnalyticFormulas.h"

#if !defined(_MSC_VER)
using namespace std;
#endif

double ZCB(double r, double Expiry) {
	return exp(-r * Expiry);

}

double ForwardContract(double r, double d, double Spot, double Strike,
		double Expiry) {
	return exp(-r * Expiry) * (exp((r - d) * Expiry) * Spot - Strike);
}


double BlackScholesCallDelta(double Spot, double Strike, double r, double d,
		double Vol, double Expiry) {

	double standardDeviation = Vol * sqrt(Expiry);
	double moneyness = log(Spot / Strike);
	double d1 = (moneyness + (r - d) * Expiry
			+ 0.5 * standardDeviation * standardDeviation) / standardDeviation;
	return CumulativeNormal(d1);

}


double BlackScholesPutDelta(double Spot, double Strike, double r, double d,
		double Vol, double Expiry) {

	double standardDeviation = Vol * sqrt(Expiry);
	double moneyness = log(Spot / Strike);
	double d1 = (moneyness + (r - d) * Expiry
			+ 0.5 * standardDeviation * standardDeviation) / standardDeviation;
	return CumulativeNormal(d1)-1;

}


double BlackScholesCallTheta(double Spot, double Strike, double r, double d,
		double Vol, double Expiry) {

	double standardDeviation = Vol * sqrt(Expiry);
	double moneyness = log(Spot / Strike);
	double d1 = (moneyness + (r - d) * Expiry
			+ 0.5 * standardDeviation * standardDeviation) / standardDeviation;
	double d2 = d1 - standardDeviation;
	return Spot*NormalDensity(d1)*standardDeviation/(2*sqrt(Expiry)) - r*Strike*exp(-r*Expiry)*CumulativeNormal(d2);

}

double BlackScholesPutTheta(double Spot, double Strike, double r, double d,
	double Vol, double Expiry) {

	double standardDeviation = Vol * sqrt(Expiry);
	double moneyness = log(Spot / Strike);
	double d1 = (moneyness + (r - d) * Expiry
			+ 0.5 * standardDeviation * standardDeviation) / standardDeviation;
	double d2 = d1 - standardDeviation;
	return Spot*NormalDensity(d1)*standardDeviation/(2*sqrt(Expiry)) + r*Strike*exp(-r*Expiry)*CumulativeNormal(-d2);


}

double BlackScholesCallRho(double Spot, double Strike, double r, double d,
	double Vol, double Expiry) {

	double standardDeviation = Vol * sqrt(Expiry);
	double moneyness = log(Spot / Strike);
	double d1 = (moneyness + (r - d) * Expiry
			+ 0.5 * standardDeviation * standardDeviation) / standardDeviation;
	double d2 = d1 - standardDeviation;
	return Strike*Expiry*exp(-r*Expiry)*CumulativeNormal(d2);

}

double BlackScholesPutRho(double Spot, double Strike, double r, double d,
	double Vol, double Expiry) {

	double standardDeviation = Vol * sqrt(Expiry);
	double moneyness = log(Spot / Strike);
	double d1 = (moneyness + (r - d) * Expiry
			+ 0.5 * standardDeviation * standardDeviation) / standardDeviation;
	double d2 = d1 - standardDeviation;
	return -Strike*Expiry*exp(-r*Expiry)*CumulativeNormal(-d2);
}
