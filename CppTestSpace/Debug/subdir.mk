################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../TestingQLLinearInterp.cpp 

OBJS += \
./TestingQLLinearInterp.o 

CPP_DEPS += \
./TestingQLLinearInterp.d 


# Each subdirectory must supply rules for building sources it contributes
%.o: ../%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -I"/home/phcostello/Documents/workspace/JoshiLibrary" -I"/home/phcostello/CppCode/Code from books/C++Design_Joshi/include" -I/usr/include/python2.7 -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


