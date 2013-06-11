################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../makefile.init

RM := rm -rf

# All of the sources participating in the build are defined here
-include sources.mk
-include subdir.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(C++_DEPS)),)
-include $(C++_DEPS)
endif
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
ifneq ($(strip $(CC_DEPS)),)
-include $(CC_DEPS)
endif
ifneq ($(strip $(CPP_DEPS)),)
-include $(CPP_DEPS)
endif
ifneq ($(strip $(CXX_DEPS)),)
-include $(CXX_DEPS)
endif
ifneq ($(strip $(C_UPPER_DEPS)),)
-include $(C_UPPER_DEPS)
endif
endif

-include ../makefile.defs

# Add inputs and outputs from these tool invocations to the build variables 

# All Target
all: BoostPythonTest.so

dependents:
	-cd /home/phcostello/Documents/workspace/JoshiLibrary/Debug && $(MAKE) all
	-cd /home/phcostello/Documents/workspace/CppRate_Curve/Debug && $(MAKE) all

# Tool invocations
BoostPythonTest.so: $(OBJS) $(USER_OBJS) /home/phcostello/Documents/workspace/JoshiLibrary/Debug/libJoshiLibrary.so /home/phcostello/Documents/workspace/CppRate_Curve/Debug/libCppRate_Curve.so
	@echo 'Building target: $@'
	@echo 'Invoking: GCC C++ Linker'
	g++ -L"/home/phcostello/Documents/workspace/CppRate_Curve/Debug" -L"/home/phcostello/Documents/workspace/JoshiLibrary/Debug" -shared -o "BoostPythonTest.so" $(OBJS) $(USER_OBJS) $(LIBS)
	@echo 'Finished building target: $@'
	@echo ' '

# Other Targets
clean:
	-$(RM) $(OBJS)$(C++_DEPS)$(C_DEPS)$(CC_DEPS)$(LIBRARIES)$(CPP_DEPS)$(CXX_DEPS)$(C_UPPER_DEPS) BoostPythonTest.so
	-@echo ' '

.PHONY: all clean dependents
.SECONDARY:
/home/phcostello/Documents/workspace/JoshiLibrary/Debug/libJoshiLibrary.so:
/home/phcostello/Documents/workspace/CppRate_Curve/Debug/libCppRate_Curve.so:

-include ../makefile.targets
