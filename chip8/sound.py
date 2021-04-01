class Sound:
    """
    CHIP-8 Sound engine.
    The original CHIP-8 only has simple beeps, so, to emulate that, we use the default OS bell sound.
    May implement a more complete audio emulation down the road. The bell sound will suffice for now.
    """
    @staticmethod
    def beep():
        """
        Prints the bell character which triggers the default OS bell sound.
        """
        print("\x07")
