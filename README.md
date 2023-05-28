# pygui

给manga-image-translator做的界面，写死在d盘下，只能放在d盘里运行

发行的需要全部下来，然后把Lib扔到，trans 里面，Lib是分卷压缩

打包好的文件 链接：https://pan.baidu.com/s/1KxB6zBQj7XaEcRXrfxE4mg?pwd=orlo 提取码：orlo（不是最新的了，自己把最新的源码扔进文件里覆盖吧）

1. 配置好python环境后，假设翻译目录是 D:/trans, 配置的python环境在 D:/trans/scripts
2. 打开 D:/trans/scripts, 地址栏输入 cmd ,然后在弹出cmd界面中执行命令 `activate`,再执行命令 `cd .. `
3. 安装库,继续在该 cmd界面中执行命令 `pip install PySimpleGUI`
4. 然后继续执行 `python win.py` 即可显示界面窗口
5. 也可右键编辑 start.bat ，修改里面的目录为正确的目录后，直接双击 start.bat 执行显示界面窗口

2023.5.28 添加了分辨率选项
