# RV32I Digital CPU Part 4

The next step towards a function system is to build the register file and add load immediate functionality.

## Core Control Unit

We add one more function: the `U_LUI_TYPE` which enables loading larger values. This loads the immediate value (from the assembly code) into the upper part of the value (shifted by 12 bits).

## Imm Sign Extender

This block takes in the instruction and parses immediate values based on the different instruction types. We implement all 5 types here, even though we're only using two of them at the moment. We'll test the rest of them in the future.

## RD MUX

This block picks which of the different possible outputs we store into the register file. We're only using the `IMM` values here. The other functionality will be tested in the future.

## Register File

This is the most complicated block so far. We need 32 different registers, each individually addressable, resettable, and readable into two separate busses. Each register has this functionality and is then duplicated across all 32 registers.

Note that the `x00` register is special - it is a read-only register with a fixed value of `0`.


## Test Plan

1. Compile the assembly test code in `part_4_inst_test.rvi`: (refer to Part 1 for instructions on how to do this) `python src/rvi.py -o rom_temp.hex -x ../homebrew-digital/rv32i_digital/part_4/part_4_inst_test.rvi` and load the ROM with the formatted `.hex` file.
2. Run the simulation
3. For each step in the instructions: 
    1. Verify that the `OP_U_LUI_TYPE` output is green
    2. Verify that the `IMM` value is shifted to the left by 12 bits. In hex these should be `1000`, `2000`, `4000`, and `8000`.
    3. After the instruction executes, verify that the correct value was loaded into the appropriate register.


