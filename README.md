# pygui

给manga-image-translator做的界面，所有库都写死在d盘下，只能放在d盘里运行，没有可以看这个改 https://jingyan.baidu.com/article/d8072ac48f8332ad95cefda8.html

我系统是win11，安装的是 python 3.10.10（64-bit），配置是13900k+4090

python在这里下载https://www.python.org/downloads/windows/

发行的需要全部下来，再解压，因为是分卷压缩

安装好 python 3.10.10 和下载解压完trans，放到d盘根目录，进入 D:/trans下打开 cmd 执行  pip install -r requirements.txt

1. 配置好python环境后，假设翻译目录是 D:/trans, 配置的python环境在 D:/trans/scripts
2. 打开 D:/trans/scripts, 地址栏输入 cmd ,然后在弹出cmd界面中执行命令 `activate`,再执行命令 `cd .. `
3. 安装库,继续在该 cmd界面中执行命令 `pip install PySimpleGUI`
4. 然后继续执行 `python win.py` 即可显示界面窗口
5. 也可右键编辑 start.bat ，修改里面的目录为正确的目录后，直接双击 start.bat 执行显示界面窗口

2023.5.30 d:/trans/scripts 添加 py3langid

2023.5.28 界面添加了分辨率选项


![1](https://github.com/1439707509/pygui/assets/128567416/bfb69910-3430-428c-8486-141d900d5a1f)
![2](https://github.com/1439707509/pygui/assets/128567416/e58861e1-c6d0-4ed5-b3c9-b0861f9fa4ae)
![3](https://github.com/1439707509/pygui/assets/128567416/df598dda-2766-4833-81d9-1a7fd36453d4)
![4](https://github.com/1439707509/pygui/assets/128567416/c6c31f9e-a30b-42c1-baac-d333480f41c5)
![6666](https://github.com/1439707509/pygui/assets/128567416/baf32815-1233-48a7-b7ac-e3dc146a9616)
![66](https://github.com/1439707509/pygui/assets/128567416/ed9d8b86-5587-4627-8b86-6272072136c5)




