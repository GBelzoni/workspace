/*
 * BoostPython.cpp
 *
 *  Created on: Apr 26, 2013
 *      Author: phcostello
 */

#include <boost/python.hpp>
#include <BlackScholesFormulas.h>

//For eclipse you have to:
// !) download libboost-python
// 2) build as shared object
// 3) Add -fPic flag in project >> properties >> C++ Build Settings
// 4) Change Name of object built to the name you use in BOOST_PYTHON_MODULE(Macro): GOTO project >> properties >> C++ Build >> Settings >> Build Artefact
// 5) include /boost and /python2.7 directories
// 6) include boost_python in libraries to include project >> properties >> symbols etc >> libraries



char const* greet()
{
	return "hello world";
}

BOOST_PYTHON_MODULE(hello_ext)
{
	using namespace boost::python;
	def("greet",greet);
	def("BlackScholesCall", BlackScholesCall);


}

