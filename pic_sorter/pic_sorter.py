# Author:TripRunn

import os
import shutil
from PIL import ImageFile
from PIL import Image
ImageFile.LOAD_TRUNCATED_IMAGES = True


def get_filelist(dir):
    """
    获取文件夹中所有文件
    dir:目录
    Filelist: 返回值为该目录下的文件列表
    """
    Filelist = []
    lists = os.listdir(dir)
    for i in range(0, len(lists)):
        filepath = os.path.join(dir, lists[i])
        if os.path.isfile(filepath):
            Filelist.append(filepath)
    return Filelist


def exist_mkdir(filepath):
    """
    目录是否存在，不存在则创建目录
    """
    isExists = os.path.exists(filepath)
    if not isExists:
        # 如果不存在则创建目录
        os.mkdir(filepath)


def except_pic(imgpath, errorpath, movesrc=None, ept=False):
    """
    打开异常的图片，原图拷贝到第四类文件夹中；
    保存异常的图片，移动到第四类文件夹，然后把原图拷贝过来（覆盖）

    imgpath: 原文件路径
    errorpath: 第四类目录路径
    movesrc:需要移动的文件路径
    ept:是否保存异常
    """
    exist_mkdir(errorpath)
    if ept:
        # 保存后异常的把已经保存的图片移动到第四类文件夹
        shutil.move(movesrc, errorpath)
    # 再把原图复制第四类文件夹进行覆盖
    shutil.copy(imgpath, errorpath)


def sort_save(img, sortpath, imgpath, errorpath):
    """
    img: 输入图片open对象
    sortpath: 输出图片文件路径
    imgpath:原文件路径
    errorpath:第四类目录路径
    """
    try:
        # 保存异常的图片放入第四个文件夹中
        img.save(sortpath)
        return True
    except:
        except_pic(imgpath, errorpath, sortpath, True)
        return False


def sort_by_wl1(imglist):
    """
    根据图片尺寸进行三分类,并重置分辨率
    imglist:list, 图片列表
    """
    path = []
    path.append(os.path.join(os.getcwd(), '分类\\矮胖形'))
    path.append(os.path.join(os.getcwd(), '分类\\高瘦形'))
    path.append(os.path.join(os.getcwd(), '分类\\方形'))

    errorpath = os.path.join(os.getcwd(), '分类\\打不开')

    # 创建三分类目录
    exist_mkdir(os.path.join(os.getcwd(), '分类'))
    for i in range(0, len(path)):
        exist_mkdir(path[i])

    # 读取、分类
    for i in range(0, len(imglist)):
        filename1 = os.path.basename(imglist[i])
        try:
            # 打不开的图片，分类到第四个文件夹中
            img = Image.open(imglist[i])
        except:
            # 打开异常的图片拷贝到第四个文件夹
            except_pic(imglist[i], errorpath)
            print("第{0}个图片，{1}--->打不开 （打不开）".format(i + 1, filename1))
            continue

        width = img.size[0]
        length = img.size[1]

        # if img.mode != "RGB":
        #     img = img.convert('RGB')

        if width > length:
            # 矮胖形
            sortpath = os.path.join(path[0], filename1)
            su = sort_save(img, sortpath, imglist[i], errorpath)
            if not su:
                print("第{0}个图片，{1}--->{2}（不能保存）".format(i + 1, filename1, errorpath.split('\\')[-1]))
                continue
        elif width < length:
            # 高瘦形
            sortpath = os.path.join(path[1], filename1)
            su = sort_save(img, sortpath, imglist[i], errorpath)
            if not su:
                print("第{0}个图片，{1}--->{2}（不能保存）".format(i + 1, filename1, errorpath.split('\\')[-1]))
                continue
        elif width == length:
            # 方形
            sortpath = os.path.join(path[2], filename1)
            su = sort_save(img, sortpath, imglist[i], errorpath)
            if not su:
                print("第{0}个图片，{1}--->{2}（不能保存）".format(i + 1, filename1, errorpath.split('\\')[-1]))
                continue
        print("第{0}个图片，{1}--->{2}".format(i+1, filename1, sortpath.split('\\')[-2]))


if __name__ == '__main__':

    # 待分类的图片目录
    image_path = os.path.join(os.getcwd(), 'test')
    filelist = get_filelist(image_path)

    sort_by_wl1(filelist)




