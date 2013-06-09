/*
 * RandomGenerator.cpp
 *
 *  Created on: Apr 25, 2013
 *      Author: phcostello
 */


#include <vector>
#include <boost/foreach.hpp>
#include <iostream>

//Joshi includes - have to add to project properties
#include <AntiThetic.h>
#include <ParkMiller.h>

using namespace std;

int main()
{
	//Parkmiller and RandomParkMiller algos in Random.h
	//Random.h included in AntiThetic.h

	RandomParkMiller generator1(1);
	RandomParkMiller generator2(generator1);
	AntiThetic ATgenerator(generator1);

	RandomParkMiller generatorMulti(2);

	MJArray variates1(1);
	MJArray variates2(1);
	MJArray variatesMulti(2);


	//Test setting seed
	unsigned long seed = 10;
	unsigned long skips = 1;
	//generator1.SetSeed( seed );
	generator1.Skip(skips);
	generator1.Reset();

	//Uniform generation
	for( int j = 0; j<5 ; j++)
	{
		generator1.GetUniforms( variates1 );
		generator2.GetUniforms( variates2 );
		//Note antithetic sampling of uniform is mod 1, i.e. negatives get wrapped to unit interval
		//ATgenerator.GetGaussians( variates1 );
		//ATgenerator.GetGaussians( variates2 );

		cout << variates1[0] << " , " << variates2[0] << endl;


	}

	cout << endl << endl;

	//Testing multi dimensiontal - draws happen sequentially across dims
	for( int j = 0; j<5 ; j++)
	{
		generatorMulti.GetUniforms( variatesMulti);
		cout << variatesMulti[0] << " , " << variatesMulti[1]  << endl;

	}

	return 0;


}


