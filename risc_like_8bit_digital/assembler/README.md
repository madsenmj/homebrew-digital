# 8-Bit RISC Assembler

Workload for loading program into rom:

1. Open a terminal and `cd assembler`
2. Change the python conda environment `conda activate rvi`
3. Run the program: `python rvi.py -o rom.hex -x ..\examples\nth_fibonacci_number.rvi` where the `.rvi` program is the assembly language verison of the program
4. In the newly created `rom.hex` file, copy the hex code lines
5. Open the `rom.hex` file in the `rv32i_digital` folder and paste the hex code lines after the `v2.0 raw` line
