################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../src/EquityOption.cpp 

OBJS += \
./src/EquityOption.o 

CPP_DEPS += \
./src/EquityOption.d 


# Each subdirectory must supply rules for building sources it contributes
src/%.o: ../src/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -I/usr/include/c++/4.6.3 -I/usr/lib/gcc/x86_64-linux-gnu/4.6/include-fixed -I/usr/lib/gcc/x86_64-linux-gnu/4.6.3/include -I/usr/include/ql -O3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


