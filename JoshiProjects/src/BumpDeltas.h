/*
 * BumpDeltas.h
 *
 *  Created on: Apr 5, 2013
 *      Author: phcostello
 */

#ifndef BUMPDELTAS_H_
#define BUMPDELTAS_H_

template<class T>
double BumpDelta( double Value,
					double BumpSize,
					T TheFunction)
{
	return (TheFunction(Value + 0.5*BumpSize) - TheFunction(Value - 0.5*BumpSize))/BumpSize;
}



#endif /* BUMPDELTAS_H_ */
