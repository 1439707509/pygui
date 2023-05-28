# -*- coding: utf-8 -*-
# 机翻软件win11 上控制界面
import PySimpleGUI as sg
from tkinter.filedialog import askdirectory
import os
import subprocess
from tkinter import messagebox
import time
import zipfile
import re
import sys
import shutil
from dotenv import load_dotenv
load_dotenv()

os.environ["sourcelang"]="日语"
# All the stuff inside your window.
langobj = [
    'gpt3',
    'gpt3.5',
    'gpt4',
    'youdao',
    'google',
    'baidu',
    'deepl',
    "papago",
    "offline",
    "offline_big",
    "nnlb",
    "nnlb_big",
    "none",
    "original",
]
layout = [
    [
        sg.Text('当前执行路径', background_color="#e3f2fd", text_color='#212121'),
        sg.Text('', key="cmddir", background_color="#e3f2fd", text_color='#212121')
    ],
    [sg.Text('待翻译图片文件夹', background_color="#e3f2fd", text_color='#212121'), sg.InputText(key="sourceinput"),
     sg.Button('选择文件夹', key="sourcedir", enable_events=True, button_color='#018fff', border_width=0)],
    [sg.Text('输出到目标文件夹', background_color="#e3f2fd", text_color='#212121'), sg.InputText(key="targetinput"),
     sg.Button('选择文件夹', key="targetdir", enable_events=True, button_color='#018fff', border_width=0)],
    [
        sg.Text('选择翻译模型', background_color="#e3f2fd", text_color='#212121'),
        sg.Combo(langobj, readonly=True, key="langinput", default_value="gpt3.5"),
        sg.Text('选择文字检测模型', background_color="#e3f2fd", text_color='#212121'),
        sg.Combo(["default","ctd","craft"], readonly=True, key="detector", default_value="default"),
        sg.Text('输出图片格式', background_color="#e3f2fd", text_color='#212121'),
        sg.Combo(["jpg", "png","webp"], size=(6,16), readonly=True, key="imgformat", default_value="jpg"),
        sg.Text('转黑白为彩色', background_color="#e3f2fd", text_color='#212121'),
        sg.Combo(["yes", "no"], size=(6,16), readonly=True, key="heibai", default_value="no")
    ],
    [
        sg.Text('ocr模型', background_color="#e3f2fd", text_color='#212121'),
        sg.Combo(["32px","48px_ctc"], readonly=True, key="ocr", default_value="48px_ctc"),
        sg.Text('upscale-ratio放大', background_color="#e3f2fd", text_color='#212121'),
        sg.Combo([1,2,3,4,8,16,32], readonly=True, key="ratio", default_value="1")
    ],
    [
        sg.Input(key="zippath", expand_x=True),
        sg.FileBrowse("导入zip包", target="zippath"),
        sg.Button('升级包', key="up")
    ],
    [
        sg.Button('开始执行', key="startbtn", button_color='#2196f3',size=(16,2),font=16),
        sg.Checkbox("使用GPU",default=True,key="usegpu",background_color="#e3f2fd",checkbox_color="#eeeeee",text_color="#ff0000",size=(9,1))
     ],
    [sg.Multiline('', key="loginfo", expand_y=True, expand_x=True, background_color='#f1f9ff', text_color="#666666")]
]
# ocr 程序所在绝对路径
rootdir = os.getcwd()
# 执行后的pid
cmdpid = ""
# ocr脚本名称，用于执行和关闭 tr.py
ocrname = "tr.py"
ocrfile = os.path.join(rootdir, ocrname)
pybin = os.path.join(rootdir, 'Scripts\python.exe -m manga_translator --mode batch --target-lang=CHS ')
current_status="no"
# 使用gpu
usecuda=False

root_dir = os.getcwd()
root_dirname = 'manga-image-translator-main'

start_time = int(time.time())

sg.theme('Material1')
# 解压
def jieya(zip_file):
    # 解压缩文件
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        for info in zip_ref.infolist():
            # 当解压缩的文件已存在于目标目录中时，不提示并覆盖原文件
            extract_path = os.path.join(root_dir, info.filename)
            if os.path.exists(extract_path):
                os.remove(extract_path)
            zip_ref.extract(info, root_dir)

    for root, dirs, files in os.walk(os.path.join(root_dir, root_dirname)):
        # 拼接目标目录
        relpath = os.path.relpath(root, start=os.path.join(root_dir, root_dirname))

        # 移动所有子文件夹
        for d in dirs:
            # src_path = os.path.join(root, d)
            dst_path = os.path.join(root_dir, relpath, d)
            print('---- ', dst_path)
            os.makedirs(dst_path, exist_ok=True)
            # if not os.path.exists(dst_path):
            # shutil.move(src_path, dst_path)
        # return
        # 移动所有子文件夹
        for f in files:
            src_path = os.path.join(root, f)
            dst_path = os.path.join(root_dir, relpath, f)
            # continue
            if os.path.exists(dst_path):
                os.remove(dst_path)
            shutil.move(src_path, dst_path)
            print(src_path, ' =====  ', dst_path)
    # 删除 root_dirname 目录
    try:
        shutil.rmtree(os.path.join(root_dir, root_dirname))
    except:
        print('清理失败')


def startocr(obj):
    global cmdpid
    # 写入标志，进行中
    with open(os.path.join(rootdir,'status.pid'),'w',encoding="utf-8") as f:
        f.write("staring")
    # cmd = "{pybin}  -i {sourcedir} -o {targetdir} --translator={lang}".format(pybin=pybin,  sourcedir=obj['sourcedir'], targetdir=obj['targetdir'], lang=obj['lang'])
    cmd = "{pybin}  -i {sourcedir} -o {targetdir}  -f {imgformat} --translator={lang} --detector {detector} {heibai} --ocr {ocr} --upscale-ratio {ratio}".format(pybin=pybin,  sourcedir=obj['sourcedir'], targetdir=obj['targetdir'], lang=obj['lang'], imgformat=obj['imgformat'], detector=obj['detector'], heibai=obj['heibai'],ocr=obj['ocr'],ratio=obj['ratio'])
    print(cmd)
    sys.exit()
    if obj['usegpu']:
        cmd += " --use-cuda"

    proc = subprocess.Popen(cmd, bufsize=0, shell=True)
    cmdpid = proc.pid
    print('poll=', proc.pid)  # 因为是 windows 系统，默认编码是 ‘gbk’
    print('开始执行，cmd=%s' % cmd)

# 停止任务
def stopocr(current=""):
    print("停止任务")
    
    # 正常停止
    with open(os.path.join(rootdir,'status.pid'),'w',encoding="utf-8") as f:        
        f.write(current)
    if cmdpid and int(cmdpid) > 0:
        print(os.system("tskill %s" % cmdpid))
    # 关掉所有进程
    pythonlist = os.popen('wmic process where caption="python.exe" get commandline,processid')
    for i in pythonlist.readlines():
        # ocrname 存在 脚本名字的进程关掉
        if i.strip() and ocrname in i:
            i = i.strip().split(" ")
            i = [x for x in i if x != '']
            print('i=', i[-1])
            os.system("tskill %s" % i[-1])


# 根据配置文件 ocr.ini 配置 目录和脚本名
def initrun():
    global rootdir, ocrname, ocrfile, pybin
    if os.path.exists(os.path.join(rootdir, 'ocr.ini')):
        with open(os.path.join(rootdir, 'ocr.ini'), 'r',encoding="utf-8") as f:
            tmp = f.read().strip().split("\n")
            for i in tmp:
                t = i.strip().split("=")
                if t[0] == 'dir':
                    rootdir = t[1]
                elif t[0] == 'file':
                    ocrname = t[1]
                elif t[0] == 'pybin':
                    pybin = t[1]
            ocrfile = os.path.join(rootdir, ocrname)
    if os.path.exists(os.path.join(rootdir, 'run.log')):
        os.unlink(os.path.join(rootdir, 'run.log'))
    if os.path.exists(os.path.join(rootdir, 'status.pid')):
        os.unlink(os.path.join(rootdir, 'status.pid'))


# 显示 run.log 信息，和 status.pid的错误信息
def showlogs():
    global start_time,current_status
    newtime = int(time.time())
    if newtime - start_time > 10:
        start_time = newtime
        if os.path.exists(os.path.join(rootdir, 'run.log')):
            with open(os.path.join(rootdir, 'run.log'), 'r',encoding="utf-8") as f:
                window['loginfo'].update(value=f.read())
        # 查询当前状态
        if current_status=='ing'  and os.path.exists(os.path.join(rootdir,'status.pid')):
            print("=========================")
            with open(os.path.join(rootdir,'status.pid'),'r',encoding="utf-8") as f:
                tmp=f.read().strip()
                # 只有处于执行状态才检测
                if tmp=='stop':
                    # 正常停止
                    current_status='no'
                    stopocr("stop")
                    window['startbtn'].update(text="开始执行")
                    window['loginfo'].update(value="【任务终止】:\n")
                elif tmp=='end':
                    current_status='no'
                    stopocr("end")
                    window['startbtn'].update(text="开始执行")
                    window['loginfo'].update(value="【任务完成】:\n")
                elif tmp!='' and tmp!='staring':
                    # 出错了
                    current_status='no'
                    window['startbtn'].update(text="开始执行")
                    window['loginfo'].update(value="【出错了】:\n%s"%tmp)
        elif os.path.exists(os.path.join(rootdir,'status.pid')):
            with open(os.path.join(rootdir,'status.pid'),'r',encoding="utf-8") as f:
                tmp=f.read().strip()
                if tmp=='stop':
                    # 正常停止

                    window['loginfo'].update(value="【任务被终止】\n")
                elif tmp=='end':
                    window['loginfo'].update(value="【任务完成】\n")



# 初始化各种路径信息
initrun()


window = sg.Window('Zero 漫画翻译', layout, size=(1000, 400), icon=os.path.join(rootdir,"icon.ico"), resizable=True)

while True:
    event, values = window.read(timeout=100)
    # print('event',event)
    # print('values',values)
    # 选择源图片文件夹
    if event == 'sourcedir':
        window['sourceinput'].update(askdirectory())
    elif event=='sourcelang':
        os.environ['sourcelang']=window["sourcelang"].get()
        print("source="+os.getenv("sourcelang"))
    # 选择目标图片文件夹
    elif event == 'targetdir':
        window['targetinput'].update(askdirectory())
        pass
    elif event == 'startbtn':
        # 当前执行中，点击按钮关闭
        if current_status == 'ing':
            stopocr("stop")
            current_status="no"
            window['startbtn'].update(text="开始执行")
        else:
            current_status="ing"
            # 开始执行
            obj = {
                "sourcedir": window['sourceinput'].get(),
                "targetdir": window['targetinput'].get(),
                "lang": window['langinput'].get(),
                "usegpu":window['usegpu'].get(),
                "detector": window['detector'].get(),
                "imgformat":window['imgformat'].get(),
                "ocr":window['ocr'].get(),
                "ratio":window['ratio'].get(),
                "heibai":" "
            }
            if window['heibai'].get()=='yes':
                obj['heibai']=' --colorizer mc2 --colorization-size -1 '
            if not obj['sourcedir']:
                messagebox.showerror('出错了', '必须选择要翻译的图片文件夹',parent=window.TKroot)
                current_status="no"
                continue
            if not os.path.exists(obj['sourcedir']):
                messagebox.showerror('出错了', '你选择的文件夹不存在')
                current_status="no"
                continue
            if not obj['targetdir']:
                obj['targetdir'] = obj['sourcedir'] + "-translated"
            if not obj['lang']:
                obj['lang'] = 'youdao'
            if obj['lang'] not in langobj:
                messagebox.showerror('出错了', '你选择的翻译选项不在有效范围内')
                current_status="no"
                continue
            if "sugoi" in obj['lang']:
                messagebox.showerror('出错了', '该翻译不支持翻译到中文')
                current_status="no"
                continue
            print("开始执行")
            window['startbtn'].update(text="执行中,点击停止")
            startocr(obj)
            window['loginfo'].update(value="开始执行...\n")
    elif event=='up':
        # 升级
        stopocr("stop")
        current_status="no"
        window['startbtn'].update(text="开始执行")
        # 升级
        zip_file = values['zippath']
        if not os.path.exists(zip_file):
            messagebox.showerror("压缩包不存在", message="先去github下载zip包", parent=window.TKroot)
            continue
        else:
            jieya(zip_file)
    elif event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
        print("关闭窗口")
        current_status='no'
        stopocr()
        break
    else:
        # 设置显示的执行路径
        if window['cmddir'].get() == '':
            print('rootdir=', rootdir)
            window['cmddir'].update(value=ocrfile)
        showlogs()

window.close()