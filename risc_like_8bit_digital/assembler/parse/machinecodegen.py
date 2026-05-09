#
# @author:Don Dennis
# 8-bit Modified: MJ Madsen
# MachineCodeGen.py
#
# Conver the tokenized assembly instruction to
# corresponding machine code

from parse.cprint import cprint as cp
from parse.machinecodeconst import MachineCodeConst


class MachineCodeGenerator:
    CONST = MachineCodeConst()

    def __init__(self):
        '''
        Class that implements the machine code generation part
        for 8-bit subset.
        '''
        pass

    def get_bin_register(self, r):
        '''
        converts the register in format
        r'[0-9]' to its equivalent
        binary
        '''
        r = r[1:]
        try:
            r = int(r)
        except:
            cp.cprint_fail("Internal Error: get_bin_register:" +
                          " Register could not be parsed")
        assert(r >= 0)
        assert(r < 8)
        rbin = format(r, '03b')
        return rbin

    def op_lui(self, tokens):
        '''
        imm[31:12] rd opcode
        '''
        bin_opcode = None
        bin_rd = None
        rd = None
        imm = None

        try:
            bin_opcode = self.CONST.BOP_LUI
            rd = tokens['rd']
            bin_rd = self.get_bin_register(rd)
            imm = tokens['imm']
        except:
            cp.cprint_fail("Internal Error: LUI: could not parse" +
                           "tokens in " + str(tokens['lineno']))
            exit()

        bin_str = imm + bin_rd + bin_opcode
        assert(len(bin_str) == 32)

        tok_dict = {
            'opcode': bin_opcode,
            'rd': bin_rd,
            'imm': imm
        }
        return bin_str, tok_dict

    def op_auipc(self, tokens):
        '''
        imm[31:12] rd opcode
        '''
        bin_opcode = None
        bin_rd = None
        rd = None
        imm = None

        try:
            bin_opcode = self.CONST.BOP_AUIPC
            rd = tokens['rd']
            bin_rd = self.get_bin_register(rd)
            imm = tokens['imm']
        except:
            cp.cprint_fail("Internal Error: AUIPC: could not parse" +
                           "tokens in " + str(tokens['lineno']))
            exit()

        bin_str = imm + bin_rd + bin_opcode
        assert(len(bin_str) == 32)

        tok_dict = {
            'opcode': bin_opcode,
            'rd': bin_rd,
            'imm': imm
        }
        return bin_str, tok_dict

    def op_jal(self, tokens):
        '''
        imm[20] imm[10:1] imm[11] imm[19:12] rd opcode
        immediate is already shuffled in tokens
        '''
        bin_opcode = None
        bin_rd = None
        rd = None
        imm = None

        try:
            bin_opcode = self.CONST.BOP_JAL
            rd = tokens['rd']
            bin_rd = self.get_bin_register(rd)
            imm = tokens['imm']
        except:
            cp.cprint_fail("Internal Error: AUIPC: could not parse" +
                           "tokens in " + str(tokens['lineno']))
            exit()

        bin_str = imm + bin_rd + bin_opcode
        assert(len(bin_str) == 32)

        tok_dict = {
            'opcode': bin_opcode,
            'rd': bin_rd,
            'imm': imm
        }
        return bin_str, tok_dict

    def op_jalr(self, tokens):
        opcode = tokens['opcode']
        '''
        imm[11:0] rs1 funct3 rd opcode
        '''
        opcode = tokens['opcode']
        bin_opcode = None
        funct = None
        rs1 = None
        bin_rs1 = None
        bin_rd = None
        rd = None
        imm = None

        try:
            funct = self.CONST.FUNCT3_JALR[opcode]
            bin_opcode = self.CONST.BOP_JALR
            rs1 = tokens['rs1']
            bin_rs1 = self.get_bin_register(rs1)
            rd = tokens['rd']
            bin_rd = self.get_bin_register(rd)
            imm = tokens['imm']
        except:
            cp.cprint_fail("Internal Error: JALR: could not parse" +
                           "tokens in " + str(tokens['lineno']))
            exit()

        bin_str = imm + bin_rs1 + funct + bin_rd + bin_opcode
        assert(len(bin_str) == 32)

        if imm[-2:] != '00':
            cp.cprint_warn_32("32_Warning:" + str(tokens['lineno']) +
                              ": Missaligned address." +
                              " Address should be 4 bytes aligned.")

        tok_dict = {
            'opcode': bin_opcode,
            'funct': funct,
            'rs1': bin_rs1,
            'rd': bin_rd,
            'imm': imm
        }
        return bin_str, tok_dict

    def op_branch(self, tokens):
        '''
        imm[4:3] rs2 rs1 imm[2:0] funct3 opcode
        immediates returned in tokens as touple (imm_4_3, imm_2_0)
        '''
        opcode = tokens['opcode']
        imm_4_3 = None
        imm_2_0 = None
        funct3 = None
        rs1 = None
        rs2 = None
        bin_rs1 = None
        bin_rs2 = None
        try:
            funct3 = self.CONST.FUNCT3_JPBR[opcode]
            bin_opcode = self.CONST.BOP_JPBR
            rs1 = tokens['rs1']
            bin_rs1 = self.get_bin_register(rs1)
            rs2 = tokens['rs2']
            bin_rs2 = self.get_bin_register(rs2)
            imm_4_3, imm_2_0 = tokens['imm']
        except:
            cp.cprint_fail("Internal Error: BRANCH: could not parse" +
                           " tokens in " + str(tokens['lineno']))
            exit()

        bin_str = imm_4_3 + bin_rs2 + bin_rs1 + funct3
        bin_str += imm_2_0 + bin_opcode
        assert(len(bin_str) == 16)
        tok_dict = {
            'opcode': bin_opcode,
            'funct': funct3,
            'rs1': bin_rs1,
            'rs2': bin_rs2,
            'imm_4_3': imm_4_3,
            'imm_2_0': imm_2_0
        }

        return bin_str, tok_dict

    def op_load(self, tokens):
        opcode = tokens['opcode']
        '''
        imm[11:0] rs1 funct3 rd opcode
        '''
        opcode = tokens['opcode']
        bin_opcode = None
        funct3 = None
        rs1 = None
        bin_rs1 = None
        bin_rd = None
        rd = None
        imm = None

        try:
            funct3 = self.CONST.FUNCT3_LOAD[opcode]
            bin_opcode = self.CONST.BOP_LOAD
            rs1 = tokens['rs1']
            bin_rs1 = self.get_bin_register(rs1)
            rd = tokens['rd']
            bin_rd = self.get_bin_register(rd)
            imm = tokens['imm']
        except:
            cp.cprint_fail("Internal Error: LOAD: could not parse" +
                           "tokens in " + str(tokens['lineno']))
            exit()

        bin_str = imm + bin_rs1 + funct3 + bin_rd + bin_opcode
        assert(len(bin_str) == 32)

        if imm[-2:] != '00':
            cp.cprint_warn_32("32_Warning:" + str(tokens['lineno']) +
                              ": Missaligned address." +
                              " Address should be 4 bytes aligned.")

        tok_dict = {
            'opcode': bin_opcode,
            'funct': funct3,
            'rs1': bin_rs1,
            'rd': bin_rd,
            'imm': imm
        }
        return bin_str, tok_dict

    def op_store(self, tokens):
        '''
        imm[11:5] rs2 rs1 funct3 imm[4:0] opcode
        immediates returned in tokens as touple (imm_11_5, imm_4_0)
        '''
        opcode = tokens['opcode']
        imm_11_5 = None
        imm_4_0 = None
        funct3 = None
        rs1 = None
        bin_rs1 = None
        bin_rs2 = None
        rs2 = None
        try:
            funct3 = self.CONST.FUNCT3_STORE[opcode]
            bin_opcode = self.CONST.BOP_STORE
            rs1 = tokens['rs1']
            bin_rs1 = self.get_bin_register(rs1)
            rs2 = tokens['rs2']
            bin_rs2 = self.get_bin_register(rs2)
            imm_11_5, imm_4_0 = tokens['imm']
        except:
            cp.cprint_fail("Internal Error: STORE: could not parse" +
                           " tokens in " + str(tokens['lineno']))
            exit()

        bin_str = imm_11_5 + bin_rs2 + bin_rs1 + funct3 + imm_4_0 + bin_opcode
        assert(len(bin_str) == 32)

        if imm_4_0[-2:] != '00':
            cp.cprint_warn_32("32_Warning:" + str(tokens['lineno']) +
                              ": Missaligned address." +
                              " Address should be 4 bytes aligned.")

        tok_dict = {
            'opcode': bin_opcode,
            'funct': funct3,
            'rs1': bin_rs1,
            'rs2': bin_rs2,
            'imm_11_5': imm_11_5,
            'imm_4_0': imm_4_0
        }

        return bin_str, tok_dict


    def op_system_u(self, tokens):
        '''
        imm[7:0] rd  funct3  opcode

        '''
        opcode = tokens['opcode']
        bin_opcode = None
        funct3 = None
        bin_rd = None
        rd = None
        imm = None

        try:
            funct3 = self.CONST.FUNCT3_SYSTEM[opcode]
            bin_opcode = self.CONST.BOP_SYSTEM
            rd = tokens['rd']
            bin_rd = self.get_bin_register(rd)
            imm = tokens['imm']
        except:
            cp.cprint_fail("Internal Error: SYSTEM_U: could not parse" +
                           "tokens in " + str(tokens['lineno']))
            exit()

        bin_str = imm  + bin_rd + funct3 + bin_opcode
        assert(len(bin_str) == 16)

        tok_dict = {
            'opcode': bin_opcode,
            'funct3': funct3,
            'rd': bin_rd,
            'imm': imm
        }
        return bin_str, tok_dict

    def op_arithi(self, tokens):
        '''
        imm[7:0] rd  funct3  opcode

        '''
        opcode = tokens['opcode']
        bin_opcode = None
        funct3 = None
        bin_rd = None
        rd = None
        imm = None

        try:
            funct3 = self.CONST.FUNCT3_ARITHI[opcode]
            bin_opcode = self.CONST.BOP_ARITHI
            rd = tokens['rd']
            bin_rd = self.get_bin_register(rd)
            imm = tokens['imm']
        except:
            cp.cprint_fail("Internal Error: ARITHI: could not parse" +
                           "tokens in " + str(tokens['lineno']))
            exit()

        bin_str = imm  + bin_rd + funct3 + bin_opcode
        assert(len(bin_str) == 16)

        tok_dict = {
            'opcode': bin_opcode,
            'funct3': funct3,
            'rd': bin_rd,
            'imm': imm
        }
        return bin_str, tok_dict

    def op_arith(self, tokens):
        '''
        NA[1:0]  rs2 rs1  rd funct3 opcode
        '''
        opcode = tokens['opcode']
        bin_opcode = None
        funct3 = None
        rs1 = None
        rs2 = None
        rd = None
        bin_rs1 = None
        bin_rs2 = None
        bin_rd = None

        try:
            funct3 = self.CONST.FUNCT3_ARITH[opcode]
            bin_opcode = self.CONST.BOP_ARITH
            rs1 = tokens['rs1']
            rs2 = tokens['rs2']
            rd = tokens['rd']
            bin_rs1 = self.get_bin_register(rs1)
            bin_rs2 = self.get_bin_register(rs2)
            bin_rd = self.get_bin_register(rd)
        except:
            cp.cprint_fail("Internal Error: ARITH: could not parse" +
                           "tokens in " + str(tokens['lineno']))
            exit()

        bin_str = '00' + bin_rs2 + bin_rs1 + funct3 + bin_rd + bin_opcode
        assert(len(bin_str) == 16)

        tok_dict = {
            'opcode': bin_opcode,
            'funct3': funct3,
            'rs1': bin_rs1,
            'rd': bin_rd,
            'rs2': bin_rs2
        }
        return bin_str, tok_dict

    def convert_to_binary(self, tokens):
        '''
        The driver function for converting tokens to machine code.
        Takes the tokens parsed by the lexer and returns the
        binary equivalent.

        Returns a touple (instr, dict),
        where instr is the binary string of the instruction
        and the dict is the tokens converted individually
        '''
        try:
            opcode = tokens['opcode']
        except KeyError:
            print("Internal Error: Key not found (opcode)")
            return None

        if opcode in self.CONST.INSTR_BOP_ARITHI:
            return self.op_arithi(tokens)
        elif opcode in self.CONST.INSTR_BOP_ARITH:
            return self.op_arith(tokens)
        elif opcode in self.CONST.INSTR_BOP_SYSTEM_U:
            return self.op_system_u(tokens)
        else:
            cp.cprint_fail("Error:" + str(tokens['lineno']) +
                           ": Opcode: '%s' not implemented" % opcode)
            return None

        print("Internal Error: Control should not reach here!")
        return None


mcg = MachineCodeGenerator()
