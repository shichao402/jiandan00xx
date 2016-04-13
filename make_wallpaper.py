# coding=utf8
import os
import Image
import random
import win32api, win32con, win32gui

def image_resize(img, size=(1500, 1100)):
    try:
        if img.mode not in ('L', 'RGB'):
            print "RGB"
            img = img.convert('RGB')
        img = img.resize(size, Image.ANTIALIAS)
    except Exception, e:
        print e
        pass
    return img

def image_merge(images, output_dir='output', output_name='merge.jpg', \
                restriction_max_width=None, restriction_max_height=None, column=8):

    max_width = 1920
    max_height = 1080
    # 产生一张空白图
    new_img = Image.new('RGB', (max_width, max_height), 255)
    # 合并
    x = y = 0
    for img_path in images:
        if os.path.exists(img_path):
            img = Image.open(img_path)
            width, height = img.size

            resize = float(max_width/ column) / width
            new_height = int(height * resize)
            new_width = int(max_width / column)
            
            img = image_resize(img, size=(new_width, new_height))
            width, height = img.size
            new_img.paste(img, (x, y))
            
            y += height
            if y >= max_height:
                x += width
                y = 0

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    save_path = '%s/%s' % (output_dir, output_name)
    new_img.save(save_path, quality = 95)
    return save_path

def compare(x, y):
    stat_x = os.stat(DIR + "/" + x)
    stat_y = os.stat(DIR + "/" + y)
    if stat_x.st_ctime < stat_y.st_ctime:
        return -1
    elif stat_x.st_ctime > stat_y.st_ctime:
        return 1
    else:
        return 0

if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings
    process = CrawlerProcess(get_project_settings())
    process.crawl('ooxx')
    process.start() # the script will block here until the crawling is finished

    root = os.path.split(os.path.realpath(__file__))[0]
    DIR = root + os.sep + "downloads" + os.sep + "images" + os.sep + "full"

    iterms = os.listdir(DIR)

    iterms.sort(compare)
    count = 0
    wlist = []
    for iterm in iterms:
        if os.path.splitext(iterm)[1] == '.gif':
            continue
        if count > 50:
            break;
        wlist.append(DIR + os.sep + iterm)
        count += 1
    random.shuffle(wlist)
    image_merge(images=wlist, column=7)

    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, "." + os.sep + "output" + os.sep + "merge.jpg", 1+2)

