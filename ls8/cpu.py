"""CPU functionality."""

import sys
LD = 0b10000011
LDI = 0b10000010
PRA = 0b01001000
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
DIV = 0b10100011
ADD = 0b10100000
MOD = 0b10100100
SUB = 0b10100001
POP = 0b01000110
PUSH = 0b01000101
CALL = 0b01010000
RET = 0b00010001
NOT = 0b011001001
OR = 0b10101010
SHL = 0b10101100
SHR = 0b10101101
XOR = 0b10101011
ST = 0b10100001
CMP = 0b10100111
DEC = 0b01100110
INC = 0b01100101
JEQ = 0b01010101
JGE = 0b01011010
JGT = 0b01010111
JLE = 0b01011001
JLT =0b01011000
JMP = 0b01010100
JNE = 0b01010110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram =  [0] * 256
        self.pc = 0
        self.E = 0
        self.L = 0
        self.G = 0
        # self.sp = 244
        self.running = False
        self.sp = 7
        self.bt = {
            LDI: self.LDI,
            PRA: self.PRA,
            PRN: self.PRN,
            HLT: self.HLT,
            MUL: self.MUL,
            DIV: self.DIV,
            MOD: self.MOD,
            ADD: self.ADD,
            SUB: self.SUB,
            POP: self.POP,
            PUSH: self.PUSH,
            CALL: self.CALL,
            RET: self.RET,
            LD: self.LD,
            NOT: self.NOT,
            OR: self.OR,
            SHR: self.SHR,
            SHL: self.SHL,
            XOR: self.XOR,
            ST: self.ST,
            CMP: self.CMP,
            DEC: self.DEC,
            INC: self.INC,
            JEQ: self.JEQ,
            JGE: self.JGE,
            JGT: self.JGT,
            JLE: self.JLE,
            JLT: self.JLT,
            JMP: self.JMP,
            JNE: self.JNE,
        }

    def ram_read(self, address):
       return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self, file_name):
        """Load a program into memory."""

        address = 0

        with open(f"examples/{file_name}") as f:
            for line in f:
                line = line.split("#")
                line = line[0].strip()
                # if line:
                #     self.ram[address] = int(line, 2)
                if line == "":
                    continue
                self.ram_write(address, int(line,2))
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == "MOD":
            self.reg[reg_a] %= self.reg[reg_b]
        elif op == "OR":
            self.reg[reg_a] |= self.reg[reg_b]
        elif op == "SHR":
            self.reg[reg_a] >>= self.reg[reg_b]
        elif op == "SHL":
            self.reg[reg_a] <<= self.reg[reg_b]
        elif op == "XOR":
            self.reg[reg_a] ^= self.reg[reg_b]
        elif op == "NOT":
            self.reg[reg_a] = ~self.reg[reg_a]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.E += 1
                self.L = 0
                self.G = 0
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.E = 0
                self.L += 1
                self.G = 0 
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.E = 0
                self.L = 0
                self.G += 1
        elif op == "DEC":
            self.reg[reg_a] -= 1
        elif op == "INC":
            self.reg[reg_a] += 1

        else:
            raise Exception("Unsupported ALU operation")


    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    def LDI(self):
        self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.pc + 2)
        self.pc += 3
    def LD(self):
        reg_A = self.ram_read(self.pc + 1)
        reg_B = self.ram_read(self.pc + 2)
        self.reg[reg_A] = self.reg[reg_B]
        self.pc += 3
    def PRA(self):
        register_address = self.ram_read(self.pc + 1)
        print(self.reg[register_address])
        self.pc += 2
    def PRN(self):
        index = self.ram_read(self.pc+1)
        print(self.reg[self.ram[self.pc+1]])
        self.pc += 2
    def ST(self):
        reg_A = self.ram_read(self.pc + 1)
        reg_B = self.ram_read(self.pc + 2)
        self.reg[reg_A] = self.reg[reg_B]
    def HLT(self):
        self.running = False
    def DEC(self):
        reg_A = self.ram_read(self.pc + 1)
        self.alu("DEC", reg_A, None)
    def INC(self):
        reg_A = self.ram_read(self.pc + 1)
        self.alu("INC", reg_A, None)
    def CMP(self):
        reg_A = self.ram_read(self.pc + 1)
        reg_B = self.ram_read(self.pc + 2)
        self.alu("CMP", reg_A, reg_B)
        self.pc += 3
    def NOT(self):
        reg_A = self.ram_read(self.pc + 1)
        self.alu("NOT", reg_A, None)
    def OR(self):
        reg_A = self.ram_read(self.pc + 1)
        reg_B = self.ram_read(self.pc + 2)
        self.alu("OR", reg_A, reg_B)
        self.pc += 3
    def SHR(self):
        reg_A = self.ram_read(self.pc + 1)
        reg_B = self.ram_read(self.pc + 2)
        self.alu("SHR", reg_A, reg_B)
        self.pc += 3
    def SHL(self):
        reg_A = self.ram_read(self.pc + 1)
        reg_B = self.ram_read(self.pc + 2)
        self.alu("SHL", reg_A, reg_B)
        self.pc += 3
    def XOR(self):
        reg_A = self.ram_read(self.pc + 1)
        reg_B = self.ram_read(self.pc + 2)
        self.alu("XOR", reg_A, reg_B)
        self.pc += 3
    def DIV(self):
        reg_A = self.ram_read(self.pc + 1)
        reg_B = self.ram_read(self.pc + 2)
        self.alu("DIV", reg_A, reg_B)
        self.pc += 3
    def MUL(self):
        reg_A = self.ram_read(self.pc + 1)
        reg_B = self.ram_read(self.pc + 2)
        self.alu("MUL", reg_A, reg_B)
        self.pc += 3
    def MOD(self):
        reg_A = self.ram_read(self.pc + 1)
        reg_B = self.ram_read(self.pc + 2)
        self.alu("MOD", reg_A, reg_B)
        self.pc += 3
    def ADD(self):
        reg_A = self.ram_read(self.pc + 1)
        reg_B = self.ram_read(self.pc + 2)
        self.alu("ADD", reg_A, reg_B)
        self.pc += 3
    def SUB(self):
        reg_A = self.ram_read(self.pc + 1)
        reg_B = self.ram_read(self.pc + 2)
        self.alu("SUB", reg_A, reg_B)
        self.pc += 3
    def POP(self):
        reg_num = self.ram[self.pc+1]
        top = self.reg[self.sp]
        value = self.ram[top]
        self.reg[reg_num] = value
        self.pc += 2
        self.reg[self.sp] += 1
    def PUSH(self):
        self.reg[self.sp] -= 1
        reg_num = self.ram[self.pc+1]
        value = self.reg[reg_num]
        top = self.reg[self.sp]
        self.ram[top] = value
        self.pc += 2
    def CALL(self):
        return_addr = self.pc+2
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = return_addr
        reg_num = self.ram[self.pc+1]
        subroutine_addr = self.reg[reg_num]
        self.pc = subroutine_addr
    def JMP(self):
        reg_num = self.ram_read(self.pc + 1)
        addr = self.reg[reg_num]
        self.pc =addr
    def JEQ(self):
        if self.E == 1:
            self.JMP()
        else:
            self.pc += 2
    def JNE(self):
        if self.E == 0:
            self.JMP()
        else:
            self.pc += 2
    def JLT(self):
        if self.L == 1:
            self.JMP()
        else:
            self.pc += 2
    def JGT(self):
        if self.G == 1:
            self.JMP()
        else:
            self.pc += 2
    def JLE(self):
        if self.L == 1 or self.E == 1:
            self.JMP()
        else:
            self.pc += 2
    def JGE(self):
        if self.G == 1 or self.E == 1:
            self.JMP()
        else:
            self.pc += 2

    def RET(self):
        self.pc = self.ram[self.reg[self.sp]]
        self.reg[self.sp] += 1

    def run(self):
        """Run the CPU."""
        # ir = self.ram_read(self.pc)
        self.running = True
        self.reg[self.sp] = 0xf4
        while self.running:
            ir = self.ram_read(self.pc)
            self.bt[ir]()

            # if ir == 0b10000010: #LOAD
            #     self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.pc + 2)
            #     self.pc += 3
            # elif ir == 0b01000111: #PRINT
            #     register_address = self.ram_read(self.pc + 1)
            #     print(self.reg[register_address])
            #     self.pc += 2
            # elif ir == 0b10100010: #MULTIPLY
            #     # self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.pc + 2) * self.ram_read(self.pc + 3)
            #     # self.pc += 3
            #     reg_A = self.ram_read(self.pc + 1)
            #     reg_B = self.ram_read(self.pc + 2)
            #     self.alu("MUL", reg_A, reg_B)
            #     self.pc += 3
            # elif ir == 0b10100000: #ADDITION
            #     reg_A = self.ram_read(self.pc + 1)
            #     reg_B = self.ram_read(self.pc + 2)
            #     self.alu("ADD", reg_A, reg_B)
            #     self.pc += 3
            # elif ir == 0b01000110: #POP
            #     self.reg[self.ram_read(self.pc + 1)] = self.ram[self.sp]
            #     self.sp += 1
            #     self.pc += 2
            # elif ir == 0b01000101: #PUSH
            #     self.sp -= 1
            #     self.ram[self.sp] = self.reg[self.ram_read(self.pc + 1)]
            #     self.pc += 2
            # elif ir == 0b00000001:
            #     print("program finished")
            #     running = False
            # else:
            #     print("Invalid Command")
            #     running = False
                
