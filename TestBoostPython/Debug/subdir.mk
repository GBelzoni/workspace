################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../SimpleTestExampleBoostPython.cpp 

OBJS += \
./SimpleTestExampleBoostPython.o 

CPP_DEPS += \
./SimpleTestExampleBoostPython.d 


# Each subdirectory must supply rules for building sources it contributes
%.o: ../%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -I"/home/phcostello/Documents/workspace/CppRate_Curve" -I"/home/phcostello/Documents/workspace/JoshiLibrary" -I/usr/include/boost -I/usr/include/python2.7 -I"/home/phcostello/CppCode/Code from books/C++Design_Joshi/include" -I"/home/phcostello/Documents/workspace/CppRate_Curve/Headers" -O0 -g3 -Wall -c -fmessage-length=0 -fPIC -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


