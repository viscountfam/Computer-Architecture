"""CPU functionality."""

import sys

LDI = 0b10000010
PRA = 0b01001000
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
DIV = 0b10100011
ADD = 0b10100000
SUB = 0b10100001
POP = 0b01000110
PUSH = 0b01000101
CALL = 0b01010000
RET = 0b00010001


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram =  [0] * 256
        self.pc = 0
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
            ADD: self.ADD,
            SUB: self.SUB,
            POP: self.POP,
            PUSH: self.PUSH,
            CALL: self.CALL,
            RET: self.RET
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
    def PRA(self):
        register_address = self.ram_read(self.pc + 1)
        print(self.reg[register_address])
        self.pc += 2
    def PRN(self):
        index = self.ram_read(self.pc+1)
        print(self.reg[self.ram[self.pc+1]])
        self.pc += 2
    def HLT(self):
        self.running = False
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
        print("RAM", self.ram)
        return_addr = self.pc+2
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = return_addr
        reg_num = self.ram[self.pc+1]
        subroutine_addr = self.reg[reg_num]
        self.pc = subroutine_addr

    def RET(self):
        self.pc = self.ram[self.reg[self.sp]]
        self.reg[self.sp] += 1

    def run(self):
        """Run the CPU."""
        # ir = self.ram_read(self.pc)
        self.running = True
        self.reg[self.sp] = 0xf4
        while self.running:
            # print("it's running again")
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
                
