import tkinter
import win32api,win32con
from tkinter import filedialog
import Logic

class GUI:

    def __init__(self):
        self.lg = Logic.SongFileReplace()

        self.getScreenRes()
        self.windowWidth=600
        self.windowHeight=300
        self.createRoot()
        self.frame = tkinter.Frame(self.root)
        self.frame.pack()
        self.setList(self.lg.getOutputs())
        self.scene1()
        self.root.mainloop()

    def setList(self,list):
        self.li = list

    def getScreenRes(self):
        self.screenWidth = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)  # 获得屏幕分辨率X轴
        self.screenHeight = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)  # 获得屏幕分辨率Y轴

    def createRoot(self):
        self.root = tkinter.Tk()
        self.root.title("test")
        self.root.geometry("%sx%s+%s+%s" % (self.windowWidth,self.windowHeight,int(self.screenWidth / 2-self.windowWidth/2) , int(self.screenHeight / 2-self.windowHeight/2)))

    def scene1(self):

        self.v = tkinter.IntVar()
        lb = tkinter.Label(self.frame, text='选择要替换的歌曲：', fg='blue')
        lb.pack()
        for i, x in enumerate(self.li):
            button = tkinter.Radiobutton(self.frame, text=x, variable=self.v, value=i)
            button.pack()
        B = tkinter.Button(self.frame, text="确认歌曲", command=self.confirmSongButton)
        B.pack()


    def confirmSongButton(self):
        self.lg.setTargetxmlNode(self.v.get())
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.scene2()

    def browseFile(self):
        self.filePath.set(filedialog.askopenfilename())

    def confirmModification(self):

        try:
            self.lg.setSourceFilePath(self.filePath.get())
        except:
            win32api.MessageBox(0, "无效歌曲文件地址！", "警告", win32con.MB_ICONWARNING)
            return -1

        try:
            self.lg.modDesiredScore(self.entries[0].get())
        except:
            self.lg.modDesiredScore(self.lg.getMaxScore(self.lg.targetxmlNode))

        try:
            self.lg.modDesiredRank(self.entries[1].get())
        except:
            self.lg.modDesiredRank(6)

        self.lg.modifyFileSize(self.lg.targetxmlNode)

        self.lg.finalPhase()
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.scene3()


    def scene2(self):
        self.entries = []
        self.filePath = tkinter.StringVar()

        tkinter.Label(self.frame,text="选择准备用来替换的歌曲").grid(row=0,column=0,columnspan=3,pady=20)
        tkinter.Entry(self.frame,textvariable=self.filePath).grid(row=1,column=0,columnspan=5,ipadx=120,pady=10)
        tkinter.Button(self.frame,text="浏览",command=self.browseFile).grid(row=1,column=5,pady=10)

        tkinter.Label(self.frame,text="输入分数").grid(row=2,column=0,pady=10)
        e=tkinter.Entry(self.frame)
        e.grid(row=2,column=1,pady=10)
        tkinter.Label(self.frame, text="本首歌最高分为%s"%(self.lg.getMaxScore(self.lg.targetxmlNode)),fg="red").grid(row=2, column=2, pady=10)
        self.entries.append(e)

        tkinter.Label(self.frame, text="输入评级").grid(row=3, column=0,pady=10)
        e = tkinter.Entry(self.frame)
        e.grid(row=3, column=1,pady=10)
        tkinter.Label(self.frame, text="共1~6六个等级，依次从C提升到SSS", fg="red").grid(row=3,column=2,pady=10)
        self.entries.append(e)

        tkinter.Button(self.frame, text="确认修改", command=self.confirmModification).grid(row=4, column=0, columnspan=3,pady=10)

    def destroyButton(self):
        self.root.destroy()

    def scene3(self):
        tkinter.Label(self.frame, text="修改及替换完成\n现可以关闭修改器\n打开全民k歌上传").grid(row=0,pady=50)
        tkinter.Button(self.frame, text="退出", command=self.destroyButton).grid(row=1,ipadx=5,ipady=5)


def main():
    gui=GUI()

main()

