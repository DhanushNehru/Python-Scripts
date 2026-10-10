#!/usr/bin/env python3
from genericpath import isdir
import cv2
import os

def vconcat_resize(img_list, interpolation= cv2.INTER_CUBIC):
    w_min = min(img.shape[1] for img in img_list)
    im_list_resize = [cv2.resize(img,
                      (w_min, int(img.shape[0] * w_min / img.shape[1])),
                                interpolation=interpolation)
                      for img in img_list]
    return cv2.vconcat(im_list_resize)

def hconcat_resize(img_list, interpolation= cv2.INTER_CUBIC):
    h_min = min(img.shape[0] for img in img_list)
    im_list_resize = [cv2.resize(img,
                       (int(img.shape[1] * h_min / img.shape[0]),
                        h_min), interpolation
                                 = interpolation) 
                      for img in img_list]
    return cv2.hconcat(im_list_resize)

imgpath1 = input("Enter 1st image path:")
imgpath2 = input("Enter 2nd image path:")
if os.path.exists(imgpath1) and os.path.exists(imgpath2):
    if os.path.isdir(imgpath1):
        print("[ERROR] 1st image path is a directory!")
        exit(1)
    if os.path.isdir(imgpath2):
        print("[ERROR] 2nd image path is a directory!")
        exit(1)
    img1 = cv2.imread(imgpath1)
    img2 = cv2.imread(imgpath2)
    merge_method = input("Merge [V]erically or [H]orizontally? ")
    if merge_method == "H" or merge_method == "h":
        im_concat = hconcat_resize([img1, img2])
        cv2.imwrite("horizontal_concatenated.jpg", im_concat)
        print("Image saved at ./horizontal_concatenated.jpg")
    elif merge_method == "V" or merge_method == "v":
        im_concat = vconcat_resize([img1, img2])
        cv2.imwrite("vertical_concatenated.jpg", im_concat)
        print("Image saved at ./vertical_concatenated.jpg")
    else:
        print("Invalid Option!")
else:
    print("[ERROR] given path(s) doesn't exist!")
    exit(1)