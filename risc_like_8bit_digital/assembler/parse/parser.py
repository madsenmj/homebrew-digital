#
# @author:Don Dennis
# 8-bit Modified: MJ Madsen
# parser.py
#
# Parser for a simple assembler for subset of 8-bit RISC

import ply.yacc as yacc
import sys
# This is required by design
from parse.tokenizer import tokens
from parse.tokenizer import reset_lineno
from parse.machinecodegen import mcg
from parse.cprint import cprint as cp
from parse.machinecodeconst import MachineCodeConst
from pprint import pprint

mcc = MachineCodeConst()
'''
Grammar
-------
program: statement

statement: OPCODE register COMMA register COMMA register NEWLINE
        | OPCODE register COMMA register COMMA IMM_I NEWLINE
        | OPCODE register COMMA IMM_I NEWLINE
        | OPCODE register COMMA register NEWLINE
        | OPCODE register COMMA register COMMA LABEL NEWLINE
        | OPCODE LABEL NEWLINE
        | OPCODE register NEWLINE
        | OPCODE register COMMA LABEL NEWLINE
        | NEWLINE

NOTE: We parse the porgram line by line Hence we don't
need to recursively define the program interms of statements
'''


def p_program_statement(p):
    'program : statement'
    p[0] = {
        'type': 'non_label',
        'tokens': p[1]
    }


def p_program_label(p):
    'program : LABEL COLUMN NEWLINE'
    dict = {
        'label': p[1],
        'lineno': p.lineno(1)
    }
    p[0] = {
        'type': 'label',
        'tokens': dict
    }


def p_statement_R(p):
    'statement : OPCODE register COMMA register COMMA register NEWLINE'
    if p[1] not in mcc.INSTR_TYPE_R:
        cp.cprint_fail("Error:" + str(p.lineno(1)) +
                       ": Incorrect opcode or arguments")
        raise SyntaxError
    p[0] = {
        'opcode': p[1],
        'rd': p[2],
        'rs1': p[4],
        'rs2': p[6],
        'lineno': p.lineno(1)
    }

def p_statement_C(p):
    'statement : OPCODE register COMMA register NEWLINE'
    if p[1] not in mcc.INSTR_TYPE_C:
        cp.cprint_fail("Error:" + str(p.lineno(1)) +
                       ": Incorrect opcode or arguments")
        raise SyntaxError
    p[0] = {
        'opcode': p[1],
        'rd': p[2],
        'rs1': p[4],
        'lineno': p.lineno(1)
    }


def p_statement_I_S_JALR(p):
    'statement : OPCODE register COMMA register COMMA IMMEDIATE NEWLINE'
    if (p[1] not in mcc.INSTR_TYPE_I) and (p[1] not in mcc.INSTR_TYPE_S) and (p[1] not in mcc.INSTR_TYPE_J3):
        cp.cprint_fail("Error:" + str(p.lineno(1)) +
                       ": Incorrect opcode or arguments")
        raise SyntaxError
    elif p[1] in mcc.INSTR_TYPE_I:
        ret, imm, msg = get_imm_I(p[6], p.lineno(6))
        if not ret:
            cp.cprint_fail("Error:" + str(p.lineno(6)) + ":" + msg)
            raise SyntaxError

        p[0] = {
            'opcode': p[1],
            'rd': p[2],
            'rs1': p[4],
            'imm': imm,
            'lineno': p.lineno(1)
        }
    elif p[1] in mcc.INSTR_TYPE_S:
        ret, imm, msg = get_imm_SB(p[6], p.lineno(6))
        if not ret:
            cp.cprint_fail("Error:" + str(p.lineno(1)) + ":" + msg)
            raise SyntaxError
        p[0] = {
            'opcode': p[1],
            'rs1': p[2],
            'rs2': p[4],
            'imm': imm,
            'lineno': p.lineno(1)
        }
    else:  # JALR
        ret, imm, msg = get_imm_I(p[6], p.lineno(6))
        if not ret:
            cp.cprint_fail("Error:" + str(p.lineno(1)) + ":" + msg)
            raise SyntaxError
        p[0] = {
            'opcode': p[1],
            'rs1': p[2],
            'rs2': p[4],
            'imm': imm,
            'lineno': p.lineno(1)
        }


def p_statement_U(p):
    'statement : OPCODE register COMMA IMMEDIATE NEWLINE'

    if (p[1] not in mcc.INSTR_TYPE_U) and (p[1] not in mcc.INSTR_TYPE_US):
        cp.cprint_fail("Error:" + str(p.lineno(1)) +
                       ": Incorrect opcode or arguments")
        raise SyntaxError
    else:  # U Type
        ret, imm, msg = get_imm_U(p[4], p.lineno(4))
        if not ret:
            cp.cprint_fail("Error:" + str(p.lineno(1)) + ":" + msg)
            raise SyntaxError
        p[0] = {
            'opcode': p[1],
            'rd': p[2],
            'imm': imm,
            'lineno': p.lineno(1)
        }


def p_statement_UJ_LABEL(p):
    'statement : OPCODE register COMMA LABEL NEWLINE'

    if (p[1] not in mcc.INSTR_TYPE_UJ):
        cp.cprint_fail("Error:" + str(p.lineno(1)) +
                       ": Incorrect opcode or arguments")
        raise SyntaxError
    else:  # UJ Type
        p[0] = {
            'opcode': p[1],
            'rd': p[2],
            'label': p[4],
            'lineno': p.lineno(1)
        }


def p_statement_B(p):
    'statement : OPCODE register COMMA register COMMA LABEL NEWLINE'
    # Branch
    if p[1] not in mcc.INSTR_TYPE_B:
        cp.cprint_fail("Error:" + str(p.lineno(1)) +
                       ": Incorrect opcode or arguments")
        raise SyntaxError
    p[0] = {
        'opcode': p[1],
        'rs1': p[2],
        'rs2': p[4],
        'label': p[6],
        'lineno': p.lineno(1)
    }

def p_statement_J1(p):
    'statement : OPCODE LABEL NEWLINE'
    if p[1] not in mcc.INSTR_TYPE_J1:
        cp.cprint_fail("Error:" + str(p.lineno(1)) +
                       ": Incorrect opcode or arguments")
        raise SyntaxError
    p[0] = {
        'opcode': p[1],
        'label': p[2],
        'lineno': p.lineno(1)
    }

def p_statement_J2(p):
    'statement : OPCODE register NEWLINE'
    if p[1] not in mcc.INSTR_TYPE_J2:
        cp.cprint_fail("Error:" + str(p.lineno(1)) +
                       ": Incorrect opcode or arguments")
        raise SyntaxError
    p[0] = {
        'opcode': p[1],
        'rd': p[2],
        'lineno': p.lineno(1)
    }

def p_register(p):
    'register : REGISTER'
    r = p[1]
    r = r[1:]
    r = int(r)
    if (r < 0) or (r > 31):
        cp.cprint_fail("Error:" + str(p.lineno(1)) +
                       ":Invalid register index.")
        raise SyntaxError
    p[0] = p[1]


def p_statement_none(p):
    'statement : NEWLINE'
    p[0] = None


def get_imm_I(imm5, lineno):
    try:
        imm5 = int(imm5)
    except:
        msg = "Invalid immediate specified."
        return False, imm5, msg
    '''
    The I type immediates occurs in system load instructions
    '''
    IMM_MAX = 0b01111
    IMM_MIN = -0b10000

    if (imm5 > IMM_MAX) or (imm5 < IMM_MIN):
        cp.cprint_warn("Warning:" + str(lineno) + ":" +
                       "Immediate is too big, will overflow.")
    # Conver to 2's complement binary
    imm2 = format(imm5 if imm5 >= 0 else (1 << 5) + imm5, '05b')
    imm2 = imm2[-5:]
    # Convert immediate back to base 10 from base 2
    # p[0] = int(imm2, 2)
    assert(len(imm2) == 5)
    return True, imm2, p_statement_none


def get_imm_U(imm8, lineno):
    try:
        imm8 = int(imm8)
    except:
        msg = "Invalid immediate specified."
        return False, imm8, msg
    '''
    The U type immediate occurs ARITHI, LI, AIPC, and J-type instructions.
    '''
    IMM_MAX = 0b01111111
    IMM_MIN = -0b10000000

    if (imm8 > IMM_MAX) or (imm8 < IMM_MIN):
        cp.cprint_warn("Warning:" + str(lineno) + ":" +
                       "Immediate is too big, will overflow.")
    # Conver to 2's complement binary
    imm2 = format(imm8 if imm8 >= 0 else (1 << 8) + imm8, '08b')
    imm2 = imm2[-8:]
    # Convert immediate back to base 10 from base 2
    # p[0] = int(imm2, 2)
    assert(len(imm2) == 8)
    return True, imm2, None


def get_imm_UJ(imm10, lineno):
    try:
        imm10 = int(imm10)
    except:
        msg = "Invalid immediate specified."
        return False, imm10, msg
    '''
    The UJ Type immediate encodes a 2 byte aligned address.
    Hence its last bit has to be zero. We do not encode this
    last bit in the instruction and the CPU assumes the last
    bit to be zero.
    The immediate is reshuffled and looks like the following.

    imm[20] imm[10:1] imm[11] imm[19:12]
    Note that imm[0] is not encoded.

    From the parsers point of view, we accept an (21 bit) immediate
    check if its a multiple of 2 (report and error)
    and then shuffle it as required
    '''
    # Effectively we are addressing 21 bits
    IMM_MAX = 0b011111111111111111110
    IMM_MIN = -0b100000000000000000000

    if (imm10 > IMM_MAX) or (imm10 < IMM_MIN):
        cp.cprint_warn("Warning:" + str(lineno) + ":" +
                       "Immediate is too big, will overflow.")
    # Conver to 2's complement binary
    imm2 = format(imm10 if imm10 >= 0 else (1 << 21) + imm10, '021b')
    if imm2[-1:] != '0':
        cp.cprint_warn("Warning:" + str(lineno) + ":" +
                       "Immediate not 2 bytes aligned. Last bit will" +
                       "be dropped.")
    imm2 = imm2[0:-1]
    assert(len(imm2) == 20)
    # Shuffling the immediate
    # imm[20] imm[10:1] imm[11] imm[19:12]
    # Indexing in reverse order
    # imm[20] in is imm2[0] = imm2[-20] of imm string
    shf_imm = imm2[0] + imm2[10:20] + imm2[9] + imm2[1:9]
    assert(len(shf_imm) == 20)
    return True, shf_imm, None


def get_imm_SB(imm5, lineno):
    try:
        imm5 = int(imm5)
    except:
        msg = "Invalid immediate specified."
        return False, imm5, msg
    '''
    The S type and B type encodes instructions SB.

    The immediate is split into two parts - one part
    holding bits [15:16] in the immediate ordering(MSB-LSB from left to right)
    and the other part holding bits [5:6].
    We split the immediate into two portions hence.
    '''
    IMM_MAX = 0b01111
    IMM_MIN = -0b10000

    if (imm5 > IMM_MAX) or (imm5 < IMM_MIN):
        cp.cprint_warn("Warning:" + str(lineno) + ":" +
                       " Immediate is too big, will overflow.")
    # Convert to 2's complement binary
    imm2 = format(imm5 if imm5 >= 0 else (1 << 5) + imm5, '05b')
    imm2 = imm2[0:5]
    # Convert immediate back to base 10 from base 2
    # p[0] = int(imm2, 2)
    assert(len(imm2) == 5)
    imm_15_16 = imm2[:2]
    imm_2_0 = imm2[2:]
    assert(len(imm_15_16) + len(imm_2_0) == 5)
    return True, (imm_15_16, imm_2_0), p_statement_none


'''
For this simple parser, I have not implemented error
recovery rules and I have decided to keep only the line
number for debugging errors.
'''


def p_error(p):
    lineno = ''
    if p:
        lineno = str(p.lineno)
        cp.cprint_fail("Error:" + lineno + ": Invalid or incomplete token" +
                       " found '" + str(p.value) + "'")
    else:
        cp.cprint_fail("Error: Invalid or incomplete token found " +
                       "Did you end with a newline?")


def encode_offset(ltokens, address, target):
    '''
    In instructions having label, this function calculates
    the value of the offset that has to be encoded inplace of the
    the label.
    It uses the current address of the instruction and the target address
    to calculate the difference and encode the offset in binary

    returns: immediate offset in binary
    '''
    # Offset address
    offset = target - address
    lineno = ltokens['lineno']
    if ltokens['opcode'] == mcc.INSTR_JAL:
        ret, imm, msg = get_imm_U(offset, lineno)
        if not ret:
            # Label translation should not raise errors,
            # Warnings make sense.
            cp.cprint_fail("Internal error:" +
                           str(tokens['lineno']) + ":" + msg)
            exit(1)
        result = {
            'opcode': ltokens['opcode'],
            'rd': ltokens['rd'],
            'imm': imm,
            'lineno': lineno
        }
    elif ltokens['opcode'] in mcc.INSTR_TYPE_J1:
        ret, imm, msg = get_imm_U(offset, lineno)
        if not ret:
            cp.cprint_fail("Internal error:" + str(lineno) + ":" + msg)
            exit(1)
        result = {
            'opcode': ltokens['opcode'],
            'imm': imm,
            'lineno': lineno
        }
    elif ltokens['opcode'] in mcc.INSTR_TYPE_B:
        ret, imm, msg = get_imm_SB(offset, lineno)
        if not ret:
            cp.cprint_fail("Internal error:" + str(lineno) + ":" + msg)
            exit(1)
        result = {
            'opcode': ltokens['opcode'],
            'rs1': ltokens['rs1'],
            'rs2': ltokens['rs2'],
            'imm': imm,
            'lineno': lineno
        }
    else:
        cp.cprint_fail("Error: " + str(lineno) + " : " +
                       "Label not supported in '" +
                       str(ltokens['opcode']) + "'")

    return result


parser = yacc.yacc()

'''
First pass of assembling:
Address and label resolution
'''


def parse_pass_one(fin, args):
    address = 0
    symbols_table = {}
    # Suppress instruction warnings
    prev_warn = cp.warn
    prev_warn8 = cp.warn8
    cp.warn = False
    cp.warn8 = False
    for line in fin:
        result = parser.parse(line)
        if result["tokens"] is None:
            continue

        if result['type'] == 'non_label':
            address += 1
            continue

        if not result['tokens']['label'] in symbols_table:
            symbols_table[result['tokens']['label']] = address
        else:
            cp.cprint_fail("Error: " + str(result['tokens']['lineno']) +
                           " : Redeclaration of label '" +
                           str(result['tokens']) + "'.")
            exit(1)
    # Restore warning state
    cp.warn = prev_warn
    cp.warn8 = prev_warn8
    if args['echo_symbols']:
        cp.cprint_msgb("Symbols and Addresses:")
        cp.cprint_msgb(str(symbols_table))
    return symbols_table


def parse_pass_two(fin, fout, symbols_table, args):
    fin.seek(0, 0)
    # Reset line number state
    reset_lineno()
    address = 0
    fout.write('v2.0 raw\n')
    for line in fin:
        result = parser.parse(line)
        if result["tokens"] is None:
            continue

        if result['type'] == 'label':
            continue

        instr = None
        result = result['tokens']
        if 'label' in result:
            if result['label'] not in symbols_table:
                cp.cprint_fail("Error: " + str(result['lineno']) +
                               " : Label used but never defined '" +
                               str(result['label']) + "'.")
                exit(1)
            result = encode_offset(
                result, address, symbols_table[result['label']])
        if result:
            instr, instr_dict = mcg.convert_to_binary(result)
        if not instr:
            continue

        # Use hex instead of binary
        if args['hex']:
            instr = '%04X' % int(instr, 2)
        # Echo to console
        if args['echo']:
            cp.cprint_msgb(str(result['lineno']) + " " + str(instr))
        if args['tokenize']:
            cp.cprint_msgb(str(result['lineno']))
            pprint(instr_dict)

        fout.write(instr + '\n')
        address += 1


def parse_input(infile, **kwargs):
    if kwargs['no_color']:
        cp.no_color = True
    if kwargs['no_8']:
        cp.warn8 = False
    fin = None
    try:
        fin = open(infile, 'r')
    except IOError:
        cp.cprint_fail("Error: File does not seem to exist or" +
                       " you do not have the required permissions.")
        return 1

    outfile = kwargs['outfile']
    fout = None
    try:
        fout = open(outfile, 'w')
    except IOError:
        cp.cprint_fail("Error: Could not create '" + outfile + "' for output")
        return 1

    # Pass 1: Address resolution of labels
    symbols_table = parse_pass_one(fin, kwargs)
    # Pass 2: Mapping instructions to binary coding
    parse_pass_two(fin, fout, symbols_table, kwargs)
    fout.close()
    fin.close()


def main():
    if len(sys.argv) <= 1:
        exit("Error: No file specified")
    fin = None
    try:
        fin = open(sys.argv[1], 'r')
    except IOError:
        cp.cprint_fail("File does not seem to exist or" +
                       " you do not have the required permissions.")
        return 1

    for line in fin:
        result = parser.parse(line)
        if result:
            print(result)


if __name__ == '__main__':
    main()
