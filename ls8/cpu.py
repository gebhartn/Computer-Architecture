"""CPU functionality."""

import sys


# Instructions
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [None] * 8
        self.ram = [None] * 256
        self.dispatch = {}
        self.dispatch[LDI] = self.handle_ldi
        self.dispatch[PRN] = self.handle_prn
        self.dispatch[HLT] = self.handle_hlt
        self.dispatch[MUL] = self.handle_mul
        self.pc = 0

    def handle_ldi(self):
        """
        Read value
        """
        self.reg[self.ram_read(self.pc + 1)] \
            = self.ram_read(self.pc + 2)

        self.pc += 3

    def handle_prn(self):
        """
        Print
        """
        print(self.reg[self.ram_read(self.pc + 1)])
        self.pc += 2

    def handle_hlt(self):
        """
        Halt process
        """
        sys.exit(1)

    def handle_mul(self):
        """
        Multiply
        """
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.alu('MUL', reg_a, reg_b)
        self.pc += 3

    def ram_read(self, address):
        """
        Read from memory
        """
        return self.ram[address]

    def write_ram(self, address, value):
        """
        Write to memory
        """
        self.ram[address] = value

    def load(self, file):
        """
        Load a file into memory
        """
        try:
            address = 0
            with open(file) as incoming:
                for line in incoming:
                    split = line.split('#')
                    value = split[0].strip()

                    if value != '':
                        # convert to base 2 integer
                        num = int(value, 2)
                        self.ram[address] = num
                        address += 1
                    else:
                        continue
        except FileNotFoundError:
            print("File not found")
            sys.exit(1)

    def alu(self, operation, reg_a, reg_b):
        """
        ALU operations.
        """

        if operation == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        if operation == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state.
        You might want to call this from run()
        if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self, file):
        """Run the CPU."""

        self.load(file)

        while True:
            read = self.ram_read(self.pc)

            if read in self.dispatch:
                self.dispatch[read]()
            else:
                raise Exception('You have fucked up')

            # # Terminate on halt condition, non-zero exit code
            # if read is HLT:
            #     sys.exit(1)

            # # Fetch value at subsequent address
            # elif read is LDI:
            #     self.reg[self.ram_read(self.pc + 1)] \
            #         = self.ram_read(self.pc + 2)

            #     self.pc += 3

            # # Multiply
            # elif read is MUL:
            #     reg_a = self.ram_read(self.pc + 1)
            #     reg_b = self.ram_read(self.pc + 2)
            #     self.alu('MUL', reg_a, reg_b)
            #     self.pc += 3

            # # Print condition
            # elif read is PRN:
            #     print(self.reg[self.ram_read(self.pc + 1)])
            #     self.pc += 2

            # # We dun fucked up
            # else:
            #     raise Exception('Error: Unknown command!')


if len(sys.argv) == 2:
    FILE = sys.argv[1]

    CPU = CPU()
    CPU.run(FILE)
else:
    sys.exit(1)
