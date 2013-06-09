/*
 * CurveExceptions.hpp
 *
 *  Created on: Jun 6, 2013
 *      Author: phcostello
 */

#ifndef CURVEEXCEPTIONS_HPP_
#define CURVEEXCEPTIONS_HPP_

#include<exception>

//Exceptions
class NeedMoreDfs : public std::exception
{
  virtual const char* what() const throw()
  {
	  return "You need at least two dfs fit curve\n";
  }
}; //Note we have instantiated NMD of NeedMoreDfs type


class NeedMoreInstruments: public std::exception
{
	virtual const char* what() const throw()
	  {
		  return "You need at least one instrument to fit curve\n";
	  }

};


class GapInstrumentTimeRange: public std::exception
{
	virtual const char* what() const throw()
	  {
		  return "There is a gap in the date ranges of curves. \n Add instruments to cover full date range. \n";

	  }

};


//Exceptions
class CurveNotFitted : public std::exception
{
  virtual const char* what() const throw()
  {
	  return "Have to fit curve before querying\n";
  }
}; //Note we have instantiated NMD of NeedMoreDfs type



#endif /* CURVEEXCEPTIONS_HPP_ */
