import unittest

from chip8.chip8 import Chip8


class TestChip8(unittest.TestCase):
    def test_ret(self):
        """
        Instruction 00EE: Return from a subroutine.
        The CPU sets the program counter to the address at the top of the stack,
        then subtracts 1 from the stack pointer.
        """
        chip8 = Chip8()

        chip8.program_counter = 0xFF
        chip8.stack[chip8.stack_pointer] = 512
        chip8.stack_pointer += 1

        chip8.ret()

        self.assertEqual(chip8.program_counter, 514)
        self.assertEqual(chip8.stack_pointer, 0)

    def test_jump(self):
        """
        Instruction 1nnn: Jump to location nnn.
        The CPU sets the program counter to nnn.
        :param self:
        :return:
        """
        chip8 = Chip8()
        chip8.jump(512)

        self.assertEqual(chip8.program_counter, 512)

    def test_call(self):
        """
        Instruction 2nnn: Call subroutine at nnn.
        The CPU increments the stack pointer, then puts the current PC on the top of the stack.
        The PC is then set to nnn.
        :param self:
        :return:
        """
        chip8 = Chip8()
        chip8.PC = 512

        chip8.call(777)

        self.assertEqual(chip8.stack_pointer, 1)
        self.assertEqual(chip8.stack[0], 512)
        self.assertEqual(chip8.program_counter, 777)

    def test_skip_if(self):
        """
        Instruction 3xkk: Skip next instruction if Vx = kk.
        The CPU compares register Vx to kk, and if they are equal,
        increments the program counter by 2.
        """
        chip8 = Chip8()
        chip8.registers[0x0] = 7

        chip8.skip_if(0x0, 7)
        self.assertEqual(chip8.program_counter, 516)

        chip8.skip_if(0x0, 9)
        self.assertEqual(chip8.program_counter, 518)
