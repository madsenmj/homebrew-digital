# A 16-bit variation on RISC-V

This is another project based on the work from [here](https://github.com/jeceljr/digitalCPUzoo/blob/main/drv16/README.md). It is a derivation of a RISC-V processor adapted for 16 bits. This adaptation is another variation attempting to narrow down the execution of the CPU into a *fetch* and *execute* system (two clock cycles) while leveraging a broader instruction set to eliminate the extensions needed to implement the immediate execution instructions.

The RV32I base integer set uses [4 different types of instruction formats](https://docs.riscv.org/reference/isa/unpriv/rv32.html). This project will follow a similar pattern, but for an extended 16 bit system.

|31 ... 20 | 19 18 17  16 | 15 14 13 12 | 11 10 09 08 | 07 ... 00 |
|--|------|------|-------------|----------------------------|
| 0[12] | rs2[4] | rs1[4] | rd[4] | operation[8] |

The immediate variation looks like this:

|31 ... 16 | 15 14 13 12 | 11 10 09 08 | 07 ... 00 |
|-------|------|-------------|----------------------------|
| imm[16] | rs1[4] | rd[4] | operation[8] |

There are 16 registers of 16 bits each. The program is stored in 32-bit wide memory, addressable by a 16-bit address (for a total of 64K of memory).

