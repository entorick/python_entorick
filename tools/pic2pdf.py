# -*- coding: utf-8 -*-
from PIL import Image
import os


def rea(path, pdf_name):
    file_list = os.listdir(path)
    pic_name = {}
    im_list = []
    tmp_lst = []
    for v in file_list:
        if "jpg" in v or 'png' in v or 'jpeg' in v:
            pic_name[v.split('.')[0]] = v
            tmp_lst.append(int(v.split('.')[0]))

    tmp_lst.sort()
    new_pic = []

    for v in tmp_lst:
        new_pic.append(pic_name[str(v)])

    im1 = Image.open(os.path.join(path, new_pic[0]))
    new_pic.pop(0)
    for i in new_pic:
        img = Image.open(os.path.join(path, i))
        if img.mode == "RGBA":
            img = img.convert('RGB')
            im_list.append(img)
        else:
            im_list.append(img)
    im1.save(pdf_name, "PDF", resolution=100.0, save_all=True, append_images=im_list)
    print("输出文件名称：", pdf_name)


if __name__ == '__main__':

    pdf_name = ''
    mypath = r"Y:\\comics\\全职法师\\"
    lst = os.listdir(mypath)
    for chapter in lst:
        pdf_name = os.path.join(mypath, chapter + '.pdf')
        chapter_path = os.path.join(mypath, chapter)
        rea(chapter_path, pdf_name)