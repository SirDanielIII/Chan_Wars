import os
import pygame as pg


class Load(object):
    def __init__(self):
        self.menu_img = None
        self.choose_boss_img = None

    def load_all(self):
        self.menu_img = self.load_images_resize(os.getcwd() + "/resources/menus", (1600, 900))
        self.choose_boss_img = self.load_images_resize(os.getcwd() + "/resources/menus/choose_boss", (1600, 900))

    @staticmethod
    def load_audio_set(path_to_directory, extension):
        """
        Args:
            path_to_directory:string:
                Directory to audio files
            extension:string:
                File extension of audio files
        """
        audio_set = []
        for filename in os.listdir(path_to_directory):
            if filename.endswith(extension):
                path = os.path.join(path_to_directory, filename)
                audio_set.append(pg.mixer.Sound(path))
        return audio_set

    @staticmethod
    def load_images(path_to_directory):
        """
        Args:
            path_to_directory:string:
                Directory of images
        """
        image_list = []
        for filename in os.listdir(path_to_directory):
            if filename.endswith('.png') or filename.endswith('.jpg'):
                path = os.path.join(path_to_directory, filename)
                image_list.append(pg.image.load(path).convert())
        return image_list

    @staticmethod
    def load_images_alpha(path_to_directory):
        """
        Args:
            path_to_directory:string:
                Directory of images
        """
        image_list = []
        for filename in os.listdir(path_to_directory):
            if filename.endswith('.png'):
                path = os.path.join(path_to_directory, filename)
                image_list.append(pg.image.load(path).convert_alpha())
        return image_list

    @staticmethod
    def load_images_alpha_resize(path_to_directory, size):
        """
        Args:
            path_to_directory:string:
                Directory of images
            size::tuple:
                Desired new resolution
        """
        image_list = []
        for filename in os.listdir(path_to_directory):
            if filename.endswith('.png'):
                path = os.path.join(path_to_directory, filename)
                image_list.append(pg.transform.smoothscale(pg.image.load(path), size).convert_alpha())
        return image_list

    @staticmethod
    def load_images_resize(path_to_directory, size):
        """
        Args:
            path_to_directory:string:
                Directory of images
            size::tuple:
                Desired new resolution
        """
        image_list = []
        for filename in os.listdir(path_to_directory):
            if filename.endswith('.png'):
                path = os.path.join(path_to_directory, filename)
                image_list.append(pg.transform.smoothscale(pg.image.load(path), size).convert())
        return image_list

    @staticmethod
    def resize_images(images, size):
        """
        Args:
            images:list:
                List of images to be resized
            size:tuple:
                Resolution to resize image list to
        """
        lst = []
        for idx, i in enumerate(images):
            lst.append(pg.transform.smoothscale(i, size).convert_alpha())
        return lst
