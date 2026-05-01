# RV32I Digital CPU Part 8

We add one more piece of custom control logic to the CCU: if we don't have an instruction (all `0s`), we'll halt the clock. This will make it easier to run code from other compilers. We'll also implement a 

## Compiling C Code

We test a simple program found in [fibonnacci.c](fibonacci.c). We'll need to add one line to the start of our assembly code before we compile it to set the function argument. The first step is to compile the C code into assembly languge. We use [godbolt.org](https://godbolt.org/z/TehMczdod). Verify the following settings:

1. The source is set to `C`
2. The compiler is set to "RISC-V rv32gc clang (trunk)" (the exact branch doesn't matter here)
3. The compiler options are set to `-O2 -mabi=ilp32 -march=rv32i`
4. The Output dropdown is set to have no options selected
5. The Filter dropdown has "Unused labels", "Library functions", "Directives", and "Comments" selected

Copy the output assembler code from the right-hand window. Verify that is matches the text in `fibonacci.asm`.

## Assembly to Hex

We'll use another tool, the [RISC-V Online Assembler](https://riscvasm.lucasteske.dev/#) to run the next step. Paste the assembler code into the left-hand window. We add one more line to the top of this before the `main:` function. If we want to calculate the 20th Fibonacci number, we add these lines to the top:

```
li a0, 10
li ra, 200
```

The RISC-V convention is that the input value to a function is stored in the `a0` register (corresponding to `x10` in our system). So we put the number of the sequence we want to calculate in that register before we run the function.

The second line is the return address, conventionally loaded into `x01` (named `ra`). We want to jump to a blank location in our instructions, which will halt the execution of the program.

Click the "Build" button. Copy the output from the "Code Hex Dump" window into the `rom_part_8.hex` file after the `v2.0 raw` line.

## Output Display

The RISC-V convention is that return value for functions get stored in the `a1` register (corresponding to `x11` in our system). We connect a base-10 digital display directly to this register so we have an output display.

## Test Plan

1. Follow the instructions above to create the `rom_part_8.hex` file.
2. Run the simulation
3. Verify each step of the program runs, ending on the 12th [Fibonacci number](https://www.mathsisfun.com/numbers/fibonacci-sequence.html), 144. Note that we're already calculating $F_0$ and $F_1$, so the input parameter is the $N+2$ Fibonacci number.


