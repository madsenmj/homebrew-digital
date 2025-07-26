"""
A utility to program the RAM and ROM Eater 8-bit Relay computer.

Run with `python ram_rom.py`. Will output a file to the `target_file`.

Update the "Circuit Specific Settings" in Digital to point to that hex file.

"""

target_file = "relay_rom_ram.hex"

file_header = "v2.0 raw"

n_registers = 2
rom_addresses = 10
ram_addresses = 4
bits = 8

address_instr = [[0 for y in range(n_registers)] for x in range(2**(max(ram_addresses, rom_addresses))) ]
rom_address_instr = [0 for x in range(2**rom_addresses) ]
ram_address_instr = [0 for x in range(2**ram_addresses) ]

# TODO: Add third register
# Update load and select to a 2-4 decoder
# Change ALU functions to load to A, then copy to B
# Add a MOV B,A (to B from A) function


# Instruction set used in the RAM
#       HHHH   LLLL bits in Instruction Register
NOP = 0b0000 # XXXX Not used - No Operation
LDB = 0b0001 # MMMM 4 bit memory address location to load into B Register
ADD = 0b0010 # MMMM 4 bit memory address location to add to B
LDA = 0b0011 # MMMM 4 bit memory address location to Load into A Register
STB = 0b0100 # MMMM 4 bit memory address location to store B Register
LDI = 0b0101 # VVVV 4 bit value to load directly into B Register
JMP = 0b0110 # VVVV 4 bit value to load into main counter
JC  = 0b0111 # VVVV 4 bit value to load into main counter if Carry flag is set
JZ  = 0b1000 # VVVV 4 bit value to load into main counter if Zero flag is set
JS =  0b1001 # VVVV 4 bit value to load into main counter if Sign flag is set
STA = 0b1010 # MMMM 4 bit memory address location to store A Register
# X = 0b1011 # VVVV 4 bit value to load into main counter if Sign flag is set
NOT = 0b1100 # XXXX Not used - Inverse of B through A
INC = 0b1101 # MMMM Not used - Increment of B through A
OUT = 0b1110 # XXXX Not used - Set Output Register from B
HLT = 0b1111 # XXXX Not used - Halt clock

# Micro Instructions used in the Program Controller
HALT = 0b1000000000000000
RML  = 0b0100000000000000
LRAM = 0b0010000000000000
SRAM = 0b0001000000000000
RSI  = 0b0000100000000000
RLI  = 0b0000010000000000
RSF1 = 0b0000001000000000
RSF0 = 0b0000000100000000
F1 =   0b0000000010000000
F0 =   0b0000000001000000
RLF1 = 0b0000000000100000
RLF0 = 0b0000000000010000
ROL =  0b0000000000001000
CE =   0b0000000000000100
J =    0b0000000000000010
SCZL = 0b0000000000000001

# ALU instruction decoding
SUME = F0
INCE = F1
NOTE = F0 | F1

RSA = RSF0
RSB = RSF1
CO = RSF0 | RSF1

RLA = RLF0
RLB = RLF1
RLC = RLF0 | RLF1

FLAGS_S0C0Z0 = 0b000
FLAGS_S0C0Z1 = 0b001
FLAGS_S0C1Z0 = 0b010
FLAGS_S0C1Z1 = 0b011
FLAGS_S1C0Z0 = 0b100
FLAGS_S1C0Z1 = 0b101
FLAGS_S1C1Z0 = 0b110
FLAGS_S1C1Z1 = 0b111
FLAGS = [FLAGS_S0C0Z0, FLAGS_S0C0Z1, FLAGS_S0C1Z0, FLAGS_S0C1Z1,
         FLAGS_S1C0Z0, FLAGS_S1C0Z1, FLAGS_S1C1Z0, FLAGS_S1C1Z1]

##############################################################
#
# Program the ROM addresses for the micro instruction set
#
##############################################################

for flag in FLAGS:
    flag_code = flag * 2**7

    inst_code = NOP * 2**3
    rom_address_instr[flag_code + inst_code + 0] = RML | CO
    rom_address_instr[flag_code + inst_code + 1] = SRAM | RLI | CE
    rom_address_instr[flag_code + inst_code + 2] = 0
    rom_address_instr[flag_code + inst_code + 3] = 0
    rom_address_instr[flag_code + inst_code + 4] = 0

    inst_code = LDB * 2**3
    rom_address_instr[flag_code + inst_code + 0] = RML | CO
    rom_address_instr[flag_code + inst_code + 1] = SRAM | RLI | CE
    rom_address_instr[flag_code + inst_code + 2] = RML | RSI
    rom_address_instr[flag_code + inst_code + 3] = SRAM | RLB
    rom_address_instr[flag_code + inst_code + 4] = 0

    inst_code = ADD * 2**3
    rom_address_instr[flag_code + inst_code + 0] = RML | CO
    rom_address_instr[flag_code + inst_code + 1] = SRAM | RLI | CE
    rom_address_instr[flag_code + inst_code + 2] = RML | RSI
    rom_address_instr[flag_code + inst_code + 3] = SRAM | RLC
    rom_address_instr[flag_code + inst_code + 4] = RLA | SUME | SCZL
    rom_address_instr[flag_code + inst_code + 5] = RSA | RLB

    inst_code = LDA * 2**3
    rom_address_instr[flag_code + inst_code + 0] = RML | CO
    rom_address_instr[flag_code + inst_code + 1] = SRAM | RLI | CE
    rom_address_instr[flag_code + inst_code + 2] = RML | RSI
    rom_address_instr[flag_code + inst_code + 3] = SRAM | RLA
    rom_address_instr[flag_code + inst_code + 4] = 0

    inst_code = STB * 2**3
    rom_address_instr[flag_code + inst_code + 0] = RML | CO
    rom_address_instr[flag_code + inst_code + 1] = SRAM | RLI | CE
    rom_address_instr[flag_code + inst_code + 2] = RML | RSI
    rom_address_instr[flag_code + inst_code + 3] = RSB | LRAM
    rom_address_instr[flag_code + inst_code + 4] = 0

    inst_code = LDI * 2**3
    rom_address_instr[flag_code + inst_code + 0] = RML | CO
    rom_address_instr[flag_code + inst_code + 1] = SRAM | RLI | CE
    rom_address_instr[flag_code + inst_code + 2] = RSI | RLB
    rom_address_instr[flag_code + inst_code + 3] = 0
    rom_address_instr[flag_code + inst_code + 4] = 0

    inst_code = JMP * 2**3
    rom_address_instr[flag_code + inst_code + 0] = RML | CO
    rom_address_instr[flag_code + inst_code + 1] = SRAM | RLI | CE
    rom_address_instr[flag_code + inst_code + 2] = RSI | J
    rom_address_instr[flag_code + inst_code + 3] = 0
    rom_address_instr[flag_code + inst_code + 4] = 0

    inst_code = JC * 2**3
    rom_address_instr[flag_code + inst_code + 0] = RML | CO
    rom_address_instr[flag_code + inst_code + 1] = SRAM | RLI | CE
    # Step 2 below
    rom_address_instr[flag_code + inst_code + 3] = 0
    rom_address_instr[flag_code + inst_code + 4] = 0

    inst_code = JZ * 2**3
    rom_address_instr[flag_code + inst_code + 0] = RML | CO
    rom_address_instr[flag_code + inst_code + 1] = SRAM | RLI | CE
    # Step 2 below
    rom_address_instr[flag_code + inst_code + 3] = 0
    rom_address_instr[flag_code + inst_code + 4] = 0

    inst_code = JS * 2**3
    rom_address_instr[flag_code + inst_code + 0] = RML | CO
    rom_address_instr[flag_code + inst_code + 1] = SRAM | RLI | CE
    # Step 2 below
    rom_address_instr[flag_code + inst_code + 3] = 0
    rom_address_instr[flag_code + inst_code + 4] = 0

    inst_code = STA * 2**3
    rom_address_instr[flag_code + inst_code + 0] = RML | CO
    rom_address_instr[flag_code + inst_code + 1] = SRAM | RLI | CE
    rom_address_instr[flag_code + inst_code + 2] = RML | RSI
    rom_address_instr[flag_code + inst_code + 3] = RSA | LRAM
    rom_address_instr[flag_code + inst_code + 4] = 0

    inst_code = NOT * 2**3
    rom_address_instr[flag_code + inst_code + 0] = RML | CO
    rom_address_instr[flag_code + inst_code + 1] = SRAM | RLI | CE
    rom_address_instr[flag_code + inst_code + 2] = RLA | NOTE | SCZL
    rom_address_instr[flag_code + inst_code + 3] = RSA | RLB

    inst_code = INC * 2**3
    rom_address_instr[flag_code + inst_code + 0] = RML | CO
    rom_address_instr[flag_code + inst_code + 1] = SRAM | RLI | CE
    rom_address_instr[flag_code + inst_code + 2] = RLA | INCE | SCZL
    rom_address_instr[flag_code + inst_code + 3] = RSA | RLB

    inst_code = OUT * 2**3
    rom_address_instr[flag_code + inst_code + 0] = RML | CO
    rom_address_instr[flag_code + inst_code + 1] = SRAM | RLI | CE
    rom_address_instr[flag_code + inst_code + 2] = RSB | ROL
    rom_address_instr[flag_code + inst_code + 3] = 0 
    rom_address_instr[flag_code + inst_code + 4] = 0 

    inst_code = HLT * 2**3
    rom_address_instr[flag_code + inst_code + 0] = RML | CO
    rom_address_instr[flag_code + inst_code + 1] = SRAM | RLI | CE
    rom_address_instr[flag_code + inst_code + 2] = HALT
    rom_address_instr[flag_code + inst_code + 3] = 0 
    rom_address_instr[flag_code + inst_code + 4] = 0 

inst_code = JC * 2**3
rom_address_instr[FLAGS_S0C1Z0 * 2**7  + inst_code + 2] = RSI | J
rom_address_instr[FLAGS_S0C1Z1 * 2**7  + inst_code + 2] = RSI | J
rom_address_instr[FLAGS_S1C1Z0 * 2**7  + inst_code + 2] = RSI | J
rom_address_instr[FLAGS_S1C1Z1 * 2**7  + inst_code + 2] = RSI | J

inst_code = JZ * 2**3
rom_address_instr[FLAGS_S0C0Z1 * 2**7  + inst_code + 2] = RSI | J
rom_address_instr[FLAGS_S0C1Z1 * 2**7  + inst_code + 2] = RSI | J
rom_address_instr[FLAGS_S1C0Z1 * 2**7  + inst_code + 2] = RSI | J
rom_address_instr[FLAGS_S1C1Z1 * 2**7  + inst_code + 2] = RSI | J

inst_code = JS * 2**3
rom_address_instr[FLAGS_S1C0Z0 * 2**7  + inst_code + 2] = RSI | J
rom_address_instr[FLAGS_S1C1Z0 * 2**7  + inst_code + 2] = RSI | J
rom_address_instr[FLAGS_S1C0Z1 * 2**7  + inst_code + 2] = RSI | J
rom_address_instr[FLAGS_S1C1Z1 * 2**7  + inst_code + 2] = RSI | J


##############################################################
#
# Program the RAM addresses for the program to run
#
##############################################################

ram_address_instr[0] = LDB * 2**4 + 15
ram_address_instr[1] = NOT * 2**4 + 0
ram_address_instr[2] = INC * 2**4 + 0
ram_address_instr[3] = STB * 2**4 + 15
ram_address_instr[4] = LDI * 2**4 + 15
ram_address_instr[5] = OUT * 2**4 + 0
ram_address_instr[6] = ADD * 2**4 + 15
ram_address_instr[7] = JZ  * 2**4 + 9
ram_address_instr[8] = JMP * 2**4 + 5
ram_address_instr[9] = HLT * 2**4 + 0
ram_address_instr[15] = 3


# Combine two sets of instructions
for i,k in enumerate(rom_address_instr):
    address_instr[i][0] = k

for i,k in enumerate(ram_address_instr):
    address_instr[i][1] = k

with open(target_file, 'w') as f:
    f.write(file_header + "\n")
    for i,n in enumerate(address_instr):
        for k in range(n_registers):
            f.write("{:04x}".format(n[k]) + " ")
        if i % bits == (bits - 1):
            print(i)
            f.write("\n")