import cv2
import torch
from torch.utils.data import Dataset


class MyDataSet(Dataset):
    def __init__(self, txt_path, transform=None):
        self.transform = transform
        self.image_path = []
        self.image_label = []
        f = open(txt_path, encoding="utf-8")
        lines = f.readlines()
        for line in lines:
            p, lab = line.split("###")
            self.image_path.append(p)
            self.image_label.append(lab)
        f.close()
        assert len(self.image_label) == len(self.image_path)

    def __getitem__(self, index):
        image = cv2.imread(self.image_path[index])
        label = int(self.image_label[index])

        if self.transform is not None:
            image = self.transform(image)
        return image, label

    def __len__(self):
        return len(self.image_label)


if __name__ == '__main__':
    train_set = MyDataSet(txt_path="../train.txt")
    x, y = train_set.__getitem__(0)
    cv2.imshow(f"label:{y}", x)
    cv2.waitKey()
    cv2.destroyAllWindows()
