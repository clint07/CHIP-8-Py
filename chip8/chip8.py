import logging
from random import randint

import numpy as np

logger = logging.getLogger()


class Chip8:
    """
    CHIP-8 interpreter that runs CHIP-8 programs.
    Currently does not support Super CHIP-8
    """

    def __init__(self):
        # Program counter.
        # All CHIP-8 programs start at 0x200.
        # 0x000 to 0x0A0 is reserved for fonts.
        self.program_counter: int = 0x200
        # Stack pointer.
        # Used for subroutines and jumps.
        self.stack_pointer: int = 0
        # Address register or also known as I in CHIP-8.
        self.address_register: int = 0x000
        # 16 8-bit registers.
        # Registers 0 to 15/V0 to VE are general registers.
        # Register 16/VF is a flag register.
        self.registers: list = [0] * 16
        # 4096: ints of memory.
        self.memory: list = [0] * 4096
        # Stack.
        self.stack: list = [0] * 16
        # Delay timer.
        self.delay_timer: int = 0
        # Sound timer. Beeps if not zero.
        self.sound_timer: int = 0
        # Draw flag.
        # Flag set when screen needs to be redrawn.
        self.draw_flag: int = 0
        # Binary 32x64 display
        self.display = np.zeros((32, 64))

        self.load_font()

    def load_font(self):
        """
        All CHIP-8 programs have this default pixel font for 0 - F.
        Loaded into 0x000 to 0x200.
        """
        font: list = [0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
                      0x20, 0x60, 0x20, 0x20, 0x70,  # 1
                      0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
                      0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
                      0xA0, 0xA0, 0xF0, 0x20, 0x20,  # 4
                      0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
                      0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
                      0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
                      0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
                      0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
                      0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
                      0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
                      0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
                      0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
                      0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
                      0xF0, 0x80, 0xF0, 0x80, 0x80]   # F

        self.memory[:len(font)] = font

    def load_file(self, rom: str):
        """
        Open and Load CHIP-8 ROM into memory.

        :param rom:
            ROM filename path.
        """
        logger.debug(f"Loading {rom} into memory.")
        with open(rom, 'rb') as file:
            data = file.read()
            for index, val in enumerate(data):
                self.memory[self.program_counter + index] = int(val)

    def cycle(self):
        """
        Emulates a CPU cycle.
        Get instruction, execute, and decrement appropriate timers.
        """
        logger.debug("CHIP-8 cycle.")

        instruction = self.get_instruction()
        self.execute_instruction(instruction)

        if self.delay_timer > 0:
            self.delay_timer -= 1

        if self.sound_timer > 0:
            self.sound_timer -= 1

    def get_instruction(self) -> int:
        """
        TODO

        Get instruction from memory.
        :return:
            Assembly instruction
        """
        NotImplemented()
        return 0

    def execute_instruction(self, int):
        """
        TODO

        Execute instruction.

        :param int:
            Assembly instruction
        """
        NotImplemented()

    def clear(self):
        """
        Instruction 00E0: Clear the display.
        """
        logger.debug("Instruction 00E0: Clear the display.")

        # Zero out display
        self.display = np.zeros((32, 64))

        # Set draw flag
        self.draw_flag = True

        # Increment PC counter
        self.program_counter += 2

    def ret(self):
        """
        Instruction 00EE: Return from a subroutine.
        The CPU sets the program counter to the address at the top of the stack,
        then subtracts 1 from the stack pointer.
        """
        logger.debug("Instruction 00EE: Return from a subroutine.")

        self.stack_pointer -= 1
        # Decrement stack pointer and error if it's below 0.
        if self.stack_pointer < 0:
            logger.error(f"ret: stack pointer out of bound::self.stack_pointer.")
            quit()
    
        self.program_counter = self.stack[self.stack_pointer]
        self.program_counter += 2

    def jump(self, nnn: int):
        """
        Instruction 1nnn: Jump to location nnn.
        The CPU sets the program counter to nnn.

        :param nnn:
            Memory location
        """
        logger.debug(f"Instruction 1nnn: Jump to location:nnn.")
        
        # Set PC to nnn. Error if it accesses invalid memory.
        self.program_counter = nnn

        if self.program_counter > 4028:
            logger.error(f"jump: program counter out of bound::nnn.")
            quit()

    def call(self, nnn: int):
        """
        Instruction 2nnn: Call subroutine at nnn.
        The CPU increments the stack pointer, then puts the current PC on the top of the stack.
        The PC is then set to nnn.

        :param nnn:
            Memory location
        """
        logger.debug(f"Instruction 2nnn: Call subroutine at:nnn.")

        self.stack[self.stack_pointer] = self.program_counter

        # Set PC to nnn. Error if it accesses invalid memory.
        self.program_counter = nnn
        if self.program_counter > 4028:
            logger.error(f"call: program counter out of bound::nnn")

        # Increment stack pointer and error if it's above it's length
        self.stack_pointer += 1
        if self.stack_pointer > len(self.stack):
            logger.error(f"call: stack pointer out of bound::self.stack_pointer")

    def skip_if(self, vx: int, kk: int):
        """
        Instruction 3xkk: Skip next instruction if Vx = kk.
        The CPU compares register Vx to kk, and if they are equal,
        increments the program counter by 2.

        :param vx:
            Register index
        :param kk:
            Register index
        """
        logger.debug("Instruction 3xkk: Skip next instruction if Vx == kk.")
    
        if self.registers[vx] == kk:
            self.program_counter += 2
    
        self.program_counter += 2

    def skip_if_not(self, vx: int, kk: int):
        """
        Instruction 4xkk: Skip next instruction if Vx != kk.
        The CPU compares register Vx to kk, and if they are not equal,
        increments the program counter by 2.

        :param vx:
            Register index
        :param kk:
            Data
        """
        logger.debug("Instruction 4xkk: Skip next instruction if Vx != kk.")
    
        if self.registers[vx] != kk:
            self.program_counter += 2

        self.program_counter += 2

    def skip_if_xy(self, vx: int, vy: int):
        """
        Instruction 5xy0: Skip next instruction if Vx = Vy.
        The CPU compares register Vx to register Vy, and if they are equal,
        increments the program counter by 2.

        :param vx:
            Register index
        :param vy:
            Register index
        """
        logger.debug("Instruction 5xy0: Skip next isntruction if Vx = Vy.")
    
        if self.registers[vx] == self.registers[vy]:
            self.program_counter += 2
    
        self.program_counter += 2

    def load(self, vx: int, kk: int):
        """
        Instruction 6xkk: Set Vx = kk.
        The CPU puts the value kk into register Vx.

        :param vx:
            Register index
        :param kk:
            Data
        """
        logger.debug("Instruction 6xkk: Set Vx = kk.")

        self.registers[vx] = kk
        self.program_counter += 2

    def add(self, vx: int, kk: int):
        """
        Instruction 7xkk: Set Vx = Vx + kk.
        Adds the value kk to the value of register Vx, then stores the result in Vx.

        :param vx:
            Register index
        :param kk:
            Data
        """
        logger.debug("Instruction 7xkk: Set Vx = Vx + kk.")

        self.registers[vx] += kk
        self.program_counter += 2

    def load_xy(self, vx: int, vy: int):
        """
        Instruction 8xy0: Set Vx = Vy.
        Stores the value of register Vy in register Vx.

        :param vx:
            Register index
        :param vy:
            Register index
        """
        logger.debug("Instruction 8xy0: Set Vx = Vy.")

        self.registers[vx] = self.registers[vy]
        self.program_counter += 2

    def or_xy(self, vx: int, vy: int):
        """
        Instruction 8xy1: Set Vx = Vx OR Vy.
        Performs a bitwise OR on the values of Vx and Vy, then stores the result in Vx.
        A bitwise OR compares the corresponding bits from two values, and if either bit is 1,
        then the same bit in the result is also 1. Otherwise, it is 0.

        :param vx:
            Register index
        :param vy:
            Register index
        """
        logger.debug("Instruction 8xy1: Set Vx = Vx | Vy.")

        self.registers[vx] |= self.registers[vy]
        self.program_counter += 2

    def and_xy(self, vx: int, vy: int):
        """
        Instruction 8xy2: Set Vx = Vx AND Vy.
        Performs a bitwise AND on the values of Vx and Vy, then stores the result in Vx.
        A bitwise AND compares the corresponding bits from two values, and if both bits are 1,
        then the same bit in the result is also 1. Otherwise, it is 0.

        :param vx:
            Register index
        :param vy:
            Register index
        """
        logger.debug("Instruction 8xy2: Set Vx = Vx & Vy.")

        self.registers[vx] &= self.registers[vy]
        self.program_counter += 2

    def x_or_xy(self, vx: int, vy: int):
        """
        Instruction 8xy3: Set Vx = Vx XOR Vy.
        Performs a bitwise exclusive OR on the values of Vx and Vy, then stores the result in Vx.
        An exclusive OR compares the corresponding bits from two values,
        and if the bits are not both the same, then the corresponding bit in the result is set to 1.
        Otherwise, it is 0.

        :param vx:
            Register index
        :param vy:
            Register index
        """
        logger.debug("Instruction 8xy3: Set Vx = Vx ^ Vy.")

        self.registers[vx] ^= self.registers[vy]
        self.program_counter += 2

    def add_xy(self, vx: int, vy: int):
        """
        Instruction 8xy4: Set Vx = Vx + Vy, set VF = carry.
        The values of Vx and Vy are added together. If the result is greater than 8 bits (i.e., > 255,)
        VF is set to 1, otherwise 0. Only the lowest 8 bits of the result are kept, and stored in Vx.

        :param vx:
            Register index
        :param vy:
            Register index
        """
        logger.debug("Instruction 8xy4: Set Vx = Vx + Vy, set VF = carry.")

        num = self.registers[vx] + self.registers[vy]

        if num > 255:
            self.registers[0xF] = 1
        else:
            self.registers[0xF] = 0

        self.registers[vx] = num

        self.program_counter += 2

    def sub_xy(self, vx: int, vy: int):
        """
        Instruction 8xy5: Set Vx = Vx - Vy, set VF = NOT borrow.
        If Vx > Vy, then VF is set to 1, otherwise 0. Then Vy is subtracted from Vx,
        and the results stored in Vx.

        :param vx:
            Register index
        :param vy:
            Register index
        """
        logger.debug("Instruction 8xy5: Set Vx = Vx - Vy, set VF = NOT borrow.")

        if self.registers[vx] > self.registers[vy]:
            self.registers[0xF] = 1
        else:
            self.registers[0xF] = 0

        self.registers[vx] = self.registers[vx] - self.registers[vy]

        self.program_counter += 2

    def shift_right(self, vx: int):
        """
        Instruction 8xy6: Set Vx = Vx SHR 1.
        If the least-significant bit of Vx is 1, then VF is set to 1, otherwise 0.
        Then Vx is divided by 2.

        :param vx:
            Register index
        """
        logger.debug("Instruction 8xy6: Set Vx = Vx SHR 1.")

        self.registers[0xF] = self.registers[vx] & 0x1

        # Divide by 2
        self.registers[vx] = self.registers[vx] >> 1

        self.program_counter += 2

    def sub_yx(self, vx: int, vy: int):
        """
        Instruction 8xy7: Set Vx = Vy - Vx, set VF = NOT borrow.
        If Vy > Vx, then VF is set to 1, otherwise 0. Then Vx is subtracted from Vy,
        and the results stored in Vx.

        :param vx:
            Register index
        :param vy:
            Register index
        """
        logger.debug("Instruction 8xy7: Set Vx = Vy - Vx, set VF = NOT borrow.")

        if self.registers[vy] > self.registers[vx]:
            self.registers[0xF] = 1
        else:
            self.registers[0xF] = 0

        self.registers[vx] = self.registers[vy] - self.registers[vx]

        self.program_counter += 2

    def shift_left(self, vx: int):
        """
        Instruction 8xyE: Set Vx = Vx SHL 1.
        If the most-significant bit of Vx is 1, then VF is set to 1, otherwise to 0.
        Then Vx is multiplied by 2.

        :param vx:
            Register index
        """
        logger.debug("Instruction 8xyE: Set Vx = Vx SHL 1.")

        # Get the most significant bit in a: int
        self.registers[0xF] = (self.registers[vx] >> 7) & 0x1

        # Multiple by 2
        self.registers[vx] = self.registers[vx] << 1

        self.program_counter += 2

    def skip_if_not_xy(self, vx: int, vy: int):
        """
        Instruction 9xy0: Skip next instruction if Vx != Vy.
        The values of Vx and Vy are compared, and if they are not equal,
        the program counter is increased by 2.

        :param vx:
            Register index
        :param vy:
            Register index
        """
        logger.debug("Instruction 9xy0: Skip next instruction if Vx != Vy.")

        if self.registers[vx] != self.registers[vy]:
            self.program_counter += 2

        self.program_counter += 2

    def load_i(self, nnn: int):
        """
        Instruction Annn: Set I = nnn.
        The value of register I is set to nnn.

        :param nnn:
            Data
        """
        logger.debug("Instruction Annn: Set I = nnn.")

        self.address_register = nnn
        self.program_counter += 2

    def jump_v0(self, nnn: int):
        """
        Instruction Bnnn: Jump to location nnn + V0.
        The program counter is set to nnn plus the value of V0.

        :param nnn:
            Data
        """
        logger.debug("Instruction Bnnn: Jump to location nnn + V0.")
        self.program_counter = self.registers[0x0] + nnn

    def rand(self, vx: int, kk: int):
        """
        Instruction Cxkk: Set Vx = random: int AND kk.
        The CPU generates a random number from 0 to 255,
        which is then ANDed with the value kk. The results are stored in Vx.
        See instruction 8xy2 for more information on AND.

        :param vx:
            Register index
        :param kk:
            Data
        """
        logger.debug("Instruction Cxkk: Set Vx = random: int AND kk.")

        r = randint(0, 255)
        self.registers[vx] = kk & r
        self.program_counter += 2

    def draw(self, vx: int, vy: int, n: int):
        """
        TODO

        Instruction Dxyn: Display n-byte sprite starting at memory location I at (Vx, Vy),
        set VF = collision.

        The CPU reads n: ints from memory, starting at the address stored in I.
        These: ints are then displayed as sprites on screen at coordinates (Vx, Vy).
        Sprites are XORed onto the existing screen. If this causes any pixels to be erased,
        VF is set to 1, otherwise it is set to 0. If the sprite is positioned so part of it
        is outside the coordinates of the display, it wraps around to the opposite side of the screen.
        See instruction 8xy3 for more information on XOR, and section 2.4, Display,
        for more information on the Chip-8 screen and sprites.

        :param vx:
            Register index
        :param vy:
            Register index
        :param n:
            Integer
        """
        logger.debug("Instruction Dxyn: Display nbyte sprite starting at memory location I at (Vx, Vy), "
                     "set Vf = collusion.")

        NotImplemented()

        self.program_counter += 2

    def skip_if_key(self, vx: int):
        """
        TODO

        Instruction Ex9E: Skip next instruction if key with the value of Vx is pressed.
        Checks the keyboard, and if the key corresponding to the value of Vx is currently
        in the down position, PC is increased by 2.

        :param vx:
            Register index
        """
        logger.debug("Instruction Ex9E: Skip instruction if key with the value of Vx is pressed.")

        NotImplemented()

        self.program_counter += 2

    def skip_if_key_not(self, vx: int):
        """
        TODO

        Instruction ExA1: Skip next instruction if key with the value of Vx is not pressed.
        Checks the keyboard, and if the key corresponding to the value of Vx is currently
        in the up position, PC is increased by 2.

        :param vx:
            Register index
        """
        logger.debug("Instruction ExA1: Skip next instruction if key with the value of Vx is not pressed.")

        NotImplemented()

        self.program_counter += 2

    def load_xdt(self, vx: int):
        """
        Instruction Fx07: Set Vx = delay timer value.
        The value of DT is placed into Vx.

        :param vx:
            Register index
        """
        logger.debug("Instruction Fx07: Set Vx = delay timer value.")

        self.registers[vx] = self.delay_timer

        self.program_counter += 2

    def load_key(self, vx: int):
        """
        TODO

        Instruction Fx0A: Wait for a key press, store the value of the key in Vx.
        All execution stops until a key is pressed, then the value of that key is stored in Vx.

        :param vx:
            Register index
        """
        logger.debug("Instruction Fx0A: Wait for a key press, store the value of the key in Vx.")

        NotImplemented()

        self.program_counter += 2

    def load_dtx(self, vx: int):
        """
        Instruction Fx15: Set delay timer = Vx.
        DT is set equal to the value of Vx.

        :param vx:
            Register index
        """
        logger.debug("Instruction Fx15: Set delay timer = Vx.")

        self.delay_timer = self.registers[vx]
        self.program_counter += 2

    def load_stx(self, vx: int):
        """
        Instruction Fx18: Set sound timer = Vx.
        ST is set equal to the value of Vx.

        :param vx:
            Register index
        """
        logger.debug("Instruction Fx18: Set sounder timer = Vx.")

        self.stack_pointer = self.registers[vx]
        self.program_counter += 2

    def add_ix(self, vx: int):
        """
        Instruction Fx1E: Set I = I + Vx.
        The values of I and Vx are added, and the results are stored in I/address register.

        :param vx:
            Register index
        """
        logger.debug("Instruction Fx1E : Set I = I + Vx.")

        self.address_register = self.address_register + self.registers[vx]
        self.program_counter += 2

    def load_ix(self, vx: int):
        """
        Instruction Fx29: Set I = location of sprite for digit Vx.
        The value of I is set to the location for the hexadecimal sprite corresponding
        to the value of Vx. See section 2.4, Display, for more information on the Chip-8 hexadecimal font.

        :param vx:
            Register index
        """
        logger.debug("Instruction Fx29: Set I = location of sprite for digit Vx.")

        self.address_register = self.registers[vx] * 5
        self.program_counter += 2

    def load_bcd(self, vx: int):
        """
        Instruction Fx33: Store BCD representation of Vx in memory locations I, I+1, and I+2.
        The CPU takes the decimal value of Vx, and places the hundreds digit in memory
        at location in I, the tens digit at location I+1, and the ones digit at location I+2.

        :param vx:
            Register index
        """
        logger.debug("Instruction Fx33: Store BCD represention of Vx in memory locations I, I+1, I+2.")

        dec = self.registers[vx]

        for i in range(2, -1, -1):
            self.memory[self.address_register+i] = dec % 10
            dec /= 10

        self.program_counter += 2

    def save_v(self, vx: int):
        """
        TODO

        Instruction Fx55: Store registers V0 through Vx in memory starting at location I.
        The CPU copies the values of registers V0 through Vx into memory,
        starting at the address in I.

        :param vx:
            Register index
        """
        logger.debug("Instruction Fx55: Store registers V0 through Vx in memory starting at location I.")

        NotImplemented()
        self.program_counter += 2

    def load_v(self, vx: int):
        """
        TODO

        Instruction Fx65: Read registers V0 through Vx from memory starting at location I.
        The CPU reads values from memory starting at location I into registers V0 through Vx.

        :param vx:
            Register index
        """
        logger.debug("Instruction Fx65: Read registers V0 through Vx in memory starting at location I.")

        NotImplemented()
        self.program_counter += 2
