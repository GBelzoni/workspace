################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
O_SRCS += \
../SWIG/JoshiSwigged.o 

CPP_SRCS += \
../SWIG/JoshiSwigged_wrap.cpp 

OBJS += \
./SWIG/JoshiSwigged_wrap.o 

CPP_DEPS += \
./SWIG/JoshiSwigged_wrap.d 


# Each subdirectory must supply rules for building sources it contributes
SWIG/%.o: ../SWIG/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -I"/home/phcostello/Documents/workspace/JoshiLibrary" -I"/home/phcostello/CppCode/Code from books/C++Design_Joshi/include" -O0 -g3 -Wall -c -fmessage-length=0 -fPIC -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


