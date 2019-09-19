"""
    These genertor is for custom purpose in training
"""
import os
import argparse

from PIL import Image
from skimage import transform
import tensorflow as tf
import random as rn
import numpy as np

class ImageGenerator():
    def __init__(self, target_size, validation_split=None,rescale = 1/255.):
        self.target_size = target_size
        self.rescale = rescale
        self.validation_split = validation_split

    def flow_from_directory(self, directory, batch_size, subset=None, shuffle=True):
        self.class_indices = dict()
        i = 0
        images_amount = 0
        data_path = dict()
        self.batch_size = batch_size
        self.shuffle = shuffle
        for class_name in sorted(os.listdir(directory)):
            self.class_indices[class_name] = i
            i+=1
            class_path = os.path.join(directory, class_name)
            #print('OS: ', class_path)
            all_images = sorted(os.listdir(class_path))
            if self.validation_split is not None:
                images = all_images[:int(len(all_images)*(1-self.validation_split))] if subset == 'training' else all_images[int(len(all_images)*(1-self.validation_split)):]
            else:
                images = all_images
            for image in images:
                image_path = os.path.join(class_path, image)
                data_path[image_path] = i
                images_amount += 1
        print('Found {} images for {} classes\n'.format(images_amount, i))
        self.n = images_amount

        return self.make_generator(data_path)

        
    def load(self, filename):
        np_image = self.img_augmentation(filename)
        np_image = np.array(np_image).astype('float32')*self.rescale
        np_image = transform.resize(np_image, (self.target_size[0], self.target_size[1], 3))
        #np_image = np.expand_dims(np_image, axis=0)
        return np_image
    
    def img_augmentation(self, filename):
        """
            Update when we can do augumentation
        """
        return Image.open(filename)
    
    def make_generator(self, data_path):
        if self.shuffle:
            data = np.random.permutation(list(data_path.keys()))
        else:
            data = np.array(list(data_path.keys()))
        for step in range(data.shape[0] // self.batch_size):
            batch_data = data[step * self.batch_size:(step + 1) * self.batch_size]
            x = list()
            y = list()
            for image_path in batch_data:
                y.append(data_path[image_path])
                x.append(self.load(image_path))
            
            # Generator here
            yield [x, y], y

def main(rootdir):
    generator = ImageGenerator(target_size=(224, 224))
    data_generator = generator.flow_from_directory(rootdir, batch_size=32)
    print(generator.class_indices)
    print(data_generator)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-rd", "--rootdir", type=str, default='food4', help="Path to the directory")
    args = parser.parse_args()
    main(args.rootdir)