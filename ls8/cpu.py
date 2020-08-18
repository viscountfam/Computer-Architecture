"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.register = [0] * 8
        self.ram =  [0] * 256
        self.pc = 0

    def ram_read(self, address):
       return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        if len(sys.argv) < 2:
          program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
            ] 
          for instruction in program:
                self.ram[address] = instruction
                address += 1
        elif len(sys.argv) == 2:
            filename = sys.argv[1]
            with open(filename) as f:
                address = 0
                for line in f:
                    if lin[0] != "#" or line[0] != "":
                        line = line.split("#")
                        try:
                            v = int(line[0], 2)
                        except ValueError:
                            continue
                        self.ram[address] = v
                        address += 1
        else:
            print("Only one ls8 program can be loaded")
            sys.exit("too many files present")



            
        


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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

    def run(self):
        """Run the CPU."""
        running = True
        # ir = self.ram_read(self.pc)
        # print("IR", bin(ir))
        while running:
            ir = self.ram_read(self.pc)
            if ir == 0b10000010:
                # print("self.ram", self.ram)
                # register_address = self.ram_read(self.pc + 1)
                # print("register address", self.ram_read(self.pc + 1))
                # print("self.register", self.register)
                # print("self.pc", self.pc)
                self.register[self.ram_read(self.pc + 1)] = self.ram_read(self.pc + 2)
                self.pc += 3
            elif ir == 0b01000111: 
                register_address = self.ram_read(self.pc + 1)
                print(self.register[register_address])
                self.pc += 2
            elif ir == 0b10100010:
                self.register[self.ram_read(self.pc + 1)] = self.ram_read(self.pc + 2) * self.ram_read(self.pc + 3)
                self.pc += 4
            elif ir == 0b00000001:
                running = False
                
