/*
 * main.cpp
 *
 *  Created on: Feb 17, 2013
 *      Author: phcostello
 */

#include <boost/smart_ptr.hpp>

class tempClass
{
	public:
	tempClass( double data );
	~tempClass();

	double& operator*();

	double data;

};

tempClass::tempClass( double _data = 0.0)
{

	data = _data;
	std::cout << "Created object" << std::endl;

}

tempClass::~tempClass()
{
	std::cout << "Destroyed object" << std::endl;
}

double& tempClass::operator*()
{
	return data;
}


int main_off()
{

	char temp;
	tempClass tc(5.0);
	std::cout << tc.data << std::endl;

	boost::shared_ptr<tempClass> p1( new tempClass(6.0));
	{
		std::cout << "about to create p2" << std::endl;
		boost::shared_ptr<tempClass> p2 = p1;
		std::cout << p2 << std::endl;
		std::cout << (p2 -> data)<<std::endl;
	}

	std::cout << **p1 << std::endl;

	std::cin >> temp;
	return 0;
}
