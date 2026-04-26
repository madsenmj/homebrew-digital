# RV32I Digital CPU Part 6

We need one more set of tools to make a functional system: the ability to jump/branch to different places in the program. 

## Core Control Unit

We add several more functions to give us the jump/branch ability:

* `OP_B_TYPE`: Conditional branching
* `OP_J_TYPE`: Jump 
* `OP_I_JALR_TYPE`: Jump and link register

## Comparitor Unit

This unit is similar to the ALU in that we have a multiplexer to handle different comparison functions.

## Test Plan

1. Compile the assembly test code in `part_6_inst_test.rvi`: (refer to Part 1 for instructions on how to do this) `python src/rvi.py -o rom_temp.hex -x ../homebrew-digital/rv32i_digital/part_6/part_6_inst_test.rvi` and load the ROM with the formatted `.hex` file.
2. Run the simulation
3. Verify each step of the test executes correctly and each loop finishes with the correct state. See the test file for the points at which to check the register state


