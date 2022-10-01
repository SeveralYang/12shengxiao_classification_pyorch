本程序经简单修改后,即可应用于其他分类任务
修改步骤如下:
	01: 修改 02item_to_index.txt 中的字典
	02: 依次执行
		爬取图片(grab_images.py),
		人工筛选,
		预处理(pre_process.py)
	03:将src.train.py 
		model = build_model(X)中X改为分类总数
	04:运行train.py 
	05:在cmd中执行 tensorboard -ligdir weight
		打开tensorboard
