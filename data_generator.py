"""
    These genertor is for custom purpose in training
"""
import os

class ImageGenerator():
    def __init__(self, target_size, rescale = 1/255.):
        self.directory = directory
        self.target_size = target_size
        self.rescale = rescale
    def flow_from_directory(self, directory, batch_size):
        self.class_indices = dict()
        for class_name in os.listdir(self.directory):
            self.class_indices['1'] = class_name
    


if __name__ == '__main__':
