import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # cần cài: pip install pillow
#from quanlibenhnhan import 
import mysql.connector # Cần thêm dòng này
from quanlibenhnhan import create_quanlybenhnhan, connect_db, center_window # Import hàm cần thiết

from giaodiendangnhap import show_login_window # Import hàm hiển thị login
#show_login_window(root, connect_db, center_window, "#e60073")


from quanlibacsi import QuanLyBacSi
from quanlikhoa import QuanLyKhoa
from quanliphong import QuanLyPhong  
from quanlidichvu import QuanLyDichVu  
from nhapvien import QuanLyNhapVien 
from quanlithanhtoan import QuanLyThanhToan
from thongke import ThongKeHoaDon




def dangnhap_click():
    """Xử lý nút Đăng nhập: Mở lại cửa sổ login."""
    # COLOR_DARK_RED_FG phải được định nghĩa ở phạm vi global hoặc truyền vào (Xem Bước 2)
    show_login_window(root, connect_db, center_window, "#E21C1C")


from tkinter import Toplevel
from quanlibenhnhan import create_quanlybenhnhan  # đổi tên hàm nếu em đang dùng khác

def open_benhnhan_form():
    """Ẩn form chính và mở form Quản lý bệnh nhân"""
    root.withdraw()  # ẩn form chính

    # Tạo cửa sổ con
    child_window = Toplevel()
    create_quanlybenhnhan(child_window)  # gọi giao diện quản lý bệnh nhân từ file quanlibenhnhan.py

    # Khi đóng form con, hiện lại form chính
    def on_close():
        child_window.destroy()
        root.deiconify()  # hiện lại form chính

    child_window.protocol("WM_DELETE_WINDOW", on_close)


def thoat():
    if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn thoát không?"):
        root.destroy()


def gioithieu():
    messagebox.showinfo(
        "Giới thiệu phần mềm",
        "🏥 PHẦN MỀM QUẢN LÝ BỆNH NHÂN 🏥\n\n"
        "Nhóm thực hiện: Nhóm 5 - Lớp DH24TH3 - Tổ TH01\n"
        "Trường: Đại học An Giang\n\n"
        "Mục tiêu:\n"
        "- Hỗ trợ quản lý bệnh nhân, bác sĩ, khoa, phòng, dịch vụ\n"
        "- Quản lý hóa đơn và thanh toán tiện lợi\n"
        "- Thống kê nhanh các dịch vụ và doanh thu\n\n"
        "Chúc các bạn sử dụng phần mềm hiệu quả!"
    )

def open_bacsi_form():
    root.withdraw()
    child = tk.Toplevel()
    child.title("Quản lý bác sĩ")
    child.geometry("1100x650")  
    app = QuanLyBacSi(child, connect_db, root)  # truyền root vào
    app.pack(fill="both", expand=True)

    def on_close():
        child.destroy()
        root.deiconify()
    child.protocol("WM_DELETE_WINDOW", on_close)

# trong file giao diện chính
def open_khoa_form():
    root.withdraw()             # ẩn form chính
    child = tk.Toplevel()
    child.geometry("1100x650")         # tạo cửa sổ con
    app = QuanLyKhoa(child, connect_db, root)
    app.pack(fill="both", expand=True)

    def on_close():             # xử lý nút X
        child.destroy()
        root.deiconify()
    child.protocol("WM_DELETE_WINDOW", on_close)
def open_phong_form():
    """Ẩn form chính và mở form Quản lý phòng"""
    root.withdraw()  # ẩn form chính
    child = tk.Toplevel()
    child.geometry("1100x650")  
    child.title("Quản lý phòng")
    app = QuanLyPhong(child, connect_db)  # truyền connect_db
    app.pack(fill="both", expand=True)

    def on_close():
        child.destroy()
        root.deiconify()  # hiện lại form chính

    child.protocol("WM_DELETE_WINDOW", on_close)
def open_dichvu_form():
    root.withdraw()  # ẩn form chính
    child = tk.Toplevel()
    child.title("Quản lý Dịch vụ")
    child.geometry("1100x650")  # thêm nếu muốn kích thước cố định
    app = QuanLyDichVu(child, connect_db, parent_root=root)
    app.pack(fill="both", expand=True)

    def on_close():
        child.destroy()
        root.deiconify()

    child.protocol("WM_DELETE_WINDOW", on_close)
def open_nhapvien_form():
    root.withdraw()  # ẩn form chính
    child = tk.Toplevel()
    child.title("Quản lý Nhập viện")
    child.geometry("1100x650")
    app = QuanLyNhapVien(child, connect_db)
    app.pack(fill="both", expand=True)

    def on_close():
        child.destroy()
        root.deiconify()  # hiện lại form chính khi đóng form con

    child.protocol("WM_DELETE_WINDOW", on_close)

def open_thanhtoan_form():
    root.withdraw()  # ẩn form chính
    child = tk.Toplevel()
    child.title("Quản lý Thanh toán")
    child.geometry("1100x650")

    app = QuanLyThanhToan(child, connect_db, parent_root=root)  # truyền root vào
    app.pack(fill="both", expand=True)




def open_thongke_form():
    root.withdraw()  # ẩn form chính
    ThongKeHoaDon(root, connect_db)


root = tk.Tk()
root.title("QUẢN LÝ BỆNH NHÂN")
root.geometry("1100x650")
root.resizable(False, False)

menubar = tk.Menu(root)
root.config(menu=menubar)

COLOR_DARK_RED_FG = "#E21C1C"

# Tạo menu "Hệ thống"

# Hàm thoát chương trình
def thoat_chuongtrinh():
    if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn thoát chương trình không?"):
        root.destroy()  # đóng toàn bộ ứng dụng

# Thêm button Thoát vào menu


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

#tk.Button(menu_frame, text="📝  Bệnh nhân",command= open_quanlybenhnhan, **style).pack(pady=5)
tk.Button(menu_frame, text="📝  Bệnh nhân", command=open_benhnhan_form, **style).pack(pady=5)

tk.Button(menu_frame, text="📋  Nhập viên", command=open_nhapvien_form, **style).pack(pady=5)
tk.Button(menu_frame, text="👨‍⚕️  Bác sĩ",command=open_bacsi_form, **style).pack(pady=5)
tk.Button(menu_frame, text="🏥  Khoa",command=open_khoa_form, **style).pack(pady=5)
tk.Button(menu_frame, text="👩‍💼  Phòng",command=open_phong_form, **style).pack(pady=5)
tk.Button(menu_frame, text="📋  Dịch Vụ",command=open_dichvu_form, **style).pack(pady=5)
tk.Button(menu_frame, text="📋  Thanh toán", command=open_thanhtoan_form, **style).pack(pady=5)

tk.Button(menu_frame, 
          text="🗂️  Thống kê", 
          command=open_thongke_form, 
          **style).pack(pady=5)




tk.Button(menu_frame, text="❓  Giới thiệu", command=gioithieu,
          bg="#0059b3", fg="white", font=("Times New Roman", 13, "bold"),
          width=22, height=2).pack(pady=10)
tk.Button(menu_frame, text="❌  Thoát", command=thoat_chuongtrinh,
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



root.withdraw()
root.protocol("WM_DELETE_WINDOW", root.quit)
#show_login_window(root, connect_db, center_window, COLOR_DARK_RED_FG)
show_login_window(root, center_window, COLOR_DARK_RED_FG)

root.mainloop()
