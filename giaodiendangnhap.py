import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # pip install pillow

# ==================== HÀM KIỂM TRA ĐĂNG NHẬP ====================
def check_login(entry_username, entry_password, login_root, main_root, connect_db_func):
    """Kiểm tra thông tin đăng nhập với MySQL."""
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showwarning("Lỗi Đăng Nhập", "Vui lòng nhập đầy đủ Tên người dùng và Mật khẩu.")
        return

    conn = connect_db_func()
    if conn is None:
        return

    cur = conn.cursor()
    try:
        query = "SELECT tentaikhoan FROM taikhoan WHERE tentaikhoan = %s AND matkhau = %s"
        cur.execute(query, (username, password))
        result = cur.fetchone()

        if result:
            messagebox.showinfo("Đăng nhập thành công", f"Chào mừng {username}!")
            login_root.destroy()
            main_root.deiconify()  # Hiện giao diện chính
        else:
            messagebox.showerror("Lỗi Đăng Nhập", "Tên người dùng hoặc Mật khẩu không đúng.")
            entry_password.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Lỗi Database", str(e))
    finally:
        conn.close()


# ==================== HÀM HIỂN THỊ CỬA SỔ LOGIN ====================
def show_login_window(main_root, connect_db_func, center_window_func, color_fg):
    """Khởi tạo và hiển thị cửa sổ Đăng nhập (giao diện chia 2 cột)."""
    login_root = tk.Toplevel(main_root)
    login_root.title("Đăng Nhập Hệ Thống")

    # --- Cấu hình kích thước ---
    window_width = 700
    window_height = 350
    center_window_func(login_root, w=window_width, h=window_height)
    login_root.resizable(False, False)
    login_root.grab_set()

    BG_COLOR = "#e6f5ff"  # nền hồng nhạt
    FRAME_COLOR = "#ffffff"
    COLOR_MAIN = "#a80000"

    # --- Frame tổng chia 2 phần ---
    frame_main = tk.Frame(login_root, bg=BG_COLOR)
    frame_main.pack(fill="both", expand=True)

    # --- Khung bên trái (hình ảnh) ---
    frame_left = tk.Frame(frame_main, bg=BG_COLOR, width=300, height=350)
    frame_left.pack(side="left", fill="both")
    frame_left.pack_propagate(False)

    try:
        image = Image.open("benhvien.png")  # 🔸 Đặt tên ảnh của bạn vào đây
        image = image.resize((300, 300), Image.LANCZOS)
        img = ImageTk.PhotoImage(image)
        lbl_img = tk.Label(frame_left, image=img, bg=BG_COLOR)
        lbl_img.image = img
        lbl_img.pack(expand=True)
    except:
        lbl_img = tk.Label(frame_left, text="(Không tìm thấy ảnh)", bg=BG_COLOR, fg="gray",
                           font=("Times New Roman", 12))
        lbl_img.pack(expand=True)

    # --- Khung bên phải (form đăng nhập) ---
    frame_right = tk.Frame(frame_main, bg=FRAME_COLOR, padx=20, pady=20)
    frame_right.pack(side="right", fill="both", expand=True)

    lbl_title = tk.Label(frame_right, text="ĐĂNG NHẬP",
                         font=("Times New Roman", 20, "bold"),
                         bg=FRAME_COLOR, fg=COLOR_MAIN)
    lbl_title.pack(pady=10)

    form_frame = tk.Frame(frame_right, bg=FRAME_COLOR)
    form_frame.pack(pady=15)

    label_style = {"font": ("Times New Roman", 13), "bg": FRAME_COLOR, "fg": "black"}

    tk.Label(form_frame, text="Tên đăng nhập", **label_style).grid(row=0, column=0, pady=8, padx=5, sticky="e")
    entry_username = tk.Entry(form_frame, width=25, font=("Times New Roman", 12))
    entry_username.grid(row=0, column=1, pady=8, padx=5)

    tk.Label(form_frame, text="Mật khẩu", **label_style).grid(row=1, column=0, pady=8, padx=5, sticky="e")
    entry_password = tk.Entry(form_frame, width=25, show="*", font=("Times New Roman", 12))
    entry_password.grid(row=1, column=1, pady=8, padx=5)

    # --- Nút đăng nhập ---
    btn_login = tk.Button(frame_right, text="ĐĂNG NHẬP", width=18,
                          font=("Times New Roman", 13, "bold"),
                          bg="#003366", fg="white",
                          command=lambda: check_login(entry_username, entry_password, login_root, main_root, connect_db_func))
    btn_login.pack(pady=20)

    # Nhấn Enter để đăng nhập
    entry_password.bind('<Return>', lambda event: check_login(entry_username, entry_password, login_root, main_root, connect_db_func))

    # Đóng cửa sổ login => thoát chương trình
    login_root.protocol("WM_DELETE_WINDOW", main_root.quit)
