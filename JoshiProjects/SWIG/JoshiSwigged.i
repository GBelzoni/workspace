%module JoshiSwigged

%{
#include "AnalyticFormulas.h"
#include "BlackScholesFormulas.h"
%}

double ZCB(double r, double Expiry);
double ForwardContract( double r, double d,	double Spot, double Strike, double Expiry);

double BlackScholesCall( double Spot,
                         double Strike,
                         double r,
                         double d,
                         double Vol,
                         double Expiry);


double BlackScholesPut( double Spot,
                        double Strike,
                        double r,
                        double d,
                        double Vol,
                        double Expiry);

double BlackScholesDigitalCall(double Spot,
                               double Strike,
                               double r,
                               double d,
                               double Vol,
                               double Expiry);

double BlackScholesDigitalPut( double Spot,
                               double Strike,
                               double r,
                               double d,
                               double Vol,
                               double Expiry);

double BlackScholesCallVega( double Spot,
                             double Strike,
                             double r,
                             double d,
                             double Vol,
                             double Expiry);