# assembler.py - Hack assembler (Nand to Tetris, Capstone)
# Khushi, K = 77  ->  77 mod 3 = 2, so extra feature = warn on duplicate labels
# usage: python assembler.py Box.asm   (makes Box.hack)

import sys

# predefined symbols
symbols = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "SCREEN": 16384, "KBD": 24576,
}
for i in range(16):
    symbols["R" + str(i)] = i

comp_table = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "!D": "0001101",
    "!A": "0110001", "-D": "0001111", "-A": "0110011",
    "D+1": "0011111", "A+1": "0110111", "D-1": "0001110",
    "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
    "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
    "M": "1110000", "!M": "1110001", "-M": "1110011",
    "M+1": "1110111", "M-1": "1110010", "D+M": "1000010",
    "D-M": "1010011", "M-D": "1000111", "D&M": "1000000",
    "D|M": "1010101",
}

dest_table = {
    "": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111",
}

jump_table = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111",
}


def clean(line):
    # remove comment and spaces
    if "//" in line:
        line = line.split("//")[0]
    return line.replace(" ", "").replace("\t", "").strip()


def first_pass(lines):
    # find labels, they dont take a line number in the output
    rom = 0
    code = []
    for line in lines:
        line = clean(line)
        if line == "":
            continue
        if line.startswith("("):
            name = line[1:-1]
            if name in symbols:
                # extra feature for K = 77
                print("Warning: label " + name + " is written twice")
            else:
                symbols[name] = rom
        else:
            code.append(line)
            rom += 1
    return code


def a_instruction(line):
    value = line[1:]
    global next_var
    if value.isdigit():
        n = int(value)
    else:
        if value not in symbols:
            symbols[value] = next_var
            next_var += 1
        n = symbols[value]
    return format(n, "016b")


def c_instruction(line):
    dest = ""
    jump = ""
    comp = line
    if "=" in line:
        dest, comp = line.split("=")
    if ";" in comp:
        comp, jump = comp.split(";")
    return "111" + comp_table[comp] + dest_table[dest] + jump_table[jump]


def second_pass(code):
    out = []
    for line in code:
        if line.startswith("@"):
            out.append(a_instruction(line))
        else:
            out.append(c_instruction(line))
    return out


next_var = 16

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python assembler.py File.asm")
        sys.exit()
    infile = sys.argv[1]
    f = open(infile)
    lines = f.readlines()
    f.close()

    code = first_pass(lines)
    binary = second_pass(code)

    outfile = infile.replace(".asm", ".hack")
    f = open(outfile, "w")
    for b in binary:
        f.write(b + "\n")
    f.close()
    print("done, wrote " + outfile)
