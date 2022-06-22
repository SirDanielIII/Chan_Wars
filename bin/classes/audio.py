import random

import pygame as pg


class Audio(object):
    def __init__(self):
        """
        Make sure to have this at the beginning of your Pygame program:
            pg.init()
            pg.mixer.pre_init(48000, -16, 2, 256)
            pg.mixer.set_num_channels(20)
        This ensures any audio playback isn't heavily delayed, and sets 20 audio channels for you to use
        """
        # Channels
        self.music_channels = [pg.mixer.Channel(i) for i in range(4)]  # Channels from 0 to 3
        self.sfx_channels = [pg.mixer.Channel(i) for i in range(4, 21)]  # Channels from 4 to 20
        # Toggles
        self.enable_music = True
        self.enable_sfx = True
        self.update_song = True
        # Volume
        self.vol_music = 1.0
        self.vol_sfx = 1.0
        # Music Handling
        self.song = None
        self.music_channel = 0

    def dj(self, song, music_c, fade_channel, ms, update, sfx_c, sfx, overlap="unused"):
        """ Handles music activation, switching, and fading.
        Args:
            song:pygame.mixer.Sound():
                Specific song to potentially play (can be null if not needed)
            music_c:int:
                Specifies a specific Pygame Channel to play a specific song from Music channel list
            fade_channel::list[string, int]:
                Specifies a specific Pygame Channel to fade its audio out (from Music / SFX list)
            ms:int:
                Specifies how long the fadeout is in milliseconds
            update:bool:
                Changes global boolean to switch songs in play_sounds()
            sfx_c:mixer.channel:
                Specifies a Pygame Channel to play a specific sound effect from SFX channel list
            sfx:pygame.mixer.Sound:
                Specific sound effect to potentially play (can be null if not needed)
            overlap:string:
                Find unused SFX channel to play the sound effect. True by default.
        Notes:
            - This method is built to be called once - E.G. Button Click
            - If switching music, it is best to fade out the old music channel and play the new music on another channel
            - Have some sort of system outside this class to specify which music piece to put into this method
            - This method should also be used to play sound effects, and work very well with buttons, etc
        """
        # ------------------------------------------------------------------------------------------------------------------
        if update:
            self.song = song
            self.music_channel = music_c
            self.update_song = update  # Whether the current song updates or not

        if sfx is not None:
            if not self.sfx_channels[sfx_c].get_busy():
                self.sfx_channels[sfx_c].play(sfx)  # Play sound effect if given
            elif overlap == "unused":  # Find unused channel
                for i in self.sfx_channels[sfx_c + 1:]:
                    if not i.get_busy():  # Play sound effect in an unused channel if given one is busy
                        i.play(sfx)
                        break
            elif overlap == "override":  # Override current channel
                self.sfx_channels[sfx_c].play(sfx)

        try:
            if fade_channel[0] == "music":
                self.music_channels[fade_channel[1]].fadeout(ms)
            if fade_channel[0] == "sfx":
                self.sfx_channels[fade_channel[1]].fadeout(ms)
        except TypeError:
            pass
        # ------------------------------------------------------------------------------------------------------------------

    def play_songs(self):
        """ Switches songs when prompted; based off states, modes, and/or Rick Roll
        Notes:
            pg.mixer.channel.play(Sound, loops=0, maxtime=0, fade_ms=0)
        """
        # ------------------------------------------------------------------------------------------------------------------
        # Music
        try:
            if self.update_song:  # Boolean Activates to Change Song
                pg.mixer.Channel(self.music_channel).play(self.song, -1)
                self.update_song = False  # Reset Value To Prevent Looping
        except TypeError:
            pass
        # ------------------------------------------------------------------------------------------------------------------

    def set_volume(self):
        """Sets the volume of already declared pygame music mixer channels"""
        # ------------------------------------------------------------------------------------------------------------------
        # Music Channel and Audio Control
        for i in self.music_channels:
            if self.enable_music:
                i.set_volume(self.vol_music)
                i.unpause()
            else:  # Mute Music
                i.pause()
        # ------------------------------------------------------------------------------------------------------------------
        # Sound Effect Channels & Volume Control
        for i in self.sfx_channels:
            if self.enable_sfx:
                i.set_volume(self.vol_sfx)
            else:  # Mute Sound Effects - Pausing doesn't work b/c the audio bugs and stops
                i.set_volume(0)
        # ------------------------------------------------------------------------------------------------------------------

    def audio_mixer(self):
        """Parent audio function used to be called in a game loop"""
        self.set_volume()
        self.play_songs()

    def calculate_volume(self, vol_type, pos, min_range, bar_range):
        """
        Notes:
            Takes in the pos, sets it to a certain range by subtracting min_range. To normalize it to a range of 0-100,
            we divide the number by the slider bar's range, giving us a percentage value that we divide again by 100 to get a usable number
            to set the pygame audio channel volume with.

            volume = ((position - minimum range) / bar_range) / 100
        """
        if vol_type == "MUSIC":
            self.vol_music = round(((pos - min_range) / bar_range), 3)
        elif vol_type == "SFX":
            self.vol_sfx = round(((pos - min_range) / bar_range), 3)

    @staticmethod
    def random_sound_lst(lst):
        return lst[random.randint(0, len(lst) - 1)]

    @staticmethod
    def fade_out_mixer(time):
        """
        Method that can be called without defining the Audio class that fades out all sounds in the Pygame program
        """
        pg.mixer.fadeout(time)
