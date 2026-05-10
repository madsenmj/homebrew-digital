# RISC-Like Digital Project

The goal of this project is to translate the command-based control ideas of the RISC-V architecture into a register-based CPU in preparation for conversion into a relay computer.

## Source Material

I'm leaning heavily on the [Micro8](https://github.com/Inspiaaa/Micro8). This is the starting point for my ISA.

I'm also leaning on this [Assembler](https://github.com/metastableB/RISCV-RV32I-Assembler) which I've modified to work with my 8-bit ISA. 

The assembler instructions are in the [README](assembler/README.md).

## ISA

| F | E | D | C | B | A | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 | Type | OP | Description | Usage | Calculation |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | :---: | :---: | :---: | :---: | :---: | :---- | :---- | :---- | :---- | :---- |
|  |  |  |  |  |  |  |  |  |  |  | 0 | 0 | 0 | 0 | 0 | N | nop | nop |  |  |
| imm 4:0 |  |  |  |  | rs1 |  |  | rd |  |  | 0 | 0 | 1 | 0 | 0 | I | lb | load byte | lb rd, imm(rs1) | rd \= mem\[rs1 \+ imm\] |
| imm 7:0 |  |  |  |  |  |  |  | rd |  |  | 0 | 1 | 0 | 0 | 0 | U\_S | aipc | add imm to PC | aipc rd imm | rd \= imm \+ PC |
| imm 4:0 |  |  |  |  | rs1 |  |  | rd |  |  | 0 | 1 | 1 | 0 | 0 | I | lbu | load unsigned | lbu rd uimm(rs1) | rd \= mem\[rs1 \+ uimm\] |
|  |  |  |  |  | rs1 |  |  | rd |  |  | 1 | 0 | 0 | 0 | 0 | C | mv | move / copy | mv rd, rs | rd \= rs1 |
| imm 7:0 |  |  |  |  |  |  |  | rd |  |  | 1 | 0 | 1 | 0 | 0 | U\_S | li | load immediate | li rd, imm\[8\] | rd \= imm |
|  |  |  |  |  | rs1 |  |  | rd |  |  | 1 | 1 | 0 | 0 | 0 | C | neg | negate | neg rd rs | rd \= \-rs1 |
| imm 4:3 |  | rs2 |  |  | rs1 |  |  | imm 2:0 |  |  | 1 | 1 | 1 | 0 | 0 | S | sb | store byte | sb rs2, uimm(rs1) | mem\[rs1 \+ uimm\] \= rs2 |
|  |  | rs2 |  |  | rs1 |  |  | rd |  |  | 0 | 0 | 0 | 1 | 0 | R | add | add | add rd rs1 rs2 | rd \= rs1 \+ rs2 |
|  |  | rs2 |  |  | rs1 |  |  | rd |  |  | 0 | 0 | 1 | 1 | 0 | R | sub | sub | sub rd rs1 rs2 | rd \= rs1 \- rs2 |
|  |  | rs2 |  |  | rs1 |  |  | rd |  |  | 0 | 1 | 0 | 1 | 0 | R | mul | mulitply | mul rd rs1 rs2 | rd \= rs1 \* rs2 |
|  |  | rs2 |  |  | rs1 |  |  | rd |  |  | 0 | 1 | 1 | 1 | 0 | R | sll | shift left logical | sll rd rs1 rs2 | rd \= rs1 \<\< rs2\[0:2\] |
|  |  | rs2 |  |  | rs1 |  |  | rd |  |  | 1 | 0 | 0 | 1 | 0 | R | srl | shift right logical | srl rd rs1 rs2 | rd \= rs1 \>\> rs2\[0:2\] |
|  |  | rs2 |  |  | rs1 |  |  | rd |  |  | 1 | 0 | 1 | 1 | 0 | R | and | bitwise and | and rd rs1 rs2 | rd \= rs1 & rs2 |
|  |  | rs2 |  |  | rs1 |  |  | rd |  |  | 1 | 1 | 0 | 1 | 0 | R | or | bitwise or | or rd rs1 rs2 | rd \= rs1 | rs2 |
|  |  | rs2 |  |  | rs1 |  |  | rd |  |  | 1 | 1 | 1 | 1 | 0 | R | xor | bitwise xor | xor rd rs1 rs2 | rd \= rs1 ^ rs2 |
| imm 7:0 |  |  |  |  |  |  |  | rd |  |  | 0 | 0 | 0 | 0 | 1 | U | addi | add immediate | addi rd imm | rd \+= imm |
| imm 7:0 |  |  |  |  |  |  |  | rd |  |  | 0 | 0 | 1 | 0 | 1 | U | subi | sub immediate | subi rd imm | rd \-= imm |
| imm 7:0 |  |  |  |  |  |  |  | rd |  |  | 0 | 1 | 0 | 0 | 1 | U | muli | multiply imm. | muli rd imm | rd \*= imm |
| imm 7:0 |  |  |  |  |  |  |  | rd |  |  | 0 | 1 | 1 | 0 | 1 | U | slli | shift left logical imm. | slli rd imm | rd \<\<= imm\[0:2\] |
| imm 7:0 |  |  |  |  |  |  |  | rd |  |  | 1 | 0 | 0 | 0 | 1 | U | srli | shift right logical imm. | srli rd imm | rd \>\>= imm\[0:2\] |
| imm 7:0 |  |  |  |  |  |  |  | rd |  |  | 1 | 0 | 1 | 0 | 1 | U | andi | bitwise and imm. | andi rd imm | rd &= imm |
| imm 7:0 |  |  |  |  |  |  |  | rd |  |  | 1 | 1 | 0 | 0 | 1 | U | ori | bitwise or imm. | ori rd imm | rd |= imm |
| imm 7:0 |  |  |  |  |  |  |  | rd |  |  | 1 | 1 | 1 | 0 | 1 | U | xori | bitwise xor imm. | xori rd imm | rd ^= imm |
| imm 7:0 |  |  |  |  |  |  |  |  |  |  | 0 | 0 | 0 | 1 | 1 | J1 | j | jump | j label | pc \= uimm |
| imm 4:3 |  | rs2 |  |  | rs1 |  |  | imm 2:0 |  |  | 0 | 0 | 1 | 1 | 1 | B | beq | branch on equal | beq rs1 rs2 label | if (rs1 \== rs2) pc \+= imm |
|  |  |  |  |  |  |  |  | rd |  |  | 0 | 1 | 0 | 1 | 1 | J2 | jr | jump register | jr rd | pc \= rd |
| imm 4:3 |  | rs2 |  |  | rs1 |  |  | imm 2:0 |  |  | 0 | 1 | 1 | 1 | 1 | B | bne | branch on not equal | bne rs1 rs2 label | if (rs1 \!= rs2) pc \+= imm |
| imm 7:0 |  |  |  |  |  |  |  | rd |  |  | 1 | 0 | 0 | 1 | 1 | U\_J | jal | jump and link | jal rd, label | rd \= pc+1, pc \= uimm |
| imm 4:3 |  | rs2 |  |  | rs1 |  |  | imm 2:0 |  |  | 1 | 0 | 1 | 1 | 1 | B | bltu | branch on less than (unsigned) | bltu rs1 rs2 label | if (rs1 \< rs2) pc \+= imm |
| imm 4:0 |  |  |  |  | rs1 |  |  | rd |  |  | 1 | 1 | 0 | 1 | 1 | J3 | jalr | jump and link register | jalr rd, rs, imm | rd \= pc+1, pc \= rs1 \+ SignExt(imm) |
| imm 4:3 |  | rs2 |  |  | rs1 |  |  | imm 2:0 |  |  | 1 | 1 | 1 | 1 | 1 | B | bgeu | branch on greater than or equal (unsigned) | bgeu rs1 rs2 label | if (rs1 \>= rs2) pc \+= imm |


## Target goals:

* No ICs - the input is simulated through a ROM, but could easily be substituted with a paper or tape drive input
* Program Memory is held by 16-bit words stored in registers
* Registers, Logic, and Control are together in the register array
* Output via LEDs but could be updated to paper or tape


## TODO

* Set up the clock
* Set up the instruction memory and loader - loading from a ROM in Digital to a second memory bank (simulating loading from an external source)
* Set up the program counter
* Start with the ALU and the R-type instructions
* Add the Register bank
* Add the immediate types
* Add branch and jump
* Add data memory
* Add IO and finalize CPU

