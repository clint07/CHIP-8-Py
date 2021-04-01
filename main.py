import logging.config
from tkinter import Tk
from tkinter.filedialog import askopenfilename

import pygame

from chip8.chip8 import Chip8
from chip8.constants import Constants
from chip8.display import Display
from chip8.sound import Sound

logger = logging.getLogger()


def main():
    # Instantiate the CHIP-8 and load a ROM into memory.
    logger.debug("Initializing CHIP-8.")
    chip8: Chip8 = Chip8()
    rom: str = open_file()
    chip8.load_file(rom)

    # Game clock that ensure the game runs at 60 FPS
    # CHIP-8 typically runs at 60 FPS, but there's nothing preventing it from running at a faster FPS.
    # Unlike CHIP-8, systems such as the NES need to run at a specific FPS or else the timing instructions will be off.
    clock: pygame.time.Clock = pygame.time.Clock()

    # WIP
    # Pygame will help display the CHIP-8 output and handle key press events.
    logger.debug("Initializing display.")
    pygame.init()
    display: Display = Display()

    # CHIP-8 sound engine.
    logger.debug("Initializing sound.")
    sound: Sound = Sound()

    logger.debug("Starting program.")
    while True:
        # Keeps CHIP-8 running at 60 FPS.
        clock.tick(Constants.fps)

        # Emulates a CHIP-8 operation cycle.
        chip8.cycle()

        # Redraw display if draw flag is set to true:
        if chip8.draw_flag:
            display.draw(chip8.display)
            # Don't forget to set the draw flag back to false!
            chip8.draw_flag = False

        # Beep if the sound timer is greater than zero.
        if chip8.sound_timer > 0:
            sound.beep()

        # Quit game if the delete key is pressed.
        if pygame.K_DELETE in pygame.event.get():
            break

    # Don't forget to properly destroy any windows created.
    pygame.quit()


def open_file() -> str:
    """
    Open file using the default OS file dialog through Tk.
    """
    root: Tk = Tk()
    root.withdraw()
    rom: str = askopenfilename(title=Constants.ask_open_filename_dialog)
    root.destroy()

    logger.debug(f"ROM: {rom}")
    return rom


if __name__ == "__main__":
    main()
