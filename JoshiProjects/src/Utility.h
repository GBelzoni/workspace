/*
 * Utility.h
 *
 *  Created on: Apr 6, 2013
 *      Author: phcostello
 */

#ifndef UTILITY_H_
#define UTILITY_H_

#include <vector>
#include <string>
#include <fstream>
#include <sstream>

using namespace std;

template<class T>
vector<T> vecseq ( T x0, T xf, double steps )
{
	double stepsize = (xf-x0)/steps;
	vector<T> result;
	result.resize(0);

	for( double i=0.0 ; i <= steps; i++)
	{
		double val = x0 + i*stepsize ;
		result.push_back(val);
	}
	return result;
}


template<class T>
void writetable (const vector< vector < T > > & resultTable , char * headers, char * outfilePath )
{
	//Need to write headers as csv list ending with \n
	std::ofstream outfile(outfilePath);
	outfile << headers;

	int numberRows = resultTable.size();
	int numberCols = resultTable[0].size();

	for( int i =0 ; i< numberRows; i++)
	{
		std::ostringstream sstream;

		//Seem to have problems converting 0 to value (get very large number) so add 0.000001
		for( int j = 0; j < numberCols; j++ )
		{
			sstream << resultTable[i][j] + 0.0000001<< ',';
		}
		//sstream << '\n'
		outfile << sstream.str() << std::endl;

	}
	outfile.close();

}



#endif /* UTILITY_H_ */
