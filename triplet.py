import cv2
import numpy as np
from numpy import dot
from numpy.linalg import norm

import scipy
import random
import os
from PIL import Image

from torchvision import transforms
import torch
import pickle
import time
import random
random.seed(0)


class TripletHierarchical():
    def __init__(self, dataset_path, depth=2):
        """
            dataset_path: path to the image dataset
        """
        self.dataset_path = dataset_path
        if depth != 2:
            print('Currently support 2')
        else:
            self.depth = depth
        self.hierarchy = self.make_hierarchy()

    def make_hierarchy(self):
        """
            output: dictionary of class
        """
        hierarchy = dict()
        for class_name in os.listdir(self.dataset_path):
            hierarchy[class_name] = 'alone'
            class_path = os.path.join(self.dataset_path, class_name)
            for sub_class in os.listdir(class_path):
                sub_class_path = os.path.join(class_path, sub_class)
                if os.path.isdir(sub_class_path):
                    hierarchy[sub_class] = class_name
                    hierarchy[class_name] = 'parent'
                else:
                    break

        return hierarchy

    def triplet_sampler(self, output_path, num_query_images, num_pos_images, num_neg_images=1, threshold=0.5):
        """
        Perform Triplet Sampling.

        Args:
            directory_path: directory of Tiny ImageNet dataset
            output_path: directory to save `triplets.txt`
            num_neg_images: number of Negative images per Query image
            num_pos_images: number of Positive images per Query image
            num_query_images: number of Query image

        Returns:
            No return value, triplets will be saved on disk.
        """
        sampling = dict()
        for child, parent in self.hierarchy.items():
            if parent != 'parent':
                # Make triplet for highest class, no positive different class

                if parent == 'alone':
                    child_path = os.path.join(self.dataset_path, child)
                else:
                    child_path = os.path.join(self.dataset_path, parent, child)

                print('Child: {} ==> {}'.format(child, child_path))
                other_class = [
                    class_name for class_name in self.hierarchy.keys()
                    if (class_name != child and self.hierarchy[class_name] != 'parent')]
                # print(other_class)
                # Get a list of random query image
                if len(os.listdir(child_path)) < num_query_images:
                    query_imgs = os.listdir(child_path)
                else:
                    query_imgs = random.sample(
                        os.listdir(child_path), num_query_images)
                # print(child_path)
                query_imgs = [os.path.join(child_path, query)
                              for query in query_imgs]
                # print(child_path)
                for query in query_imgs:
                    # print(child_path)
                    pairs = list()
                    for i in range(num_pos_images):
                        positive = random.choice(os.listdir(child_path))
                        negative_class = random.choice(other_class)
                        if self.hierarchy[negative_class] != 'alone':
                            negative_class = os.path.join(
                                self.hierarchy[negative_class], negative_class)
                        negative = random.choice(os.listdir(
                            os.path.join(self.dataset_path, negative_class)))
                        pairs.append([os.path.join(child_path, positive), os.path.join(
                            self.dataset_path, negative_class, negative)])

                    sampling[query] = pairs

        triplets = list()
        for k, v in sampling.items():
            for pair in v:
                triplets.append(k+',')
                triplets.append(pair[0]+',')
                triplets.append(pair[1]+'\n')

        print("==> Sampling Done ... Now Writing ...")
        f = open(os.path.join(output_path), 'w')
        f.write("".join(triplets))
        f.close()
        print('Finished\n')


if __name__ == '__main__':
    gen = TripletHierarchical('../san_pham_new')
    # print(gen.hierarchy)
    gen.triplet_sampler('san_pham.txt', 100, 3)
