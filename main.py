import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time


def log_write(acc, action):
    try:  # 紀錄"帳號、時間、動作於log.db中"
        conn = sqlite3.connect('log.db')
        conn.execute("""create table if not exists member
                                    (
                                        acc   char(20)  not null,
                                        datetime     char(20)   not null,
                                        action     char(20)  not null
                                    ); """)
        conn.execute("""insert into member(acc, datetime, action)
                    values('{}', '{}', '{}') """.format(acc, time.strftime("%Y-%m-%d %H:%M:%S\
                        ", time.localtime()), action))
        conn.commit()
        conn.close()
    except:
        messagebox.showerror(message="log讀取失敗")


def login():
    acc = entryacc_var.get()
    pwd = entrypwd_var.get()
    conn = sqlite3.connect('admin.db')  # 開啟admin資料庫搜索輸入的帳密是否有在裡面
    cursor = conn.execute('select * from member')
    rows = cursor.fetchall()
    success = False
    role = ""
    for i in rows:
        if (acc == i[1]) and (pwd == i[2]):  # 如果帳密符合
            success = True
            role = i[0]
            global account
            account = i[1]
            log_write(i[1], action="登入")  # 寫入log
            break
    if success:
        messagebox.showinfo(message="登入成功")
        frame1.destroy()  # 摧毀登入畫面
        frame2_form(role, account)  #進入選單畫面
    else:
        messagebox.showerror(message="帳密有誤")
    conn.close()


def logout():
    yes = messagebox.askquestion(message="確定離開嗎?")
    if yes == "yes":
        log_write(account, action="登出")  # 紀錄登出
        frame2.destroy()  # 摧毀所有畫面(也可改pack_forget關閉畫面)
        frame3.destroy()
        frame4.destroy()
        frame5.destroy()
        frame1_form()  # 返回登入畫面


def frame1_form():  # 切換至登入畫面
    form.title('登入帳密')
    global frame1
    frame1 = tk.Frame(form)
    frame1.pack()
    account = tk.Label(frame1, text='帳密：')
    account.grid(row=0, column=0)
    global entryacc_var
    entryacc_var = tk.StringVar()
    entryacc = tk.Entry(frame1, textvariable=entryacc_var)
    entryacc.grid(row=0, column=1)
    password = tk.Label(frame1, text='密碼：')
    password.grid(row=1, column=0)
    global entrypwd_var
    entrypwd_var = tk.StringVar()
    entrypwd = tk.Entry(frame1, textvariable=entrypwd_var)
    entrypwd.grid(row=1, column=1)
    login_button = tk.Button(frame1, text="登入", command=login)  #當登入按鈕按下去時進login()
    login_button.grid(row=2, column=1)


def frame2_form(role, account):  # 切換至選單畫面
    global frame2
    frame2 = tk.Frame(form)  # 由於我將所有畫面做在一個form裡 所以其他計算都各一個畫面
    frame2.pack()
    global frame3
    frame3 = tk.Frame(form)
    global frame4
    frame4 = tk.Frame(form)
    global frame5
    frame5 = tk.Frame(form)

    global comboSex
    if role == "admin":  # 根據帳密的等級有不同的功能
        comboSex = ttk.Combobox(frame2, values=('BMI計算', '最佳體重計算',
                                '觀看log', '離開'))
    elif role == "user":
        comboSex = ttk.Combobox(frame2, values=('BMI計算', '最佳體重計算', '離開'))
    comboSex.grid(row=0, column=0)
    comboSex.bind("<<ComboboxSelected>>", frame_select)  # 將事件綁定在選單上


def frame_select(event):  # 下拉選單的事件觸發，切換選項畫面

    if comboSex.get() == "BMI計算":
        log_write(account, action="BMI計算")  # 每個動作都要寫入log
        frame3.pack()  # 使用pack開啟畫面  pack_forget關閉畫面
        frame4.pack_forget()
        frame5.pack_forget()
        BMI(frame3)
    elif comboSex.get() == "最佳體重計算":
        log_write(account, action="最佳體重計算")
        frame3.pack_forget()
        frame4.pack()
        frame5.pack_forget()
        Best_weight(frame4)
    elif comboSex.get() == "觀看log":
        log_write(account, action="觀看log")
        frame3.pack_forget()
        frame4.pack_forget()
        frame5.pack()
        log_read(frame5)
    elif comboSex.get() == "離開":
        logout()  # 登出


def BMI(frame3):
    form.title("BMI計算")
    # -------------------------
    weight = tk.Label(frame3, text='體重(公斤)：')
    weight.grid(row=1, column=0)
    global entryweight_var
    entryweight_var = tk.StringVar()
    entryweight = tk.Entry(frame3, textvariable=entryweight_var)
    entryweight.grid(row=1, column=1)
    # -------------------------
    height = tk.Label(frame3, text='身高(公尺)：')
    height.grid(row=2, column=0)
    global entryheight_var
    entryheight_var = tk.StringVar()
    entryheight = tk.Entry(frame3, textvariable=entryheight_var)
    entryheight.grid(row=2, column=1)
    # -------------------------
    calc_button = tk.Button(frame3, text="計算", command=BMI_calc)
    calc_button.grid(row=3, column=0)
    calc_button2 = tk.Button(frame3, text="清除", command=BMI_clear)
    calc_button2.grid(row=3, column=1)


def BMI_calc():
    try:
        weight = float(entryweight_var.get())
        height = float(entryheight_var.get())
        if (weight > 0) and (height > 0):
            messagebox.showinfo(message=("您的BMI為", weight / height ** 2))
    except:
        messagebox.showinfo(message=("請輸入正確的數字"))


def BMI_clear():
    entryweight_var.set("")
    entryheight_var.set("")


def Best_weight(frame4):
    form.title("最佳體重計算")
    height = tk.Label(frame4, text='身高(公尺)：')
    height.grid(row=1, column=0)
    global entryheight_var
    entryheight_var = tk.StringVar()
    entryheight = tk.Entry(frame4, textvariable=entryheight_var)
    entryheight.grid(row=1, column=1)
    calc_button = tk.Button(frame4, text="計算", command=Best_weight_calc)
    calc_button.grid(row=2, column=0)
    calc_button2 = tk.Button(frame4, text="清除", command=Best_weight_clear)
    calc_button2.grid(row=2, column=1)


def Best_weight_calc():
    try:
        height = float(entryheight_var.get())
        if (height > 0):
            messagebox.showinfo(message=("您的最佳體重為", 22 * (height ** 2)))
    except:
        messagebox.showinfo(message=("請輸入正確的數字"))


def Best_weight_clear():
    entryheight_var.set("")


def log_read(frame5):  # 用treeview顯示log.db
    tree = ttk.Treeview(frame5, columns=['1', '2', '3'], show='headings')
    tree.column('1', width=100, anchor='center')
    tree.column('2', width=150, anchor='center')
    tree.column('3', width=100, anchor='center')
    tree.heading('1', text='帳號')
    tree.heading('2', text='時間')
    tree.heading('3', text='動作')
    try:  # 依照時間讀取最後20筆log資料
        conn = sqlite3.connect('log.db')
        cursor = conn.execute("""select * from member order by \
            datetime desc limit 20""")
        rows = cursor.fetchall()
        for i in rows:
            tree.insert('', 'end', values=i)  # 把每一筆資料塞進tree
        conn.close()
    except:
        messagebox.showerror(message="log讀取失敗")
    tree.grid()


if __name__ == "__main__":

    conn_build = True
    try:
        with open('accounts.csv', 'r') as f: # 1.讀取CSV建立admin.db
                for line in f:
                    conn = sqlite3.connect('admin.db')
                    line = line.strip('\n')
                    line = line.split(",")
                    if conn_build:
                        conn.execute("""create table if not exists member
                                        (
                                            {0}   char(20)  not null,
                                            {1}     char(20)   not null,
                                            {2}     char(20)  not null
                                        ); """.format(line[0], line[1], line[2]))
                        conn.commit()
                        conn_build = False  # 2.conn_build以讓第一筆紀錄為資料表的欄位名稱
                    else:                   # 之後的才是資料
                        conn.execute("""insert into member(role, acc, pwd)
                        values('{}', '{}', '{}') """.format(line[0], line[1],
                                                            line[2]))
                        conn.commit()
                # cursor = conn.execute('select * from member')  #查看資料庫內容
                # rows = cursor.fetchall()
                # print(rows)
                conn.close()
    except Exception as e:
        messagebox.showerror(message=("讀取失敗 原因: ", e))

    form = tk.Tk()
    form.geometry('400x400+50+100')
    frame1_form()  # 3.進入登入畫面
    frame1.mainloop()