"""
爬数据集
"""
import os
import time

import requests
import urllib3

urllib3.disable_warnings()


def create_dir(keyword, path=None):
    if not path:
        path = os.path.join('../dataset/', str(keyword))
    if not os.path.exists('../dataset'):
        os.makedirs('../dataset')
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def grab(keyword, path, require_number):
    properties = open('../01properties.txt', encoding="utf-8").read().split('######')
    cookies = eval(properties[0])
    headers = eval(properties[1])
    num = 0
    count = 0
    while True:
        count += 1
        page = count * 30
        params = eval(properties[2])
        response = requests.get('https://image.baidu.com/search/acjson', headers=headers, params=params,
                                cookies=cookies)
        if response.status_code == 200:
            try:
                json_data = response.json().get("data")
                if json_data:
                    for x in json_data:
                        data_type = x.get("type")
                        if type not in ["gif"]:
                            img = x.get("thumbURL")
                            fromPageTitleEnc = x.get("fromPageTitleEnc")
                            try:
                                resp = requests.get(url=img, verify=False)
                                time.sleep(1)
                                print(f"链接 {img}")
                                file_save_path = f'{path}/{num}.{data_type}'
                                with open(file_save_path, 'wb') as f:
                                    f.write(resp.content)  # 保存图像文件到本地
                                    f.flush()
                                    print('第 {} 张图像 {} 爬取完成'.format(num, fromPageTitleEnc))
                                    num += 1
                                    if num >= require_number:
                                        print('over')
                                        return None
                                if num >= require_number:
                                    print('over')
                                    return None
                            except Exception:
                                pass
                else:
                    pass
            except:
                pass
        else:
            break


if __name__ == '__main__':
    keywords = eval(open('../02item_to_index.txt', encoding="utf-8").read().split('######')[1])
    # keywords = ['鼠', '牛', '虎', '兔', "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
    for k in keywords:
        dir_path = create_dir(k)
        grab(keyword=k, require_number=200, path=dir_path)
