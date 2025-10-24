import tkinter as tk
from tkinter import ttk,messagebox
from tkcalendar import DateEntry
import mysql.connector
# Kết nối đến cơ sở dữ liệu MySQL
def connect_db():
    try:
        # Thay thế các giá trị bên dưới bằng thông tin MySQL của bạn
        conn = mysql.connector.connect(
            host="localhost",
            user="root",          
            password="071005",          
            database="qlbenhnhan" 
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi Kết Nối Database", f"Không thể kết nối đến MySQL: {err}")
        return None
# Hàm canh giữa cửa sổ
def center_window(win, w=900,h=600):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws//2) - (w//2)
    y=(hs//2) - (h//2)
    win.geometry(f'{w}x{h}+{x}+{y}')
# Cửa sổ chính
root=tk.Tk()
root.title("Quản lý bệnh nhân")
center_window(root,900,600)
root.resizable(False,False)
# Định nghĩa các màu sắc bạn muốn
COLOR_RED_TITLE = "red"
COLOR_LIGHT_RED_BG = "#F9F9F9" 
COLOR_DARK_RED_FG = "#E21C1C"  
OLOR_PASTEL_RED_BG = "#F6C8C8"
#Tiêu đề
lbl_title=tk.Label(root,text="QUẢN LÝ BỆNH NHÂN",font=("Times New Roman",18,"bold"),fg=COLOR_DARK_RED_FG)
lbl_title.pack(pady=10)
# Frame nhập thông tin
frame_info=tk.Frame(root)
frame_info.pack(pady=5,padx=10,fill="x")

tk.Label(frame_info, text="Mã số bệnh nhân",fg=COLOR_DARK_RED_FG,font=("Times New Roman",13,"bold")).grid(row=0,column=0,padx=5,pady=5,sticky="w")
entry_maso=tk.Entry(frame_info,width=15)
entry_maso.grid(row=0,column=1,padx=5,pady=5,sticky="w")

tk.Label(frame_info, text="Họ và tên", fg=COLOR_DARK_RED_FG,font=("Times New Roman",13,"bold")).grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_holot = tk.Entry(frame_info, width=40)
entry_holot.grid(row=1, column=1, columnspan=3 ,padx=5, pady=5, sticky="w")

gender_var= tk.StringVar(value="Nam")
tk.Label(frame_info,text="Phái",fg=COLOR_DARK_RED_FG,font=("Times New Roman",13,"bold")).grid(row=2,column=0,padx=5,pady=5,sticky="w")
tk.Radiobutton(frame_info,text="Nam",variable=gender_var,value="Nam",fg=COLOR_DARK_RED_FG ,font=("Times New Roman",13,"bold")).grid(row=2,column=1,padx=5,sticky="w")
tk.Radiobutton(frame_info,text="Nữ",variable=gender_var,value="Nữ",fg=COLOR_DARK_RED_FG,font=("Times New Roman",13,"bold")).grid(row=2,column=1,padx=80,sticky="w")

tk.Label(frame_info,text="Ngày sinh",fg=COLOR_DARK_RED_FG,font=("Times New Roman",13,"bold")).grid(row=0,column=2,padx=(90,5),pady=5,sticky="w")
date_entry_ns=DateEntry(frame_info,width=12,background="darkblue",foreground="white",date_pattern="dd-mm-yyyy")
date_entry_ns.grid(row=0,column=3,padx=(5,5),pady=5,sticky="w")

tk.Label(frame_info,text="Địa chỉ",fg=COLOR_DARK_RED_FG,font=("Times New Roman",13,"bold")).grid(row=1,column=2,padx=(90,5),pady=5,sticky="w")
entry_diachi=tk.Entry(frame_info,width=55)
entry_diachi.grid(row=1, column=3, padx=5, pady=5, sticky="w")
# chạy
root.mainloop()
#x

