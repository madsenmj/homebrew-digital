# RV32I Digital CPU Part 2

We add the program counter in this part. The test file/ROM is the same as Part 1 (no changes to the ROM file). We verify the functionality of the program counter by incrementing the clock one step at a time.

We add two new items to the "To be Implemented" box:

1. `alu_output`: when we eventually get to jumps/branches, this will be used to overwrite the program counter to jump to a specific point in the program
2. `pc_mux_sel`: this flag is used to tell the program counter when to use the `alu_output` for the next step in the program

## Test Plan

1. Verify that the ROM is loading the Part 1 hex file
2. Run the simulation
3. Manually step the clock and verify that the PC increments in steps of 4
4. Select the `Reset` input. Verify that the next clock step resets the PC to `0`
5. Add an input of `20` (base 10, or `0x14` in hex) to the `alu_output` input. Select the `pc_muxsel` input as well. Verify that the next clock cycle sets the PC to `14` and the Instruction Memory to `002081B3`

