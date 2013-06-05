/*
 * BSaliases.h
 *
 *  Created on: Apr 6, 2013
 *      Author: phcostello
 */

#ifndef BSALIASES_H_
#define BSALIASES_H_

//
//
//                  BSCallClass.h
//
//



class BSCallSpot
{

public:

    BSCallSpot(double r_, double d_,
                     double T, double Vol_,
                     double Strike_);

    double operator()(double Spot) const;


private:

    double r;
    double d;
    double T;
    double Vol;
    double Strike;

};


#endif /* BSALIASES_H_ */
