# RV32I Digital CPU Part 7

The last set of components are the data memory and the Load/Store Unit (LSU)

## Core Control Unit

We add several more functions to give us control over reading/writing to data memory:

* `OP_S_TYPE`: Store
* `OP_I_LOAD_TYPE`: I Load data
* `OP_U_AUIPC_TYPE`: Add Upper Immediate to PC

This finishes covering all of the possibilities for the Core Control Unit.

## Test Plan

1. Compile the assembly test code in `part_7_inst_test.rvi`: (refer to Part 1 for instructions on how to do this) `python src/rvi.py -o rom_temp.hex -x ../homebrew-digital/rv32i_digital/part_7/part_7_inst_test.rvi` and load the ROM with the formatted `.hex` file.
2. Run the simulation
3. Verify each step of the test executes correctly and each loop finishes with the correct state. See the test file for the points at which to check the register state


