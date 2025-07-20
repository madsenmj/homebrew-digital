"""
A utility to program the two EEPROMs used in the Eater 8-bit IC computer.

Run with `python eeprom_9x8x2.py`. Will output a file to the `target_file`.

Update the "Circuit Specific Settings" in Digital to point to that hex file.

"""

target_file = "eeprom_9x8x2.hex"

file_header = "v2.0 raw"

addresses = 9
bits = 8

total_registers = 2

pc_registers = 2
HT = [0b10000000,0]
MI = [0b01000000,0]
RI = [0b00100000,0]
RO = [0b00010000,0]
IO = [0b00001000,0]
II = [0b00000100,0]
AI = [0b00000010,0]
AO = [0b00000001,0]
EO = [0,0b10000000]
SU = [0,0b01000000]
BI = [0,0b00100000]
OI = [0,0b00010000]
CE = [0,0b00001000]
CO = [0,0b00000100]
J =  [0,0b00000010]
FI = [0,0b00000001]

address_instr = [[0 for y in range(total_registers)] for x in range(2**addresses) ]

FLAGS_Z0C0 = 0b000000000
FLAGS_Z0C1 = 0b010000000
FLAGS_Z1C0 = 0b100000000
FLAGS_Z1C1 = 0b110000000
FLAGS = [FLAGS_Z0C0, FLAGS_Z0C1, FLAGS_Z1C0, FLAGS_Z1C1]

for flag in FLAGS:
    for k in range(pc_registers):
        #NOP 0000
        inst_code = 0b0000000
        address_instr[flag + inst_code + 0][k] = MI[k] | CO[k]
        address_instr[flag + inst_code + 1][k] = RO[k] | II[k] | CE[k]
        address_instr[flag + inst_code + 2][k] = 0
        address_instr[flag + inst_code + 3][k] = 0
        address_instr[flag + inst_code + 4][k] = 0

        #LDA 0001
        inst_code = 0b0001000
        address_instr[flag + inst_code + 0][k] = MI[k] | CO[k]
        address_instr[flag + inst_code + 1][k] = RO[k] | II[k] | CE[k]
        address_instr[flag + inst_code + 2][k] = MI[k] | IO[k]
        address_instr[flag + inst_code + 3][k] = RO[k] | AI[k]
        address_instr[flag + inst_code + 4][k] = 0

        #ADD 0010
        inst_code = 0b0010000
        address_instr[flag + inst_code + 0][k] = MI[k] | CO[k]
        address_instr[flag + inst_code + 1][k] = RO[k] | II[k] | CE[k]
        address_instr[flag + inst_code + 2][k] = MI[k] | IO[k]
        address_instr[flag + inst_code + 3][k] = RO[k] | BI[k]
        address_instr[flag + inst_code + 4][k] = AI[k] | EO[k] | FI[k]

        #SUB 0011
        inst_code = 0b0011000
        address_instr[flag + inst_code + 0][k] = MI[k] | CO[k]
        address_instr[flag + inst_code + 1][k] = RO[k] | II[k] | CE[k]
        address_instr[flag + inst_code + 2][k] = MI[k] | IO[k]
        address_instr[flag + inst_code + 3][k] = RO[k] | BI[k]
        address_instr[flag + inst_code + 4][k] = AI[k] | EO[k] | SU[k] | FI[k]

        #STA 0100
        inst_code = 0b0100000
        address_instr[flag + inst_code + 0][k] = MI[k] | CO[k]
        address_instr[flag + inst_code + 1][k] = RO[k] | II[k] | CE[k]
        address_instr[flag + inst_code + 2][k] = MI[k] | IO[k]
        address_instr[flag + inst_code + 3][k] = AO[k] | RI[k]
        address_instr[flag + inst_code + 4][k] = 0

        #LDI 0101
        inst_code = 0b0101000
        address_instr[flag + inst_code + 0][k] = MI[k] | CO[k]
        address_instr[flag + inst_code + 1][k] = RO[k] | II[k] | CE[k]
        address_instr[flag + inst_code + 2][k] = IO[k] | AI[k]
        address_instr[flag + inst_code + 3][k] = 0
        address_instr[flag + inst_code + 4][k] = 0

        #JMP 0110
        inst_code = 0b0110000
        address_instr[flag + inst_code + 0][k] = MI[k] | CO[k]
        address_instr[flag + inst_code + 1][k] = RO[k] | II[k] | CE[k]
        address_instr[flag + inst_code + 2][k] = IO[k] | J[k]
        address_instr[flag + inst_code + 3][k] = 0
        address_instr[flag + inst_code + 4][k] = 0

        #JC 0111
        inst_code = 0b0111000
        address_instr[flag + inst_code + 0][k] = MI[k] | CO[k]
        address_instr[flag + inst_code + 1][k] = RO[k] | II[k] | CE[k]
        # Step 2 below
        address_instr[flag + inst_code + 3][k] = 0
        address_instr[flag + inst_code + 4][k] = 0

        #JZ 1000
        inst_code = 0b1000000
        address_instr[flag + inst_code + 0][k] = MI[k] | CO[k]
        address_instr[flag + inst_code + 1][k] = RO[k] | II[k] | CE[k]
        # Step 2 below
        address_instr[flag + inst_code + 3][k] = 0
        address_instr[flag + inst_code + 4][k] = 0

        #OUT 1110
        inst_code = 0b1110000
        address_instr[flag + inst_code + 0][k] = MI[k] | CO[k]
        address_instr[flag + inst_code + 1][k] = RO[k] | II[k] | CE[k]
        address_instr[flag + inst_code + 2][k] = AO[k] | OI[k]
        address_instr[flag + inst_code + 3][k] = 0 
        address_instr[flag + inst_code + 4][k] = 0 

        #HLT 1111
        inst_code = 0b1111000
        address_instr[flag + inst_code + 0][k] = MI[k] | CO[k]
        address_instr[flag + inst_code + 1][k] = RO[k] | II[k] | CE[k]
        address_instr[flag + inst_code + 2][k] = HT[k]
        address_instr[flag + inst_code + 3][k] = 0 
        address_instr[flag + inst_code + 4][k] = 0 


for k in range(pc_registers):
    #JC 0111
    inst_code = 0b0111000
    address_instr[FLAGS_Z0C0 + inst_code + 2][k] = 0
    address_instr[FLAGS_Z0C1 + inst_code + 2][k] = IO[k] | J[k]
    address_instr[FLAGS_Z1C0 + inst_code + 2][k] = 0
    address_instr[FLAGS_Z1C1 + inst_code + 2][k] = IO[k] | J[k]

    #JZ 1000
    inst_code = 0b1000000
    address_instr[FLAGS_Z0C0 + inst_code + 2][k] = 0
    address_instr[FLAGS_Z0C1 + inst_code + 2][k] = 0
    address_instr[FLAGS_Z1C0 + inst_code + 2][k] = IO[k] | J[k]
    address_instr[FLAGS_Z1C1 + inst_code + 2][k] = IO[k] | J[k]


with open(target_file, 'w') as f:
    f.write(file_header + "\n")

    for i,n in enumerate(address_instr):
        for k in range(total_registers):
            f.write("{:02x}".format(n[k]) + " ")
        if i % bits == (bits - 1):
            print(i)
            f.write("\n")