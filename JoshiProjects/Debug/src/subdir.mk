################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../src/AnalyticFormulas.cpp \
../src/BSaliases.cpp \
../src/TestingMCGreeks.cpp \
../src/VanillaPayOffs.cpp 

OBJS += \
./src/AnalyticFormulas.o \
./src/BSaliases.o \
./src/TestingMCGreeks.o \
./src/VanillaPayOffs.o 

CPP_DEPS += \
./src/AnalyticFormulas.d \
./src/BSaliases.d \
./src/TestingMCGreeks.d \
./src/VanillaPayOffs.d 


# Each subdirectory must supply rules for building sources it contributes
src/%.o: ../src/%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -I"/home/phcostello/Documents/workspace/JoshiLibrary" -I"/home/phcostello/CppCode/Code from books/C++Design_Joshi/include" -O0 -g3 -Wall -c -fmessage-length=0 -fPIC -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


