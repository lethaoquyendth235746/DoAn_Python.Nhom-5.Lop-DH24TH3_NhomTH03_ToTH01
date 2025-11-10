import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import os

# ==================== HÀM KẾT NỐI DATABASE ====================
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="071005",  # điền mật khẩu DB
            database="qlbenhnhan"
        )
        return conn
    except Exception as e:
        tk.messagebox.showerror("Lỗi Database", str(e))
        return None

# ==================== HÀM CHECK LOGIN ====================
def check_login(entry_username, entry_password, login_root, main_root, remember_var, remember_file="remember.txt"):
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showwarning("Lỗi Đăng Nhập", "Vui lòng nhập đầy đủ Tên người dùng và Mật khẩu.")
        return

    conn = connect_db()
    if conn is None:
        return

    cur = conn.cursor()
    try:
        cur.execute("SELECT tentaikhoan FROM taikhoan WHERE tentaikhoan=%s AND matkhau=%s", (username, password))
        result = cur.fetchone()

        if result:
            if remember_var.get():
                with open(remember_file, "w") as f:
                    f.write(f"{username}\n{password}")
            else:
                if os.path.exists(remember_file):
                    os.remove(remember_file)

            messagebox.showinfo("Đăng nhập thành công", f"Chào mừng {username}!")
            login_root.destroy()
            main_root.deiconify()
        else:
            messagebox.showerror("Lỗi Đăng Nhập", "Tên người dùng hoặc Mật khẩu không đúng.")
            entry_password.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Lỗi Database", str(e))
    finally:
        conn.close()


# ==================== HÀM ĐĂNG KÝ ====================
def register_user(entry_username, entry_password):
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showwarning("Đăng ký", "Vui lòng nhập đầy đủ Tên người dùng và Mật khẩu.")
        return

    conn = connect_db()
    if conn is None:
        return

    cur = conn.cursor()
    try:
        cur.execute("SELECT tentaikhoan FROM taikhoan WHERE tentaikhoan=%s", (username,))
        if cur.fetchone():
            messagebox.showerror("Đăng ký", "Tên tài khoản đã tồn tại!")
            return

        cur.execute("INSERT INTO taikhoan(tentaikhoan, matkhau) VALUES(%s, %s)", (username, password))
        conn.commit()
        messagebox.showinfo("Đăng ký", "Đăng ký thành công! Bạn có thể đăng nhập ngay.")
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Lỗi Database", str(e))
    finally:
        conn.close()


# ==================== HÀM QUÊN MẬT KHẨU ====================
def reset_password(entry_username):
    username = entry_username.get()
    if not username:
        messagebox.showwarning("Quên mật khẩu", "Nhập tên đăng nhập cần lấy lại mật khẩu.")
        return
    # Demo: chỉ thông báo, bạn có thể thay bằng gửi email hoặc reset password trong DB
    messagebox.showinfo("Quên mật khẩu", f"Tài khoản '{username}' yêu cầu reset mật khẩu.\nLiên hệ admin để đặt lại mật khẩu.")


# ==================== HÀM HIỂN THỊ LOGIN ====================
def show_login_window(main_root, center_window_func, color_fg):
    login_root = tk.Toplevel(main_root)
    login_root.title("Đăng Nhập Hệ Thống")
    center_window_func(login_root, w=700, h=350)
    login_root.resizable(False, False)
    login_root.grab_set()

    BG_COLOR = "#e6f5ff"
    FRAME_COLOR = "#ffffff"
    COLOR_MAIN = "#a80000"

    # Frame tổng chia 2
    frame_main = tk.Frame(login_root, bg=BG_COLOR)
    frame_main.pack(fill="both", expand=True)

    # --- Bên trái: hình ảnh ---
    frame_left = tk.Frame(frame_main, bg=BG_COLOR, width=300, height=350)
    frame_left.pack(side="left", fill="both")
    frame_left.pack_propagate(False)
    try:
        image = Image.open("benhvien.png")
        image = image.resize((300, 300), Image.LANCZOS)
        img = ImageTk.PhotoImage(image)
        lbl_img = tk.Label(frame_left, image=img, bg=BG_COLOR)
        lbl_img.image = img
        lbl_img.pack(expand=True)
    except:
        lbl_img = tk.Label(frame_left, text="(Không tìm thấy ảnh)", bg=BG_COLOR, fg="gray",
                           font=("Times New Roman", 12))
        lbl_img.pack(expand=True)

    # --- Bên phải: form ---
    frame_right = tk.Frame(frame_main, bg=FRAME_COLOR, padx=20, pady=20)
    frame_right.pack(side="right", fill="both", expand=True)

    lbl_title = tk.Label(frame_right, text="ĐĂNG NHẬP", font=("Times New Roman", 20, "bold"), bg=FRAME_COLOR, fg=COLOR_MAIN)
    lbl_title.pack(pady=10)

    form_frame = tk.Frame(frame_right, bg=FRAME_COLOR)
    form_frame.pack(pady=5)

    label_style = {"font": ("Times New Roman", 13), "bg": FRAME_COLOR, "fg": "black"}

    tk.Label(form_frame, text="Tên đăng nhập", **label_style).grid(row=0, column=0, pady=5, padx=5, sticky="e")
    entry_username = tk.Entry(form_frame, width=25, font=("Times New Roman", 12))
    entry_username.grid(row=0, column=1, pady=5, padx=5)

    tk.Label(form_frame, text="Mật khẩu", **label_style).grid(row=1, column=0, pady=5, padx=5, sticky="e")
    entry_password = tk.Entry(form_frame, width=25, show="*", font=("Times New Roman", 12))
    entry_password.grid(row=1, column=1, pady=5, padx=5)

    # Nhớ mật khẩu
    remember_var = tk.BooleanVar()
    tk.Checkbutton(form_frame, text="Nhớ mật khẩu", variable=remember_var, bg=FRAME_COLOR).grid(row=2, column=1, sticky="w")

    # Load nếu có
    remember_file = "remember.txt"
    if os.path.exists(remember_file):
        with open(remember_file, "r") as f:
            lines = f.read().splitlines()
            if len(lines) >= 2:
                entry_username.insert(0, lines[0])
                entry_password.insert(0, lines[1])
                remember_var.set(True)

    # Buttons
        # ======== Frame chứa 2 nút ngang hàng ========
    btn_frame = tk.Frame(frame_right, bg=FRAME_COLOR)
    btn_frame.pack(pady=10)

    btn_login = tk.Button(btn_frame, text="ĐĂNG NHẬP", width=12, 
                        bg="#007ACC", fg="white",  
                        font=("Times New Roman", 13, "bold"),
                        command=lambda: check_login(entry_username, entry_password, login_root, main_root, remember_var))
    btn_login.grid(row=0, column=0, padx=(0,5))  # khoảng cách giữa 2 nút

    btn_register = tk.Button(btn_frame, text="ĐĂNG KÝ", width=12, 
                            bg="#007ACC", fg="white",  
                            font=("Times New Roman", 13, "bold"),
                            command=lambda: register_user(entry_username, entry_password))
    btn_register.grid(row=0, column=1, padx=(5,0))
    lbl_reset = tk.Label(frame_right, text="Quên mật khẩu?", fg="blue", cursor="hand2",
                        font=("Times New Roman", 12, "underline"), bg=FRAME_COLOR)
    lbl_reset.pack()
    lbl_reset.bind("<Button-1>", lambda e: reset_password(entry_username))


        # Enter để đăng nhập
    entry_password.bind('<Return>', lambda e: check_login(entry_username, entry_password, login_root, main_root, remember_var))

    # Xử lý đóng cửa sổ login
    login_root.protocol("WM_DELETE_WINDOW", main_root.quit)
