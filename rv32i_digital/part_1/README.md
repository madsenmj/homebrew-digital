# RV32I Digital CPU Part 1

The first step is to get the clock running and to set up the instruction module. 

## The Clock

We implement a simple clock with the following functionality:

1. It has a manual/automatic function that switches from a single manual input
2. It has a single step button that pulses the clock once
3. It has a Halt function that can stop the clock manually or (for future implementations) in code
4. It outputs both clock high and low

## The Instruction Memory

This is a ROM module that reads a file and stores it for use by the CPU. When the Program Counter (`PC`) is incremented by a step-size of 4 (as per the RISC-V specifications), the instruction memory module outputs the next instruction on the `INSTRUCTION` bus.

To load the program:

1. Open the Assembler repo in a new window
2. Change the python conda environment `conda activate rvi`
3. Run the program: `python src/rvi.py -o rom_temp.hex -x ../homebrew-digital/rv32i_digital/part_1/part_1_inst_test.rvi` where the `.rvi` program is the assembly language verison of the program
4. In the newly created `rom_temp.hex` file, copy the hex code lines
5. Open the `rom_part1.hex` file in the `rv32i_digital` folder and paste the hex code lines after the `v2.0 raw` line
6. Right-click on the `Instruction ROM` component in Digital, click on the `Advanced` tab and select the `rom_part1.hex` file to use as the data for the ROM.

## Test Plan

Run the Digital simulation. Verify that the instruction display corresponds to the hex file contents. Verify that incrementing the `PC` by a step size of 4 updates the instruction.
