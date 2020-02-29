from PIL import Image
import numpy as np
import random

letters = {}

def crop_img(image):
    pixels = image.load()

    w, h = image.size
    minw, minh = w, h
    maxw, maxh = 0, 0
    for i in range(w):
        for j in range(h):
            if pixels[i, j][3] != 0:
                minw, minh = min(minw, i), min(minh, j)
                maxw, maxh = max(maxw, i), max(maxh, j)

    return image.crop((minw, minh, maxw, maxh))

def read_letters(path, letters_map, maxh):
    img = Image.open(path).convert('RGBA')
    arr = np.array(np.asarray(img))

    r, g, b, a = np.rollaxis(arr ,axis=-1)    
    mask = ((r > 200) & (g > 200) & (b > 200))
    arr[mask, 3]=0

    tr_img = Image.fromarray(arr, mode='RGBA')
    pixels = tr_img.load()
    w, h = tr_img.size

    k = 0
    lin = -1
    for i in range(w):
        for j in range(h):
            if pixels[i, j][3] != 0:
                if lin == -1:
                    lin = i
                break
        else:
            if lin != -1:
                letter = tr_img.crop((lin, 0, i + 5, h))
                letter.thumbnail((letter.size[0], maxh), Image.BICUBIC)
                letters[letters_map[k]] = letters.get(letters_map[k], []) + [crop_img(letter)]

                lin = -1
                k += 1

                if k >= len(letters_map):
                    return

read_letters('resources/letters.jpg', 'abcdefghijklmnopqrstuvwxyz', 120)
read_letters('resources/l3.jpg', 'abcefghijklmnopqrstuvw', 200)
read_letters('resources/c1.jpg', '1234567890.,()', 200)

bg = Image.open('resources/background.jpg')

s = '1. in the morning my father always buys a newspaper in the newspaper stand.\n2. john seldom goes on holiday in autumn\n3. i am occasionally late for classes, but i am not at all proud of it\n4. this film has just been shown to the young audience'
y = 130
x = 20
for line in s.split('\n'):
    for word in line.split():
        word_letters = []
        word_w = 0

        for l in word:
            if letters.get(l) is None:
                l = l.lower()
            
            if letters.get(l) is None:
                word_w += 20
                continue
                
            limg = random.choice(letters[l.lower()]).rotate(-random.randint(1, 5))
            word_letters.append((word_w, limg, l))
            word_w += limg.size[0] + random.randint(3, 6)
        
        if word_w + x > 1650:
            y += 118
            x = 20

        for lx, limg, l in word_letters:
            ly = y - limg.size[1]
            if l in ['y', 'g', 'p', ',']:
                ly += 20
            
            bg.paste(limg, (x + lx, ly), limg)
        
        x += word_w + 40
        if x > 1650:
            y += 118
            x = 20
    
    x = 20
    y += 118

bg.show()