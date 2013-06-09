/*
 * InstrumentDF.cpp
 *
 *  Created on: Jun 3, 2013
 *      Author: phcostello
 */

#include "InstrumentDF.h"
#include "math.h"
#include <iostream>

using namespace std;

InstrumentDF::InstrumentDF(double df, double Expiry): df_(df), expiry_(Expiry) {
}

InstrumentDF::~InstrumentDF() {

}

void InstrumentDF::setDf(double df, double Expiry) {

	df_ = df;
	expiry_ = Expiry;
}

void InstrumentDF::fromSr(double sr, double Expiry) {

	expiry_ = Expiry;
	df_ = 1.0/(1.0+ sr);

}

void InstrumentDF::fromAr(double ar, double Expiry, double compoundsPerYear) {

	expiry_ = Expiry;
	df_ = 1.0/(pow((1.0+ ar/compoundsPerYear), Expiry * compoundsPerYear));

}

void InstrumentDF::fromCcr(double ccr, double Expiry) {

	expiry_ = Expiry;
	df_ = exp(- ccr * Expiry);

}

double InstrumentDF::getDf() const{

	return( df_);
}

double InstrumentDF::getExpiry() const {

	return( expiry_);

}

double InstrumentDF::getSr() const {

	double sr = 1.0/ df_ - 1.0;
	return(sr);

}

double InstrumentDF::getAr(double compoundsPerYear) const {

	double ar = (pow(1.0/ df_ , 1/(expiry_ * compoundsPerYear)) - 1)* compoundsPerYear;
	return(ar);

}

double InstrumentDF::getCcr() const {

	double ccr = -log(df_)/ expiry_;
	return ccr;

}

//
//InstrumentDF* InstrumentDF::clone() const {
//
//	return new InstrumentDF(*this);
//
//}

bool InstrumentDF::ExpiryLessThan( const InstrumentDF & df1, const InstrumentDF & df2)
{
	//Compares Expiry so can sort by expiries
	bool tf;
	df1.getExpiry() < df2.getExpiry()  ? (tf = true) : (tf = false);
	return(tf);

}


