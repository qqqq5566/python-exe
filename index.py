from tkinter import *
from downloadFile import Download



root = Tk()
root.geometry("600x300")
root.title("链吧更新")

#root.wm_iconbitmap("chainbar.ico")


if __name__ == '__main__':
    #t = threading.Thread(target=download, name="Download File")
    #t.start()
    #t.join()
    d = Download(root)
    d.createCav()
    mainloop()



