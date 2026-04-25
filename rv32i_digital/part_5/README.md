# RV32I Digital CPU Part 5

We now add the immediate ALU functions that let us add more values to the register file.

## Core Control Unit

We add one more function: the `OP_I_ALU_TYPE` which enables immediate ALU operations on (small) constant values.

## Port A & B MUX

We finally connect inputs to the `a` and `b` variables. These are controlled by the Core Control Unit and redirect inputs to the ALU depending on which instruction we're running. We'll test this functionality in our test plan, too, by testing the *R-type* functions again.

## Test Plan

1. Compile the assembly test code in `part_5_inst_test.rvi`: (refer to Part 1 for instructions on how to do this) `python src/rvi.py -o rom_temp.hex -x ../homebrew-digital/rv32i_digital/part_5/part_5_inst_test.rvi` and load the ROM with the formatted `.hex` file.
2. Run the simulation
3. For each step in the instructions: 
    1. Verify that the `OP_I_ALU_TYPE` output is green for the first set of instructions and `OP_R_TYPE` for the second set.
    2. Verify that the `IMM` value is correct.
    3. Verify that the correct values are in the `a` and `b` variables and that the output of the ALU is correct.
    4. After the instruction executes, verify that the correct value was loaded into the appropriate register.


