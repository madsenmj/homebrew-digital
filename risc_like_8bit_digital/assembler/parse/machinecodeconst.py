#
# @author:Don Dennis
# 8-bit Modified: MJ Madsen
# machinecodeconst.py
#
# Constants and variable declaring various
# machine instructions


class MachineCodeConst:
    # Definition of opcodes used in assembly language instructions
    INSTR_NOP = 'nop'
    INSTR_LB = 'lb'
    INSTR_AIPC = 'aipc'
    INSTR_LBU = 'lbu'
    INSTR_MV = 'mv'
    INSTR_LI = 'li'
    INSTR_NEG = 'neg'
    INSTR_SB = 'sb'
    INSTR_ADD = 'add'
    INSTR_SUB = 'sub'
    INSTR_MUL = 'mul'
    INSTR_SLL = 'sll'
    INSTR_SRL = 'srl'
    INSTR_AND = 'and'
    INSTR_OR = 'or'
    INSTR_XOR = 'xor'
    INSTR_ADDI = 'addi'
    INSTR_SUBI = 'subi'
    INSTR_MULI = 'muli'   
    INSTR_SLLI = 'slli'
    INSTR_SRLI = 'srli'
    INSTR_ANDI = 'andi'
    INSTR_ORI = 'ori'
    INSTR_XORI = 'xori'
    INSTR_J = 'j'
    INSTR_BEQ = 'beq'
    INSTR_JR = 'jr'
    INSTR_BNE = 'bne'
    INSTR_JAL = 'jal'
    INSTR_BLTU = 'bltu'
    INSTR_JALR = 'jalr'
    INSTR_BGEU = 'bgeu'


    # All reserved opcodes
    ALL_INSTR = [INSTR_NOP, INSTR_LB, INSTR_AIPC,
                 INSTR_LBU, INSTR_MV, INSTR_LI,
                 INSTR_NEG, INSTR_SB, INSTR_ADD,
                 INSTR_SUB, INSTR_MUL,INSTR_SLL,
                 INSTR_SRL, INSTR_AND,INSTR_OR,
                 INSTR_XOR, INSTR_ADDI,INSTR_SUBI,
                 INSTR_MULI,INSTR_SLLI,INSTR_SRLI,
                 INSTR_ANDI,INSTR_ORI,INSTR_XORI,
                 INSTR_J,INSTR_BEQ,INSTR_JR,INSTR_BNE,
                 INSTR_JAL,INSTR_BLTU,INSTR_JALR,INSTR_BGEU
                 ]
    # All instruction in a type
    INSTR_TYPE_N = [INSTR_NOP]
    INSTR_TYPE_U = [INSTR_ADDI,INSTR_SUBI,
                    INSTR_MULI,INSTR_SLLI,INSTR_SRLI,
                    INSTR_ANDI,INSTR_ORI,INSTR_XORI]
    INSTR_TYPE_US = [INSTR_LI, INSTR_AIPC]
    INSTR_TYPE_UJ = [INSTR_J,INSTR_JR,INSTR_JAL]
    INSTR_TYPE_J = [INSTR_JALR]
    INSTR_TYPE_S = [INSTR_SB]
    INSTR_TYPE_B = [INSTR_BEQ, INSTR_BNE,
                     INSTR_BLTU, INSTR_BGEU]
    INSTR_TYPE_I = [INSTR_LB, INSTR_LBU]
    INSTR_TYPE_C = [INSTR_MV, INSTR_NEG]
    INSTR_TYPE_R = [INSTR_ADD, INSTR_SUB,  INSTR_MUL,
                    INSTR_SLL, INSTR_XOR,
                    INSTR_SRL, INSTR_OR, INSTR_AND]

    # Binary Opcodes
    BOP_SYSTEM = '00'
    BOP_ARITH = '10'
    BOP_ARITHI = '01'
    BOP_JPBR = '11'

    # The instruction in each distinct binary opcode
    INSTR_BOP_SYSTEM = [INSTR_NOP, INSTR_LB, INSTR_LBU, INSTR_AIPC, 
                        INSTR_LI, INSTR_SB,INSTR_MV, INSTR_NEG]
    INSTR_BOP_ARITH = [INSTR_ADD, INSTR_SUB, INSTR_MUL,
                       INSTR_SLL, INSTR_SRL, INSTR_XOR,
                        INSTR_OR, INSTR_AND]
    INSTR_BOP_ARITHI = [INSTR_ADDI, INSTR_SUBI, INSTR_MULI,
                        INSTR_ORI, INSTR_XORI, INSTR_ANDI,
                        INSTR_SLLI, INSTR_SRLI]
    INSTR_BOP_JPBR = [ INSTR_BEQ, INSTR_BNE, INSTR_BLTU, INSTR_BGEU, 
                      INSTR_J, INSTR_JR, INSTR_JAL, INSTR_JALR]


    # FUNCT for each instruction type
    FUNCT3_SYSTEM = {
        INSTR_NOP: '000',
        INSTR_LB: '001',
        INSTR_AIPC: '010',
        INSTR_LBU: '011',
        INSTR_MV: '100',
        INSTR_LI: '101',
        INSTR_NEG: '110',
        INSTR_SB: '111',
    }


    FUNCT3_ARITHI = {
        INSTR_ADDI: '000',
        INSTR_SUBI: '001',
        INSTR_MULI: '010',
        INSTR_SLLI: '011',
        INSTR_SRLI: '100',
        INSTR_ANDI: '101',
        INSTR_ORI:  '110',
        INSTR_XORI: '111',
    }

    FUNCT3_ARITH = {
        INSTR_ADD: '000',
        INSTR_SUB: '001',
        INSTR_MUL: '010',
        INSTR_SLL: '011',
        INSTR_SRL: '100',
        INSTR_AND: '101',
        INSTR_OR:  '110',
        INSTR_XOR: '111',
    }

    FUNCT3_JPBR = {
        INSTR_J: '000',
        INSTR_BEQ: '001',
        INSTR_JR: '010',
        INSTR_BNE: '011',
        INSTR_JAL: '100',
        INSTR_BLTU: '101',
        INSTR_JALR:  '110',
        INSTR_BGEU: '111',
    }
