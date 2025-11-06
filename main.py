import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # cần cài: pip install pillow
from quanlibenhnhan import open_quanlybenhnhan


def dangnhap():
    messagebox.showinfo("Thông báo", "Mở cửa sổ Đăng nhập...")

def dangxuat():
    messagebox.showinfo("Thông báo", "Bạn đã đăng xuất!")
def thoat():
    if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn thoát không?"):
        root.destroy()

def gioithieu():
    messagebox.showinfo("Giới thiệu", 
                        "PHẦN MỀM QUẢN LÝ BỆNH VIỆN\n"
                        "Nhóm 5 - Lớp DH24TH3 - Tổ TH01\n"
                        "Trường Đại học An Giang")

root = tk.Tk()
root.title("QUẢN LÝ BỆNH NHÂN")
root.geometry("1100x650")
root.resizable(False, False)

menubar = tk.Menu(root)
root.config(menu=menubar)

# Tạo menu "Hệ thống"
hethong_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Hệ thống", menu=hethong_menu)

# Thêm các mục con vào menu "Hệ thống"
hethong_menu.add_command(label="🔑 Đăng nhập", command=dangnhap)
hethong_menu.add_command(label="🔒 Đăng xuất", command=dangxuat)
hethong_menu.add_separator() 
hethong_menu.add_command(label="❓ Giới thiệu", command=gioithieu) 
hethong_menu.add_command(label="🚪 Thoát", command=thoat)

# ======== ẢNH NỀN ========
bg_image = Image.open("benhvien.png")
bg_image = bg_image.resize((1100, 650))
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# ======== KHUNG MENU ========
menu_frame = tk.Frame(root, bg="#003366", width=250, height=650)
menu_frame.place(x=0, y=0)

title = tk.Label(menu_frame, text="CHỨC NĂNG", 
                 fg="white", bg="#003366", font=("Times New Roman", 16, "bold"))
title.pack(pady=20)

style = {"font": ("Times New Roman", 13, "bold"), 
         "fg": "white", "bg": "#0059b3", "activebackground": "#1E90FF",
         "width": 22, "height": 2, "bd": 0, "relief": "flat"}

tk.Button(menu_frame, text="📝  Bệnh nhân",command= open_quanlybenhnhan, **style).pack(pady=5)
tk.Button(menu_frame, text="📋  Nhập viên", **style).pack(pady=5)
tk.Button(menu_frame, text="👨‍⚕️  Bác sĩ", **style).pack(pady=5)
tk.Button(menu_frame, text="🏥  Khoa", **style).pack(pady=5)
tk.Button(menu_frame, text="👩‍💼  Phòng", **style).pack(pady=5)
tk.Button(menu_frame, text="📋  Thuốc", **style).pack(pady=5)
tk.Button(menu_frame, text="📋  Thanh toán", **style).pack(pady=5)
tk.Button(menu_frame, text="🗂️  Thống kê", **style).pack(pady=5)

tk.Button(menu_frame, text="❓  Giới thiệu", command=gioithieu,
          bg="#EE2222", fg="white", font=("Times New Roman", 13, "bold"),
          width=22, height=2).pack(pady=10)



# ======== TIÊU ĐỀ ========
title_text = tk.Label(root, text="QUẢN LÝ BỆNH NHÂN",
                      font=("Times New Roman", 20, "bold"),
                      fg="darkred", bg="white")
title_text.place(x=500, y=10)

author = tk.Label(root, text="Nhóm 5 - Lớp DH24TH3 - Tổ TH01",
                  font=("Times New Roman", 12, "italic"), bg="white", fg="gray")
author.place(x=850, y=600)

root.mainloop()
