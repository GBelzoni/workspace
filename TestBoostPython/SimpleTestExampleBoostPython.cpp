/*
 * BoostPython.cpp
 *
 *  Created on: Apr 26, 2013
 *      Author: phcostello
 */


#include <boost/python.hpp>
#include <BlackScholesFormulas.h>

//From Rate curves
#include <Headers/GeneralCurveInstrument.h>
#include <Headers/BaseInstrument.h>
#include <Headers/SimpleBootStrap.h>


//For eclipse you have to:
// !) download libboost-python
// 2) build as shared object
// 3) Add -fPic flag in project >> properties >> C++ Build Settings
// 4) Change Name of object built to the name you use in BOOST_PYTHON_MODULE(Macro): GOTO project >> properties >> C++ Build >> Settings >> Build Artefact
// 5) include /boost and /python2.7 directories
// 6) include boost_python in libraries to include project >> properties >> symbols etc >> libraries
// 7) Make sure you copy the lib*.so you create out of Debug into the home directory, or include otherwise

using namespace boost::python;

char const* greet()
{
	return "hello world";
}

//You need to names the BOOST_PYTHON_MODULE same as the lib*.so you will output
//NOTE:See "CurveRatesBoostPython.cpp" for example of how to handle classes, inheritance, ABC

BOOST_PYTHON_MODULE(BoostPythonTest)
{
	using namespace boost::python;
	def("greet",greet);
	def("BlackScholesCall", BlackScholesCall);

}

