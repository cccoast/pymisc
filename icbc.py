#encoding=utf-8
from PIL import Image
import matplotlib
matplotlib.use('qt4agg')
from matplotlib.font_manager import *
import matplotlib.pyplot as plt
myfont = FontProperties(fname='/usr/share/fonts/truetype/wqy/wqy-microhei.ttc')
import pandas as pd
import os

sub_img_root_path = r'/media/xudi/coding/samba/lyx/pics'

def resizeImg(**args):
    args_key = {'ori_img':'','dst_w':'','dst_h':''}
    arg = {}
    for key in args_key:
        if key in args:
            arg[key] = args[key]
    
    im = arg['ori_img']
    ori_w,ori_h = im.size
    widthRatio = heightRatio = None
    ratio = 1
    if (ori_w and ori_w > arg['dst_w']) or (ori_h and ori_h > arg['dst_h']):
        if arg['dst_w'] and ori_w > arg['dst_w']:
            widthRatio = float(arg['dst_w']) / ori_w #正确获取小数的方式
        if arg['dst_h'] and ori_h > arg['dst_h']:
            heightRatio = float(arg['dst_h']) / ori_h

        if widthRatio and heightRatio:
            if widthRatio < heightRatio:
                ratio = widthRatio
            else:
                ratio = heightRatio

        if widthRatio and not heightRatio:
            ratio = widthRatio
        if heightRatio and not widthRatio:
            ratio = heightRatio
            
        newWidth = int(ori_w * ratio)
        newHeight = int(ori_h * ratio)
    else:
        newWidth = ori_w
        newHeight = ori_h
        
    return im.resize((newWidth,newHeight),Image.ANTIALIAS)
    
def draw():
    img_src_path1 = r'/media/xudi/coding/samba/lyx/2.jpg'
    img_src_path2 = r'/media/xudi/coding/samba/lyx/1.jpg'
    
    fig = plt.figure()  
    
    ax1 = fig.add_subplot(121)
    img = Image.open(img_src_path1)
    ax1.imshow(img)
    ax1.axis('off')
    
    ax2 = fig.add_subplot(122)
    img = Image.open(img_src_path2)
    ax2.imshow(img)
    ax2.axis('off')
    
    plt.show()

def cut(no):
    img_src_path = r'/media/xudi/coding/samba/lyx/big/{0}.png'.format(no)
    print img_src_path
    img = Image.open(img_src_path)
    width = img.size[0]  
    height = img.size[1]    
    width_adjust = 30 
    height_adjust = 30
    box1=(0 + width_adjust,20 + height_adjust,width - width_adjust - 70,height/6 - height_adjust)
    header=img.crop(box1)
    width_minus,height_minus,bottom_minus = 110,220,40
    box2=(width_minus,width/2 + height_minus - 126,width - width_minus,height - bottom_minus)
    tail=img.crop(box2)
    args_key = {'ori_img':header,'dst_w':tail.width,'dst_h':tail.height}
    header = resizeImg(**args_key)
    tail.paste(header,(0,0,header.width,header.height))
    return tail
    
def get_sub_img(no):
    img_src_path = os.path.join(sub_img_root_path,str(no) + '.png') 
    img = Image.open(img_src_path)    
    width = img.size[0]  
    height = img.size[1] 
    width_minus,height_minus,bottom_minus = 110,220,40
    box=(width_minus,width/2 + height_minus,width - width_minus,height - bottom_minus)
    img=img.crop(box)
    return img

def generate():
    src_path = r'/media/xudi/coding/samba/lyx/12.csv'
    df = pd.read_csv(src_path,index_col = 0,encoding = 'utf8')
#     print df
    
    left  = 0.08  # the left side of the subplots of the figure
    right = 0.84   # the right side of the subplots of the figure
    bottom = 0.2   # the bottom of the subplots of the figure
    top = 0.8      # the top of the subplots of the figure
    wspace = 0.01   # the amount of width reserved for blank space between subplots
    hspace = 0.10   # the amount of height reserved for white space between subplots
    
    ny = 2
    nx = 6  
    fig, ax = plt.subplots(ny, nx, figsize=(92, 126) )
    for i in range(ny):
        sub_ax = ax[i]
        for j in range(nx):
            nth = i * nx + j + 1
            start = df.loc[nth]['start']
            end   = df.loc[nth]['date']
            name  = df.loc[nth]['name']
            sub_ax[j].imshow(cut(nth))
            sub_ax[j].axis('off')
            sub_ax[j].set_title('%02d.%02d - %02d.%02d %s' \
                                %(start/100, start%100, end/100, end%100,name + u'座'),\
                                fontproperties=myfont,\
                                fontsize = 16)
    plt.legend()
    plt.subplots_adjust(left = left,right = right,bottom = bottom,top = top,wspace = wspace,hspace = hspace)
#     plt.savefig('/home/xudi/lyx.png')
    plt.show()
    
if __name__ == '__main__':
    generate()
    
    
        
        