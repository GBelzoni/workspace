/*
 * main.cpp


 *
 *  Created on: Feb 14, 2013
 *      Author: phcostello
 */

#include <iostream>
#include <vector>
#include <fstream>
#include <iostream>
#include <string>
#include <sstream>
#include <boost/foreach.hpp>

//Joshi includes
#include <BlackScholesFormulas.h>
#include <Vanilla3.h>
#include "VanillaPayOffs.h"
#include <MCStatistics.h>
#include <ConvergenceTable.h>
#include <AntiThetic.h>
#include <ParkMiller.h>
#include <SimpleMC8.h>

//My project includes
#include "AnalyticFormulas.h"
#include "Utility.h"

using namespace std;

int main()
{

	double Spot = 90;
	double Strike = 100;
    double r = 0.05;
    double d = 0.0;
    double Vol = 0.1;
    double Expiry = 1.0;



    //Monte Carlo Engine from Joshi

    ParametersConstant VolParam(Vol);
    ParametersConstant rParam(r);

    StatisticsMean gatherer;
    ConvergenceTable gathererTwo(gatherer);

    RandomParkMiller generator(1);
    AntiThetic GenTwo(generator);

    unsigned long NumberOfPaths = 10000;
    vector<vector<double> > results;

    //Vanilla Euro Call
    PayOffCall thePayOff(Strike);
    VanillaOption theOption(thePayOff,Expiry);

    //Calculating functions
    double BSCprice = BlackScholesCall( Spot,
                                 Strike,
                                 r,
                                 d,
                                 Vol,
                                 Expiry);




    SimpleMonteCarlo6(theOption,
    							Spot,
    							VolParam,
    							rParam,
    							NumberOfPaths,
    							gatherer,
    							GenTwo);

    results= gatherer.GetResultsSoFar();

    std::cout << "BSC price: " << BSCprice << std::endl;
    cout << "MC Call Price " << results[0][0] << endl;

    //Vanilla Euro Digital Call

    PayOffDigitalCall theDigPayOff(Strike);
    VanillaOption theDigOption(theDigPayOff,Expiry);

    double BSCDigitaCall = BlackScholesDigitalCall( Spot,
                                 Strike,
                                 r,
                                 d,
                                 Vol,
                                 Expiry);

    StatisticsMean gathererDig;
    SimpleMonteCarlo6(theDigOption,
        							Spot,
        							VolParam,
        							rParam,
        							NumberOfPaths,
        							gathererDig,
        							GenTwo);

    results= gathererDig.GetResultsSoFar();

    std::cout << "BSC Dig price: " << BSCDigitaCall << std::endl;
    cout << "MC Dig Call Price " << results[0][0] << endl;

//    for ( int i = 0 ; i < results.size(); i++)
//    {
//    	for ( int j =0 ; j < results[i].size();j++)
//    	{
//    		 cout << results[i][j] << " ";
//    	}
//    	cout<< "\n";
//    }

    typedef std::vector<double>::iterator vit;

    //Sequences
    std::vector<double> Result;
    std::vector<double> SpotSeq = vecseq(40.00,60.00,40.0);
    std::vector<double> StrikeSeq = vecseq(42.0,58.0,5.0);
    std::vector<double> VolSeq = vecseq(0.01,0.2,5.0);
    std::vector<double> TimeSeq = vecseq(0.0,1.0,5.0);


    //Make result table
    std::vector< std::vector<double>  > resultTable;
    std::vector<double> thisResultRow(8);

    vit itspt;
    vit itstk;
    vit itvol;
    vit ittme;

    double Spotl;
	double Strikel;
	double Voll;
	double Expiryl;
	unsigned long NumberOfPathsl;


    for(itspt = SpotSeq.begin(); itspt != SpotSeq.end(); itspt++)
    {
    	//cout << *itspt << endl;
    	for(itstk = StrikeSeq.begin(); itstk != StrikeSeq.end(); itstk++)
    	{
    		for(itvol = VolSeq.begin(); itvol != VolSeq.end(); itvol++)
    		{
    			for(ittme = TimeSeq.begin(); ittme != TimeSeq.end(); ittme++)
    			{

    				Spotl = *itspt;
    				Strikel= *itstk;
    				Voll = *itvol;
    				Expiryl = *ittme;

    				double BSCAnalprice = BlackScholesCall( Spotl,
    				                                 Strikel,
    				                                 r,
    				                                 d,
    				                                 Voll,
    				                                 Expiryl);

    				thisResultRow[0] = Spotl;
					thisResultRow[1] = Strikel;
					thisResultRow[2] = Voll;
					thisResultRow[3] = Expiryl;
					thisResultRow[4] = BSCAnalprice;

    				//Make sure option goes out of scope to destroy
    				{

    					NumberOfPathsl = 10000;

    					//Vanilla Euro Call
    					ParametersConstant VolParam(Voll);
						ParametersConstant rParam(r);
						//ConvergenceTable gathererTwo(gatherer);
						StatisticsMean gatherer2;
    					PayOffCall theLoopPayOff(Strikel);
						VanillaOption theLoopOption(theLoopPayOff,Expiryl);

						SimpleMonteCarlo6(theLoopOption,
						    							Spotl,
						    							VolParam,
						    							rParam,
						    							NumberOfPathsl,
						    							gatherer2,
						    							GenTwo);

						vector< vector<double> > thisMCprice = gatherer2.GetResultsSoFar();
						thisResultRow[5] = thisMCprice[0][0];
						thisResultRow[6] = NumberOfPathsl;


    				}
    				resultTable.push_back(thisResultRow);


    			}
    		}
    	}

    }

    std::string thisResult;

    std::ofstream outfile("Project111.csv");
    outfile << "Spot, Strike, Vol, Expiry, BSC_An_price, MC_price, numberPaths \n";
    int numberRows = resultTable.size();

    for( int i =0 ; i< numberRows; i++)
    {
    	std::ostringstream sstream;

    	//Seem to have problems converting 0 to value (get very large number) so add 0.000001
    	for( int j = 0; j <7; j++ )
    	{
    		sstream << resultTable[i][j] + 0.0000001<< ',';
    	}
    	//sstream << '\n'
    	outfile << sstream.str() << std::endl;

    }
    outfile.close();

    cout<< "done" << endl;

}



