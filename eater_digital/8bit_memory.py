"""
A utility to program the RAM and ROM Eater 8-bit Digital computer.

Run with `python ram_rom.py`. Will output a file to the `target_file`.

Update the "Circuit Specific Settings" in Digital to point to that hex file.

"""

target_file = "rom_ram.hex"

file_header = "v2.0 raw"

n_registers = 2
rom_addresses = 9
ram_addresses = 4
bits = 8

address_instr = [[0 for y in range(n_registers)] for x in range(2**(max(ram_addresses, rom_addresses))) ]
rom_address_instr = [0 for x in range(2**rom_addresses) ]
ram_address_instr = [0 for x in range(2**ram_addresses) ]


# Instruction set used in the RAM
#       HHHH   LLLL bits in Instruction Register
NOP = 0b0000 # XXXX Not used - No Operation
LDA = 0b0001 # MMMM 4 bit memory address location to load into A Register
ADD = 0b0010 # MMMM 4 bit memory address location to store result from ALU
SUB = 0b0011 # MMMM 4 bit memory address location to store result from ALU
STA = 0b0100 # MMMM 4 bit memory address location to store A Register
LDI = 0b0101 # VVVV 4 bit value to load directly into A Register
JMP = 0b0110 # VVVV 4 bit value to load into main counter
JC  = 0b0111 # VVVV 4 bit value to load into main counter if Carry flag is set
JZ  = 0b1000 # VVVV 4 bit value to load into main counter if Zero flag is set
OUT = 0b1110 # XXXX Not used - Set Output Register from A
HLT = 0b1111 # XXXX Not used - Halt clock

# Micro Instructions used in the Program Controller
HT = 0b1000000000000000
MI = 0b0100000000000000
RI = 0b0010000000000000
RO = 0b0001000000000000
IO = 0b0000100000000000
II = 0b0000010000000000
AI = 0b0000001000000000
AO = 0b0000000100000000
EO = 0b0000000010000000
SU = 0b0000000001000000
BI = 0b0000000000100000
OI = 0b0000000000010000
CE = 0b0000000000001000
CO = 0b0000000000000100
J =  0b0000000000000010
FI = 0b0000000000000001

FLAGS_Z0C0 = 0b00
FLAGS_Z0C1 = 0b01
FLAGS_Z1C0 = 0b10
FLAGS_Z1C1 = 0b11
FLAGS = [FLAGS_Z0C0, FLAGS_Z0C1, FLAGS_Z1C0, FLAGS_Z1C1]

##############################################################
#
# Program the ROM addresses for the micro instruction set
#
##############################################################

for flag in FLAGS:
    flag_code = flag * 2**7

    inst_code = NOP * 2**3
    rom_address_instr[flag_code + inst_code + 0] = MI | CO
    rom_address_instr[flag_code + inst_code + 1] = RO | II | CE
    rom_address_instr[flag_code + inst_code + 2] = 0
    rom_address_instr[flag_code + inst_code + 3] = 0
    rom_address_instr[flag_code + inst_code + 4] = 0

    inst_code = LDA * 2**3
    rom_address_instr[flag_code + inst_code + 0] = MI | CO
    rom_address_instr[flag_code + inst_code + 1] = RO | II | CE
    rom_address_instr[flag_code + inst_code + 2] = MI | IO
    rom_address_instr[flag_code + inst_code + 3] = RO | AI
    rom_address_instr[flag_code + inst_code + 4] = 0

    inst_code = ADD * 2**3
    rom_address_instr[flag_code + inst_code + 0] = MI | CO
    rom_address_instr[flag_code + inst_code + 1] = RO | II | CE
    rom_address_instr[flag_code + inst_code + 2] = MI | IO
    rom_address_instr[flag_code + inst_code + 3] = RO | BI
    rom_address_instr[flag_code + inst_code + 4] = AI | EO | FI

    inst_code = SUB * 2**3
    rom_address_instr[flag_code + inst_code + 0] = MI | CO
    rom_address_instr[flag_code + inst_code + 1] = RO | II | CE
    rom_address_instr[flag_code + inst_code + 2] = MI | IO
    rom_address_instr[flag_code + inst_code + 3] = RO | BI
    rom_address_instr[flag_code + inst_code + 4] = AI | EO | SU | FI

    inst_code = STA * 2**3
    rom_address_instr[flag_code + inst_code + 0] = MI | CO
    rom_address_instr[flag_code + inst_code + 1] = RO | II | CE
    rom_address_instr[flag_code + inst_code + 2] = MI | IO
    rom_address_instr[flag_code + inst_code + 3] = AO | RI
    rom_address_instr[flag_code + inst_code + 4] = 0

    inst_code = LDI * 2**3
    rom_address_instr[flag_code + inst_code + 0] = MI | CO
    rom_address_instr[flag_code + inst_code + 1] = RO | II | CE
    rom_address_instr[flag_code + inst_code + 2] = IO | AI
    rom_address_instr[flag_code + inst_code + 3] = 0
    rom_address_instr[flag_code + inst_code + 4] = 0

    inst_code = JMP * 2**3
    rom_address_instr[flag_code + inst_code + 0] = MI | CO
    rom_address_instr[flag_code + inst_code + 1] = RO | II | CE
    rom_address_instr[flag_code + inst_code + 2] = IO | J
    rom_address_instr[flag_code + inst_code + 3] = 0
    rom_address_instr[flag_code + inst_code + 4] = 0

    inst_code = JC * 2**3
    rom_address_instr[flag_code + inst_code + 0] = MI | CO
    rom_address_instr[flag_code + inst_code + 1] = RO | II | CE
    # Step 2 below
    rom_address_instr[flag_code + inst_code + 3] = 0
    rom_address_instr[flag_code + inst_code + 4] = 0

    inst_code = JZ * 2**3
    rom_address_instr[flag_code + inst_code + 0] = MI | CO
    rom_address_instr[flag_code + inst_code + 1] = RO | II | CE
    # Step 2 below
    rom_address_instr[flag_code + inst_code + 3] = 0
    rom_address_instr[flag_code + inst_code + 4] = 0

    inst_code = OUT * 2**3
    rom_address_instr[flag_code + inst_code + 0] = MI | CO
    rom_address_instr[flag_code + inst_code + 1] = RO | II | CE
    rom_address_instr[flag_code + inst_code + 2] = AO | OI
    rom_address_instr[flag_code + inst_code + 3] = 0 
    rom_address_instr[flag_code + inst_code + 4] = 0 

    inst_code = HLT * 2**3
    rom_address_instr[flag_code + inst_code + 0] = MI | CO
    rom_address_instr[flag_code + inst_code + 1] = RO | II | CE
    rom_address_instr[flag_code + inst_code + 2] = HT
    rom_address_instr[flag_code + inst_code + 3] = 0 
    rom_address_instr[flag_code + inst_code + 4] = 0 

inst_code = JC * 2**3
rom_address_instr[FLAGS_Z0C0 * 2**7 + inst_code + 2] = 0
rom_address_instr[FLAGS_Z0C1 * 2**7  + inst_code + 2] = IO | J
rom_address_instr[FLAGS_Z1C0 * 2**7  + inst_code + 2] = 0
rom_address_instr[FLAGS_Z1C1 * 2**7  + inst_code + 2] = IO | J

inst_code = JZ * 2**3
rom_address_instr[FLAGS_Z0C0 * 2**7  + inst_code + 2] = 0
rom_address_instr[FLAGS_Z0C1 * 2**7  + inst_code + 2] = 0
rom_address_instr[FLAGS_Z1C0 * 2**7  + inst_code + 2] = IO | J
rom_address_instr[FLAGS_Z1C1 * 2**7  + inst_code + 2] = IO | J

##############################################################
#
# Program the RAM addresses for the program to run
#
##############################################################

ram_address_instr[0] = OUT * 2**4 + 0
ram_address_instr[1] = ADD * 2**4 + 15
ram_address_instr[2] = JC  * 2**4 + 4
ram_address_instr[3] = JMP * 2**4 + 0
ram_address_instr[4] = SUB * 2**4 + 15
ram_address_instr[5] = OUT * 2**4 + 0
ram_address_instr[6] = JZ  * 2**4 + 0
ram_address_instr[7] = JMP * 2**4 + 4
ram_address_instr[15] = 8


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