/*
 * VanillaPayOffs.h
 *
 *  Created on: Apr 6, 2013
 *      Author: phcostello
 */

#ifndef VANILLAPAYOFFS_H_
#define VANILLAPAYOFFS_H_

#include <PayOff3.h>

class PayOffDigitalCall : public PayOff
{
public:

    PayOffDigitalCall(double Strike_);

    virtual double operator()(double Spot) const;
    virtual ~PayOffDigitalCall(){};
    virtual PayOff* clone() const;

private:

    double Strike;

};

class PayOffDigitalPut : public PayOff
{
public:

    PayOffDigitalPut(double Strike_);

    virtual double operator()(double Spot) const;
    virtual ~PayOffDigitalPut(){};
    virtual PayOff* clone() const;

private:

    double Strike;

};





#endif /* VANILLAPAYOFFS_H_ */
