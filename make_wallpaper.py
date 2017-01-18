# coding=utf8
import os
from PIL import Image
import random
import win32api, win32con, win32gui
import ctypes
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def image_resize(img, size=(1500, 1100)):
    try:
        if img.mode not in ('L', 'RGB'):
            img = img.convert('RGB')
        img = img.resize(size, Image.ANTIALIAS)
    except Exception, e:
        print e
        pass
    return img

def image_merge(images_dir, output_dir='output', output_name='merge.jpg', \
                restriction_max_width=None, restriction_max_height=None, column=8):
    images = os.listdir(images_dir)

    #random.shuffle(images)
    images.sort(compare)

    max_width = 2560
    max_height = 1440
    # 产生一张空白图
    new_img = Image.new('RGB', (max_width, max_height), 255)
    # 合并
    side = 1
    y = 0
    x = max_width / 3
    for img_path in images:
        if os.path.splitext(img_path)[1] == '.gif':
            continue
        img_path = images_dir + os.sep + img_path
        if os.path.exists(img_path):
            try:
                img = Image.open(img_path)
            except Exception, e:
                print "can not load image:", img_path
                continue
            width, height = img.size

            resize = float(max_width/ column) / width
            new_height = int(height * resize)
            new_width = int(max_width / column)
            
            img = image_resize(img, size=(new_width, new_height))
            width, height = img.size
            
            if side > 0:
                #检查y的位置有没有超出范围,超出的话重置一下
                if y >= max_height:
                    x += width
                    y = 0
                #贴图
                new_img.paste(img, (x, y))
                #y累加
                y += height
            if side < 0:
                if y >= max_height:
                    x -= width
                    y = 0
                new_img.paste(img, (x - width, y))
                y += height
            if x > max_width:
                side = -1
                x = max_width / 3
                y = 0
            if x - width < 0:
                break


    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    save_path = '%s/%s' % (output_dir, output_name)
    new_img.save(save_path, quality = 95)
    return save_path

def compare(x, y):
    stat_x = os.stat(DIR + "/" + x)
    stat_y = os.stat(DIR + "/" + y)
    if stat_x.st_mtime < stat_y.st_mtime:
        return 1
    elif stat_x.st_mtime > stat_y.st_mtime:
        return -1
    else:
        return 0

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('ooxx')
    process.start() # the script will block here until the crawling is finished
    
    root = os.path.split(os.path.realpath(__file__))[0]
    DIR = get_project_settings().get('IMAGES_STORE') + os.sep + "full"

    image_merge(images_dir=DIR, column=12)

    SPI_SETDESKWALLPAPER = 20 
    ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, "." + os.sep + "output" + os.sep + "merge.jpg" , 0)

