### 介绍
基于 itchat 做的简单微信个人号机器人，主要实现的功能如下：
* 接收图片，并预测图片中人物的年龄及表情
* 接收图片，并将图片转化为艺术风格的图片
* 利用SVM预测国内股票的下一个交易日的开盘价
* 聊天机器人
* 其他功能
	* 查看服务器内存及CPU状况
	* 更新股票列表
	* ……

### 安装
pip install -r requirements.txt

### 使用
1、cd songbing
2、python App.py
3、打开手机微信扫一扫，完成登录

### 效果
https://github.com/wk448378469/songbing/tree/master/wx_robot/userpic/effect.png
https://github.com/wk448378469/songbing/tree/master/wx_robot/handler/neuralstyle/neuralpic/test.png
https://github.com/wk448378469/songbing/tree/master/wx_robot/handler/predictStock/predictResult/test.png

### 结构
* App.py (主程序，初始化并注册处理器)
* wx_robot
	* robot.py（实现itchat接收信息，并分配给合理的处理器）
	* userpic（用户上传图片的目录）
	* handler
		* myselfHandler.py（处理特定指令的处理器，包括查看内存，更新股票列表等）
		* neuralHandler.py（预测年龄及艺术风格转换的处理器）
		* predictStockHandler.py（预测股票的处理器）
		* publicHandler.py（获取特点文本输入的回复处理器）
		* redEnvelopesHandler.py（接收红包的处理器）
		* xiaoDouHandler.py（小豆机器人的处理器）
		* faceDetection
			* faceDetection.py（面部识别的核心函数）
		* neuralstyle
			* models（训练好的模型目录）
			* neuralpic（生成的艺术风格图片的保存目录）
			* model.py（生成神经网络的函数）
			* myeval.py（实现接收图片和模型的通信）
			* preprocessing_factory.py
			* reader.py（读取图片的函数）
			* vgg_preprocessing.py
		* predictStock
			* predictResult（生成预测股票图片的保存目录）
			* stockCodeList.csv（股票代码列表）
			* test.py（预测股票的核心函数）
