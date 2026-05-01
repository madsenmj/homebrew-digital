# 32-bit RISC-V-based Computer

The goal of this project is to extend the Eater 8-bit computer into a 32-bit system based on the RISC-V ISA. 

Starting point: an April Fool's joke discussion here: https://groups.google.com/a/groups.riscv.org/g/isa-dev/c/SrujNcNc8RA/m/uTnndiPaAgAJ

And more seriously here: https://groups.google.com/a/groups.riscv.org/g/isa-dev/c/iK3enKGb5bw/m/cuVAq0J8EAAJ

A RISC-V Intro book: http://home.ustc.edu.cn/~louwenqi/reference_books_tools/Computer%20Organization%20and%20Design%20RISC-V%20edition.pdf


Another starting point: https://github.com/HarieshAnbalagan/RV32I/tree/main - a RV32I processor design. This one is turning out to be the most useful. Between it and the RISC-V documentation, that is most of the source material for this.

More resources:

* https://pages.hmc.edu/harris/ddca/ddcarv/DDCArv_AppB_Harris.pdf - a list of RISC-V opcodes
* https://docs.riscv.org/reference/isa/unpriv/rv32.html - the docs for the RV32I instruction set
* https://projectf.io/posts/riscv-cheat-sheet/ - the 32 bit cheat sheet for opcodes
* https://github.com/metastableB/RISCV-RV32I-Assembler - a python assembler for compiling programs into bytecode
* RISC-V Instruction encoder/decoder - https://luplab.gitlab.io/rvcodecjs/

Workload for loading program into rom:

1. Open the Assembler repo in a new window
2. Change the python conda environment `conda activate rvi`
3. Run the program: `python rvi.py -o rom.hex -x ..\examples\nth_fibonacci_number.rvi` where the `.rvi` program is the assembly language verison of the program
4. In the newly created `rom.hex` file, copy the hex code lines
5. Open the `rom.hex` file in the `rv32i_digital` folder and paste the hex code lines after the `v2.0 raw` line

## Tutorial

* [Part 1: Clock and Instruction Memory](part_1/README.md)
* [Part 2: Program Counter](part_2/README.md)
* [Part 3: ALU and Core Control](part_3/README.md)
* [Part 4: Immediate values and Register File](part_4/README.md)
* [Part 5: Immediate ALU Calculations](part_5/README.md)
* [Part 6: Branch and Jump](part_6/README.md)
* [Part 7: Data Memory and LSU](part_7/README.md)
* [Part 8: Halt and C programming](part_8/README.md)


