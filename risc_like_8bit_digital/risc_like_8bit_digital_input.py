"""
A utility to program the RAM and ROM Eater 8-bit Digital computer.

Run with `python risc_like_8bit_digital_input.py`. Will output a file to the `target_file`.

Update the "Circuit Specific Settings" in Digital to point to that hex file.

"""

def dot(K, L):
   if len(K) != len(L):
      return 0

   return sum(i[0] * i[1] for i in zip(K, L))

def set_addr(control, source, destination):
    CO = 2**14 # LEFTMOST 2 BITS
    DO = 2**0 # RIGHTMOST 6 BITS
    SO = 2**6 # STARTS AT BIT 7 FROM THE RIGHT
    CL = [CO, SO, DO]
    return dot(CL, [control, source, destination])

target_file = "rom.hex"

file_header = "v2.0 raw"

rom_addresses = 8
bits = 16

address_instr = [0  for x in range(2** rom_addresses) ]
rom_address_instr = [0 for x in range(2**rom_addresses) ]


# Instruction set used in the Input
ZERO  =	 0
ONE	  =  1
PC	  =  2
REG_A =  3
REG_B =  4
REG_C =  5
REG_D =  6
NOT   =  7
SLL   =  8 # SHIFT LEFT LOGICAL
SRL   =  9 # SHIFT RIGHT LOGICAL
SLA   = 10 # SHFIT LEFT ARITHMETIC
SRA   = 11 # SHIFT RIGHT ARITHMETIC
EQZ   = 12 # EQUAL TO ZERO
NEZ   = 13 # NOT EQUAL TO ZERO
NEG   = 14 # LEFTMOST BIT IS ONE
ADD_1 = 15
ADD_2 = 16 
ADD_C = 17 # ADD CARRY BIT
SUB_1 = 19
SUB_2 = 19
SUB_C = 20 # SUBTRACT CARRY BIT
INC   = 21 # INCREMENT BY ONE
AND_1 = 22
AND_2 = 23
OR_1  = 24
OR_2  = 25
XOR_1 = 26
XOR_2 = 27
SLT_1 = 28 
SLT_2 = 29 #SELECT LESS THAN SIGNED
SLU_1 = 30
SLU_2 = 31 #SELECT LESS THAN UNSIGNED
JMP   = 32 # JUMP TARGET ADDRESS
PC_IN = 33 # PROGRAM COUNTER INCREMENT

BI1   = 36 # BRANCH IF ONE
BEQ_1 = 37
BEQ_2 = 38 # BRANCH IF EQUAL
BNE_1 = 39
BNE_2 =	40 # BRANCH IF NOT EQUAL
BLT_1 = 41
BLT_2 = 42 # BRANCH IF 2 IS LESS THAN 1
BGT_1 = 43
BGT_2 = 44 # BRANCH IF 2 IS GREATER THAN 1
BLU_1 = 45
BLU_2 = 46 # BRANCH IF 2 IS LESS THAN 1 UNSIGNED
BGU_1 = 47
BGU_2 = 48 # BRANCH IF 2 IS GREATER THAN 1 UNSIGNED
GTJ   = 49 # GOTO JUMP DIRECTLY

# CONTROL
REG  = 0
IM   = 1
HALT = 3



##############################################################
#
# Program the OUTPUT
#
##############################################################

address_instr[0] = set_addr(IM, 129, REG_A)
address_instr[1] = set_addr(IM, 32, REG_B)
address_instr[2] = set_addr(REG, REG_B, ADD_2)

address_instr[3] = set_addr(IM, 0, GTJ)
address_instr[4] = set_addr(REG, REG_A, ADD_1)
address_instr[5] = set_addr(REG, ADD_2, REG_A)
address_instr[6] = set_addr(IM, 15, JMP)
address_instr[7] = set_addr(REG, ADD_C, BI1)
address_instr[8] = set_addr(IM, 3, JMP)
address_instr[9] = set_addr(IM, 1, GTJ)
address_instr[15] = set_addr(HALT, 0, 0)

with open(target_file, 'w') as f:
    f.write(file_header + "\n")
    for k in address_instr:
        f.write("{:04x}".format(k) + " ")
