/*
 * BoostPython.cpp
 *
 *  Created on: Apr 26, 2013
 *      Author: phcostello
 */

//Various things I included when tryign weap an ABC, and implement virtual
//methods.

//#include <boost/python/module.hpp>
//#include <boost/python/class.hpp>
//#include <boost/python/wrapper.hpp>
//#include <boost/python/call.hpp>
//#include <boost/python/implicit.hpp>
//struct BaseInstrumentWrap : BaseInstrument, wrapper<BaseInstrument>
//{
//
//	//BaseInstrument* (BaseInstrument::*clone1)() const = &BaseInstrument::clone;
//	//BaseInstrument* (BaseInstrument::*clone2)() = &BaseInstrument::clone;
//
//	BaseInstrument* clone() const
//	{
//		return this->get_override("clone")();
//	}
//	BaseInstrument* clone()
//	{
//		return this->get_override("clone")();
//	}
//
//
//};
#include <boost/python.hpp>
#include <boost/noncopyable.hpp>
#include <BlackScholesFormulas.h>

//From Rate curves
#include <Headers/InstrumentDF.h>
#include <Headers/BaseInstrument.h>
#include <Headers/GeneralCurveInstrument.h>
#include <Headers/LinearZeroesInnerCurve.h>
#include <Headers/SimpleBootStrap.h>


//For eclipse you have to:
// !) download libboost-python
// 2) build as shared object
// 3) Add -fPic flag in project >> properties >> C++ Build Settings
// 4) Change Name of object built to the name you use in BOOST_PYTHON_MODULE(Macro): GOTO project >> properties >> C++ Build >> Settings >> Build Artefact
// 5) include /boost and /python2.7 directories
// 6) include boost_python in libraries to include project >> properties >> symbols etc >> libraries

using namespace boost::python;

SimpleBootStrap CurveBootStrapLZ()
{
	LinearZeroesInnerCurve inner_LZ_curve;

	SimpleBootStrap curve(inner_LZ_curve);

	return curve;
}


BOOST_PYTHON_MODULE(CurveRatesPy)
{
	using namespace boost::python;

	//Exposing SimpleBootStrap;
	//BoostPython automatically includes default constructor
	class_<SimpleBootStrap>("SimpleBootStrap")
			.def("getRate", &SimpleBootStrap::getRate)
			.def("fit", &SimpleBootStrap::fit)
			.def("addInstrument", &SimpleBootStrap::addInstrument);


	//This is how to expose a abstract base class. DO NOT FORGET!!
	class_<BaseInstrument, boost::noncopyable>("BaseInstrument", no_init); //Make sure you have the noncopyable and "no init" for ABC
	class_<DepoInstrument, bases< BaseInstrument > >("DepoInstrument",init<double, double>());


	//CurveRate curve functions
	def("CurveBootStrapLZ" , CurveBootStrapLZ);


}

