################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../BaseInnerCurve.cpp \
../BaseInnerCurve_test.cpp \
../InstrumentDF.cpp \
../InstrumentDF_test.cpp \
../Test.cpp 

OBJS += \
./BaseInnerCurve.o \
./BaseInnerCurve_test.o \
./InstrumentDF.o \
./InstrumentDF_test.o \
./Test.o 

CPP_DEPS += \
./BaseInnerCurve.d \
./BaseInnerCurve_test.d \
./InstrumentDF.d \
./InstrumentDF_test.d \
./Test.d 


# Each subdirectory must supply rules for building sources it contributes
%.o: ../%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -I"/home/phcostello/Documents/workspace/JoshiLibrary" -O0 -g3 -Wall -c -fmessage-length=0 -fPIC -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


