import glob
import os
import random

from PIL import Image

PICTURE_SIZE = 224
TEST_SET_RATE = 0.2


def resize_all(root_path):
    """
    将root_path目录及其子目录下所有JPG和PNG图片转化为（3xPICTURE_SIZExPICTURE_SIZE）的JPG图片，并且按照5%的比例划分出测试集
    :param root_path:目标目录
    :return:None
    """
    dirs = glob.glob(os.path.join(root_path, '*'))
    dirs = [d for d in dirs if os.path.isdir(d)]
    print(f'totally {len(dirs)} dirs')
    count = 0
    dict1 = open('../02item_to_index.txt', encoding="utf-8").read().split('######')
    dict1 = eval(dict1[0])
    print(dict1)
    for path in dirs:
        print(str(path)+" done")
        dir_name0, dir_name = os.path.split(path)  # 获取文件夹名称
        train_dir = os.path.join(dir_name0, 'train')
        os.makedirs(train_dir, exist_ok=True)
        test_dir = os.path.join(dir_name0, 'test')
        os.makedirs(test_dir, exist_ok=True)
        files = glob.glob(os.path.join(root_path, dir_name, '*.JPEG'))
        files += glob.glob(os.path.join(root_path, dir_name, '*.jpg'))
        files += glob.glob(os.path.join(root_path, dir_name, '*.png'))
        random.shuffle(files)

        test_set_size = int(len(files) * TEST_SET_RATE)
        for i, file in enumerate(files):
            new_img = Image.open(file).convert('RGB')

            if i <= test_set_size:
                p = os.path.join(test_dir, '{}.jpg'.format(str(count).rjust(6, '0')))
                with open("../test.txt", "a") as f:
                    f.write(str(p) + f"###{dict1[dir_name]}" + "\n")
            else:
                p = os.path.join(train_dir, '{}.jpg'.format(str(count).rjust(6, '0')))
                with open("../train.txt", "a") as f:
                    f.write(str(p) + f"###{dict1[dir_name]}" + "\n")
            new_img.save(p)
            count += 1


if __name__ == '__main__':
    resize_all('../dataset')
