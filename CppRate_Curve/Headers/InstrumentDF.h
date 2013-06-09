/*
 * InstrumentDF.h
 *
 *  Created on: Jun 3, 2013
 *      Author: phcostello
 */

#ifndef INSTRUMENTDF_H_
#define INSTRUMENTDF_H_

//#include<BaseInstruments.h>

class InstrumentDF  {
public:
	InstrumentDF( double df = 1.0, double Expiry = 0.0 );
	virtual ~InstrumentDF();

	//Setters
	void setDf( double df, double Expiry);
	void fromSr( double sr, double Expiry);
	void fromAr( double ar, double Expiry, double compoundsPerYear );
	void fromCcr( double ccr, double Expiry);

	//Getters
	double getDf() const;
	virtual double getExpiry() const; //from base class
	double getSr() const ;
	double getAr( double periodsPerYear) const;
	double getCcr() const;

	//Clone: if we want to make base class that this inherits from
//	virtual InstrumentDF* clone() const;


	//Comparison
	static bool ExpiryLessThan( const InstrumentDF & df1, const InstrumentDF & df2);


private:

	double df_;
	double expiry_;

};


#endif /* INSTRUMENTDF_H_ */
