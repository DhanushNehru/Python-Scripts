#!/usr/bin/env python
# coding: utf-8

# In[1]:


#### Importing libraries for reading and displaying images

#for reading images
import cv2
#for displaying images
import matplotlib.pyplot as plt

#### Reading image

image = cv2.imread('sample.jpg')
img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
img = img.tolist()

#### Displaying Image Comparisons

def compare(original, manipulated, title_1="Original", title_2="Manipulated"):
    plt.figure(figsize=(15, 25))
    plt.subplot(1, 2, 1)
    plt.title(title_2)
    plt.imshow(manipulated)
    plt.subplot(1, 2, 2)
    plt.title(title_1)
    plt.imshow(original)
    plt.show()

def print_shape(img):
    try:
        print("Shape of the array is:", len(img), "x", len(img[0]), "x",
              len(img[0][0]))
    except:
        print("Shape of the array is:", len(img), "x", len(img[0]))


def add_list(img1, img2):
    return [[img1[i][j] + img2[i][j] for j in range(len(img1[0]))]
            for i in range(len(img1))]


#original shape
print("Original:")
print_shape(img)
print("\n")


def channel_first(img):
    return [[[img[j][k][i] for k in range(len(img[0]))]
             for j in range(len(img))] for i in range(len(img[0][0]))]


print("After Channel_first operation")
z = channel_first(img)
print_shape(z)
print("\n")


def channel_last(img):
    return [[[img[k][i][j] for k in range(len(img))]
             for j in range(len(img[0][0]))] for i in range(len(img[0]))]


print("After Channel_last operation")
z = channel_last(z)
print_shape(z)

#### Displaying channels

channel_wise = channel_first(img)
plt.figure(figsize=(10, 20))
plt.subplot(1, 3, 1)
plt.title("Red")
plt.imshow(channel_wise[0], cmap="gray")
plt.subplot(1, 3, 2)
plt.title("Green")
plt.imshow(channel_wise[1], cmap="gray")
plt.subplot(1, 3, 3)
plt.title("Blue")
plt.imshow(channel_wise[2], cmap="gray")
plt.show()


def channel_wise_addition(img):
    temp = channel_first(img)
    return add_list(temp[2], add_list(temp[0], temp[1]))


plt.imshow(channel_wise_addition(img), cmap="gray")
plt.show()

#### Invert

def invert(img):
    return [[[255 - k for k in j] for j in i] for i in img]


compare(img, invert(img))

#### Mirror Vertical

def mirror_v(img):
    return [img[-i - 1] for i in range(len(img))]


compare(img, mirror_v(img))

#### Mirror Horizontal

def mirror_h(img):
    return [[img[i][-j - 1] for j in range(len(img[0]))]
            for i in range(len(img))]


compare(img, mirror_h(img))


def blur_1(img, strength=1):
    temp1 = []
    for i in range(len(img)):
        temp2 = []
        for j in range(len(img[0])):
            temp3 = []
            for k in range(len(img[0][0])):
                temp4 = []
                for x in range(1, strength + 1):
                    a_pixels = 1
                    temp = img[i][j][k]
                    try:
                        temp += img[i + x][j + x][k]
                        a_pixels += 1
                    except:
                        True
                    try:
                        temp += img[i + x][j][k]
                        a_pixels += 1
                    except:
                        True
                    try:
                        temp += img[i + x][j - x][k]
                        a_pixels += 1
                    except:
                        True
                    try:
                        temp += img[i][j - x][k]
                        a_pixels += 1
                    except:
                        True

                    try:
                        temp += img[i - x][j - x][k]
                        a_pixels += 1
                    except:
                        True
                    try:
                        temp += img[i - x][j][k]
                        a_pixels += 1
                    except:
                        True
                    try:
                        temp += img[i - x][j + x][k]
                        a_pixels += 1
                    except:
                        True
                    try:
                        temp += img[i][j + x][k]
                        a_pixels += 1
                    except:
                        True
                    temp4.append(temp / a_pixels)
                temp3.append(int(sum(temp4) / len(temp4)))
            temp2.append(temp3)
        temp1.append(temp2)

    return temp1



compare(img, blur_1(img, strength=20))


def blur_2(img, strength=1):

    def blur_strength_1(img):
        temp1 = []
        for i in range(len(img)):
            temp2 = []
            for j in range(len(img[0])):
                temp3 = []
                for k in range(len(img[0][0])):
                    a_pixels = 1
                    temp = img[i][j][k]
                    try:
                        temp += img[i + 1][j + 1][k]
                        a_pixels += 1
                    except:
                        True
                    try:
                        temp += img[i + 1][j][k]
                        a_pixels += 1
                    except:
                        True
                    try:
                        temp += img[i + 1][j - 1][k]
                        a_pixels += 1
                    except:
                        True
                    try:
                        temp += img[i][j - 1][k]
                        a_pixels += 1
                    except:
                        True

                    try:
                        temp += img[i - 1][j - 1][k]
                        a_pixels += 1
                    except:
                        True
                    try:
                        temp += img[i - 1][j][k]
                        a_pixels += 1
                    except:
                        True
                    try:
                        temp += img[i - 1][j + 1][k]
                        a_pixels += 1
                    except:
                        True
                    try:
                        temp += img[i][j + 1][k]
                        a_pixels += 1
                    except:
                        True

                    temp3.append(int(temp / a_pixels))
                temp2.append(temp3)
            temp1.append(temp2)
        return temp1

    temp = img.copy()
    for i in range(strength):
        temp = blur_strength_1(temp)
    return temp



compare(img, blur_2(img, 20))


#### Resize

def resize(img, size):

    return [[[
        img[int(len(img) * i / size[0])][int(len(img[0]) * j / size[1])][k]
        for k in range(3)
    ] for j in range(size[1])] for i in range(size[0])]


compare(img, resize(img, (500, 500)))

#### Lightness

def lightness(img, b=50):

    return [[[
        int((255 * (b / 100)) + (img[i][j][k] * (1 - (b / 100))))
        for k in range(len(img[0][0]))
    ] for j in range(len(img[0]))] for i in range(len(img))]


compare(img, lightness(img, 50))

#### Brightness

def brightness(img, strength=0):
    return [[[
        int((510 / (1 + (2.7183**(-strength * img[i][j][k] / 255)))) - 255)
        for k in range(len(img[0][0]))
    ] for j in range(len(img[0]))] for i in range(len(img))]


compare(img, brightness(img, 5))

#### Contrast

def contrast(img, strength=0):
    return [[[
        int(255 / (1 + (2.7183**(-strength *
                                 ((img[i][j][k] - 127.5) / 127.5)))))
        for k in range(len(img[0][0]))
    ] for j in range(len(img[0]))] for i in range(len(img))]

compare(img, contrast(img, 10))

