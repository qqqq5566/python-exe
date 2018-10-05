import requests
from getVersion import getDiff
import configparser
import os
from tkinter import *
from tkinter import ttk
import queue, threading
import time
class Download:
    __url = ""
    __config = None
    totaFileSize = 0  #文件的总大小
    fileTmpSize = 0
    flag = False
    __root = None
    fill_rec = ''
    canvas = None
    def __init__(self, root):
        self.__url = "http://test.chain-bar.com/jic/package/exe/"
        self.__root = root
        if getDiff():
            self.updatetext = StringVar()
            self.downloadIni("updateConfig.ini")
            path = os.getcwd()
            # if os.access("/usr/local", os.W_OK):
            #    print(11)
            # else:
            #    exit()
            print("完成")
        else:
            exit()

    def downloadIni(self, filename):
        """下载配置文件"""
        r = requests.get(self.__url+filename)

        with open('1.ini', 'wb') as f:
            f.write(r.content)
        self.getConfig()


    def downloadFile(self, fileName):
        """下载更新文件"""
        r1 = requests.get(self.__url + fileName, stream=True) #第一次请求获取大小
        totalSize = int(r1.headers['content-length'])

        if os.path.exists(fileName):
            temp_size = os.path.getsize(fileName)
        else:
            temp_size = 0
        print(temp_size)
        #self.fileTmpSize +=temp_size
        print(totalSize)
        try:
            headers = {'Range': 'bytes=%d-' % temp_size}
            r = requests.get(self.__url+fileName, stream=True, headers=headers)

            #中要
            with open(fileName, 'ab') as f:
                for chunk in r.iter_content(1024*1024):
                    print(1)
                    if chunk:
                        f.write(chunk)
                        temp_size += len(chunk)
                        f.flush()
                        self.fileTmpSize += len(chunk)
                        print("下载大小:--%d" % self.fileTmpSize)
                        self.thread_queue.put((self.fileTmpSize/self.totaFileSize)*100)
        except:
            self.downloadFile(fileName)
        if temp_size != totalSize:
            self.downloadFile(fileName)

        print()

    def createDir(self):
        pass

    def getConfig(self):
        """获取配置对象"""
        self.__config = configparser.ConfigParser()
        self.__config.read("1.ini")


    def readConfig(self):
        """读取更新文件"""
        count = self.__config.getint("XML", 'count')
        self.getFileTotalSize()
        if count > 0:
            for i in range(1, count+1):
                fileName = self.__config.get("XML", 'file_'+str(i))
                if os.path.exists(fileName):
                    os.remove(fileName)
                else:
                    dirPath = os.path.split(fileName)
                    if dirPath[0]:
                        if not os.path.exists(dirPath[0]):
                            os.makedirs(dirPath[0])
                print(fileName)
                t = threading.Thread(target=self.downloadFile,args=(fileName,))
                t.start()
                t.join()
                #self.downloadFile(fileName)
        self.flag = True

    def getFileTotalSize(self):
        """获取文件的总大小"""
        count = self.__config.getint("XML", 'count')

        if count > 0:
            for i in range(1, count + 1):
                fileSize = self.__config.getint("SIZE", 'file_' + str(i))
                self.totaFileSize +=fileSize
            print("总大小--%d" % self.totaFileSize)
    def createCav(self):
        self.strvar=StringVar()
        label = Label(self.__root, textvariable=self.strvar)
        label.pack()
        self.progress =IntVar()
        self.progress_max = 100
        self.progressbar = ttk.Progressbar(self.__root, mode='determinate', orient=HORIZONTAL, variable=self.progress,
                                       maximum=self.progress_max)
        self.progressbar.pack(fill=X, expand=True)
        self.progress.set(0)
        self.thread_queue = queue.Queue()
        t = threading.Thread(target=self.run_loop, name="update processbar")
        #self.readConfig()
        t.start()
        #t.join()
        self.__root.after(100, self.listen_for_result)
    # 更新进度条函数
    def run_loop(self):
        progress = 0
        self.strvar.set("正在更新，请稍后...")
        self.readConfig()


    def listen_for_result(self):
        '''
        Check if there is something in the queue.
        Must be invoked by self.root to be sure it's running in main thread
        '''
        try:
            progress = self.thread_queue.get(False)
            self.progress.set(progress)
        except queue.Empty:  # must exist to avoid trace-back
            pass
        finally:
            if self.progress.get() < self.progressbar['maximum']:
                self.__root.after(100, self.listen_for_result)
            elif self.progressbar['maximum'] == 100:
                self.strvar.set("更新完毕，请重启")
                time.sleep(5)
                sys.exit(1)




if __name__ == '__main__':
    if getDiff():
        d = Download()
        d.downloadIni("updateConfig.ini")
        path = os.getcwd()
        #if os.access("/usr/local", os.W_OK):
        #    print(11)
        #else:
        #    exit()
        d.readConfig()
        print("完成")
    else:
        exit()
