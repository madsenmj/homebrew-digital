# RV32I Digital CPU Part 3

We add the ALU and the first part of the Core Control Unit in this part. We'll be focusing specifically on decoding the *R-type* instructions. We also introduce a number of new items to the "To be Implemented" box:

1. A new data type `imm_select` that will be used to determine what type (if any) of immediate value to parse
2. A new data type `load_store_type` that will be used later
3. A new data type `branch_op_sel` that will be used later
4. A new data type `reg_write_data_sel` that will be used later
5. Two new inputs `a` and `b` that are the input data into the ALU

We also introduce the data type `alu_op_sel` that controls which function we're using from the ALU. The other control flags in the list in the Core Control Unit will be used later.

## Test Plan

1. Compile the assembly test code in `part_3_inst_test.rvi`: (refer to Part 1 for instructions on how to do this) `python src/rvi.py -o rom_temp.hex -x ../homebrew-digital/rv32i_digital/part_3/part_3_inst_test.rvi` and load the ROM with the formatted `.hex` file.
2. Run the simulation
3. For each step in the instructions: 
    1. Verify that the `OP_R_TYPE` output is green (i.e. the instruction is read as an R-type instruction)
    2. Verify that the `alu_op_sel` variable has selected the correct function - see the listing in the `part_3_inst_test.rvi` file
    3. Update the values in the `a` and `b` busses and verify that the output of the `ALU` matches these inputs and the selected function


