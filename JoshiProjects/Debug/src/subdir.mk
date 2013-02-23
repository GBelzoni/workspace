################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../src/AnalyticFormulas.cpp \
../src/main.cpp 

OBJS += \
./src/AnalyticFormulas.o \
./src/main.o 

CPP_DEPS += \
./src/AnalyticFormulas.d \
./src/main.d 


# Each subdirectory must supply rules for building sources it contributes
src/%.o: ../src/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -I"/home/phcostello/Documents/workspace/JoshiLibrary" -I"/home/phcostello/CppCode/Code from books/C++Design_Joshi/include" -O0 -g3 -Wall -c -fmessage-length=0 -fPIC -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


