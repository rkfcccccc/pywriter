from PIL import Image, ImageFilter
import numpy as np
import random
import os

input_file = 'input.txt'
output_folder = 'output'
backgrounds = [
    {
        'path': 'resources/bg1.jpg',
        'start_x': 20,
        'start_y': 130,
        'line_height': 118,
        'max_y': 2400
    },

    {
        'path': 'resources/bg2.jpg',
        'start_x': 250,
        'start_y': 100,
        'line_height': 118,
        'max_y': 2400
    }
]

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

def load_letters(path, letters_map, maxh):
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
                letter.thumbnail((w, maxh), Image.BICUBIC)
                letters[letters_map[k]] = letters.get(letters_map[k], []) + [crop_img(letter)]

                lin = -1
                k += 1

                if k >= len(letters_map):
                    return

def show_letters():
    global x, y
    for k, v in letters.items():
        for limg in v + [' '] + [random.choice(letters[x]) for x in '(' + str(len(v)) + ')']:
            if limg == ' ':
                x += 30
                continue
                
            ly = y - limg.size[1]
            if k in ['y', 'g', 'p', ',']:
                ly += 20
            
            bg.paste(limg, (x, ly), limg)
            x += limg.size[0] + 20

        x = 20
        y += 118 // 2

letters = {}
load_letters('resources/l1.jpg', 'aaaaaaaaaabbbbbbbcccccddddddeeeeee', 120)
load_letters('resources/l2.jpg', 'ffffffffgggggghhhhhhhiiiiijjjjjkkkkkk', 120)
load_letters('resources/l3.jpg', 'llllllllmmmmmmmmnnnnnnooooooopppppp', 120)
load_letters('resources/l4.jpg', 'qqqqqqqrrrrrrrrssssssstttttttuuuuuuu', 120)
load_letters('resources/l5.jpg', 'vvvvvvvvvvvwwwwwwxxxxxxxxyyy', 120)
load_letters('resources/l6.jpg', 'zzzzzzzzz', 120)
load_letters('resources/ul1.jpg', 'AAABBBCCCDDDEEEFFFGGGHHHIIIJJJKKKLLLMMM', 180)
load_letters('resources/ul2.jpg', 'NNNOOOOPPPQQQRRRSSSSSTTTTTTTUUUVVVV', 180)
load_letters('resources/ul3.jpg', 'WWWWWXXXXYYYZZZZ', 180)
load_letters('resources/spc.jpg', '1234567890.,()', 180)
load_letters('resources/spc2.jpg', '!!!!?????$$$1234567890', 200)

with open(input_file, 'r') as f:
    text = ''.join(f.readlines())

for filename in os.listdir(output_folder):
    file_path = os.path.join(output_folder, filename)
    if (os.path.isfile(file_path) or os.path.islink(file_path)) and filename[0] != '.':
        os.unlink(file_path)

bgid = 0
bgimg, x, y = Image.open(backgrounds[bgid]['path']), backgrounds[bgid]['start_x'], backgrounds[bgid]['start_y']
for line in text.split('\n'):
    for word in line.split(' '):
        if y > backgrounds[bgid % len(backgrounds)]['max_y']:
            bgimg.filter(ImageFilter.GaussianBlur(1)).save(f'{output_folder}/{bgid}.jpg')
            bgid += 1

            i = bgid % len(backgrounds)
            bgimg = Image.open(backgrounds[i]['path'])
            x = backgrounds[i]['start_x']
            y = backgrounds[i]['start_y']

        word_letters = []
        word_w = 0

        for i, l in enumerate(word):
            if letters.get(l) is None:
                l = l.lower()
            
            if letters.get(l) is None:
                word_w += 20
                print('no letter', l)
                continue
                
            limg = random.choice(letters[l]).rotate(-random.randint(1, 5))
            word_letters.append((word_w, limg, l))
            word_w += limg.size[0] + (random.randint(3, 6) if i + 1 != len(word) else 0)
        
        if word_w + x > 1650:
            y += backgrounds[bgid % len(backgrounds)]['line_height']
            x = backgrounds[bgid % len(backgrounds)]['start_x']
        
        for lx, limg, l in word_letters:
            ly = y - limg.size[1]
            if l in ['y', 'g', 'p']:
                ly += 15
            
            if l in [',']:
                ly += 10
            
            bgimg.paste(limg, (x + lx, ly), limg)
        
        x += word_w + 30
        if x > 1650:
            y += backgrounds[bgid % len(backgrounds)]['line_height']
            x = backgrounds[bgid % len(backgrounds)]['start_x']
    
    x = backgrounds[bgid % len(backgrounds)]['start_x']
    y += backgrounds[bgid % len(backgrounds)]['line_height']

bgimg.filter(ImageFilter.GaussianBlur(1)).save(f'{output_folder}/{bgid}.jpg')