/*
 * TestingMCGreeks.cpp
 *
 *  Created on: Apr 25, 2013
 *      Author: phcostello
 */



#include <iostream>
#include <fstream>
#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <cmath>
#include <boost/foreach.hpp>

#include <BlackScholesFormulas.h>
#include <BSCallClass.h>
#include "AnalyticFormulas.h"
#include "BumpDeltas.h"
#include "BSaliases.h"
#include "Utility.h"

//Testing boost function and boost bind
#include <boost/bind.hpp>
#include <boost/function.hpp>

//Joshi includes
#include <BlackScholesFormulas.h>
#include <Vanilla3.h>
#include "VanillaPayOffs.h"
#include <MCStatistics.h>
#include <ConvergenceTable.h>
#include <AntiThetic.h>
#include <ParkMiller.h>
#include <SimpleMC8.h>



using namespace std;

int main()
{

	double Spot = 100;
	double Strike = 100;
    double r = 0.05;
    double d = 0.0;
    double Vol = 0.1;
    double Expiry = 1;

    double BSCprice2 = BlackScholesCall( Spot,
                                 Strike,
                                 r,
                                 d,
                                 Vol,
                                 Expiry);

    double BSCVegaAnal = BlackScholesCallVega( Spot,
                                     Strike,
                                     r,
                                     d,
                                     Vol,
                                     Expiry);

    double BSCDeltaAnal = BlackScholesCallDelta(Spot,
            Strike,
            r,
            d,
            Vol,
            Expiry);

    double BumpSize = 0.00001;

    cout << "Original " << BSCprice2 << std::endl;
    cout << "Analytic Del " << BSCDeltaAnal << std::endl;
    cout << "Analytic Vega " << BSCVegaAnal << std::endl;

    //Testing boost bind and function
    boost::function<double (double)> BSCPriceSpot2;
    BSCPriceSpot2 = boost::bind(BlackScholesCall,_1,
    												Strike,
    												r,
    												d,
    												Vol,
    												Expiry);

    cout << "Analytic Call, Boost bind " << BSCPriceSpot2(Spot) << endl;
    double bumpedDelta2 = BumpDelta(Spot,BumpSize,BSCPriceSpot2);
    cout << "Bumped Del, Boost bind " << bumpedDelta2 << endl;

    //Calc Vega of call as function of time
    //Sequences

	std::vector<double> SpotSeq = vecseq(40.00,60.00,20.0);
	//std::vector<double> StrikeSeq = vecseq(42.0,58.0,5.0);
	std::vector<double> VolSeq = vecseq(0.01,0.2,5.0);
	std::vector<double> TimeSeq = vecseq(0.0,1.0,5.0);
	double Strikel = 50;

	//Make result table
	std::vector< std::vector<double>  > resultTable;
	std::vector<double> thisResultRow(8);
	double thisAnalVega, thisBumpedVega;
	unsigned long NumberOfPathsl;
	boost::function<double (double)> thisBumpFunc;

	//Random Number Genearator
	RandomParkMiller generator(1);
	AntiThetic GenTwo(generator);


	BOOST_FOREACH( double  Spotl, SpotSeq)
		BOOST_FOREACH( double  Voll, VolSeq)
			BOOST_FOREACH( double  Timel, TimeSeq)
			{
				thisAnalVega = BlackScholesCallVega(Spotl,
		    										Strikel,
		    										r,
		    										d,
		    										Voll,
		    										Timel);



				thisResultRow[0] = Spotl;
				thisResultRow[1] = Strikel;
				thisResultRow[2] = Voll;
				thisResultRow[3] = Timel;
				thisResultRow[4] = thisAnalVega;



					//Make sure option goes out of scope to destroy
					{

						NumberOfPathsl = 10000;

						//Vanilla Euro Call
						ParametersConstant VolParam(Voll);
						ParametersConstant rParam(r);
						//ConvergenceTable gathererTwo(gatherer);
						StatisticsMean gatherer;
						PayOffCall theLoopPayOff(Strikel);
						VanillaOption theLoopOption(theLoopPayOff,Timel);

						thisBumpFunc = boost::bind(SimpleMonteCarlo6,
														theLoopOption,
														Spotl,
														VolParam,
														rParam,
														NumberOfPathsl,
														gatherer,
														GenTwo);

						vector< vector<double> > thisMCprice = gatherer.GetResultsSoFar();
						thisResultRow[6] = thisMCprice[0][0];
						thisResultRow[7] = NumberOfPathsl;


					}
	    		resultTable.push_back(thisResultRow);
			}

	//Write Output using my writetable function in Utility.h
	char* headers = "Spot, Strike, Vol, Expiry, BSC_An_Vega, BSC_Bumped_Vega, MC_Results, NumberOfPaths \n";
	writetable(resultTable, headers, "Proj2.2_MCGreekBumps.csv");
	cout<< "done2" << endl;

	return 0;


}
