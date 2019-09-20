from PIL import Image
import argparse
import os
import time

def convert_png_2_jpg(imgdir):
    for img_path in os.listdir(imgdir):
        #print(img_path.split('.')[-1].lower())
        if img_path.split('.')[-1].lower() == 'png':
            img_path = os.path.join(imgdir, img_path)
            im = Image.open(img_path)
            rgb_im = im.convert('RGB')
            rgb_im.save('.'.join(img_path.split('.')[:-1])+'.jpg')
            os.remove(img_path)

            print('Convert: ', img_path, ' to ', '.'.join(img_path.split('.')[:-1])+'.jpg')

def remove_non_img(imgdir):
    for img_path in os.listdir(imgdir):
        if img_path.split('.')[-1].lower() not in ['png', 'jpg', 'jpeg']:
            img_path = os.path.join(imgdir, img_path)
            os.remove(img_path)
            print('Remove: ', img_path)

def main(rootdir):
    print("Analyzing {}".format(rootdir))
    for imgdir in os.listdir(rootdir):
        imgdir = os.path.join(rootdir, imgdir)
        convert_png_2_jpg(imgdir)
        remove_non_img(imgdir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-rd", "--rootdir", type=str, default='food_data', help="Path to the save directory")
    args = parser.parse_args()
    main(args.rootdir)
