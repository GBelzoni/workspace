/*
 * BoostPython.cpp
 *
 *  Created on: Apr 26, 2013
 *      Author: phcostello
 */

#include <boost/python.hpp>



char const* greet()
{
	return "hello world";
}

BOOST_PYTHON_MODULE(hello_ext)
{
	using namespace boost::python;
	def("greet",greet);
}

