import tkinter as tk
from tkinter import messagebox

# Không cần import mysql.connector ở đây, sẽ dùng hàm connect_db từ file chính

def check_login(entry_username, entry_password, login_root, main_root, connect_db_func):
    """Kiểm tra thông tin đăng nhập với MySQL."""
    username = entry_username.get()
    password = entry_password.get()
    
    if not username or not password:
        messagebox.showwarning("Lỗi Đăng Nhập", "Vui lòng nhập đầy đủ Tên người dùng và Mật khẩu.")
        return

    # Sử dụng hàm connect_db được truyền từ file chính
    conn = connect_db_func() 
    if conn is None: return

    cur = conn.cursor()
    try:
        # Truy vấn kiểm tra username và password
        query = "SELECT tentaikhoan FROM taikhoan WHERE tentaikhoan = %s AND matkhau = %s"
        cur.execute(query, (username, password))
        result = cur.fetchone()

        if result:
            login_root.destroy() # Đóng cửa sổ Login
            main_root.deiconify() # Hiển thị cửa sổ chính Quản lý Bệnh nhân
        else:
            messagebox.showerror("Lỗi Đăng Nhập", "Tên người dùng hoặc Mật khẩu không đúng.")
            entry_password.delete(0, tk.END) 
            
    except Exception as e:
        messagebox.showerror("Lỗi Database", str(e))
    finally:
        conn.close()


def show_login_window(main_root, connect_db_func, center_window_func, color_fg):
    """Khởi tạo và hiển thị cửa sổ Đăng nhập."""
    
    login_root = tk.Toplevel(main_root) 
    login_root.title("Login")
    # Sử dụng hàm center_window được truyền từ file chính
    center_window_func(login_root, w=400, h=250) 
    login_root.resizable(False, False)
    login_root.grab_set() 
    
    BG_COLOR = "#b3cde0" 
    login_root.config(bg=BG_COLOR)

    # 2. TIÊU ĐỀ
    lbl_title = tk.Label(login_root, text="Login", font=("Arial", 20, "bold"), bg=BG_COLOR, fg="black")
    lbl_title.pack(pady=15)
    
    # 3. FRAME CHỨA THÔNG TIN ĐĂNG NHẬP
    frame_login_fields = tk.Frame(login_root, bg=BG_COLOR)
    frame_login_fields.pack(padx=20, pady=5)
    
    label_style = {"font": ("Arial", 12), "bg": BG_COLOR, "fg": color_fg}

    # Username
    tk.Label(frame_login_fields, text="Username", **label_style).grid(row=0, column=0, pady=10, padx=5, sticky="e")
    entry_username = tk.Entry(frame_login_fields, width=25, font=("Arial", 12))
    entry_username.grid(row=0, column=1, pady=10, padx=5)

    # Password
    tk.Label(frame_login_fields, text="Password", **label_style).grid(row=1, column=0, pady=10, padx=5, sticky="e")
    entry_password = tk.Entry(frame_login_fields, width=25, show="*", font=("Arial", 12)) 
    entry_password.grid(row=1, column=1, pady=10, padx=5)
    
    # 4. NÚT LOGIN 
    btn_login = tk.Button(login_root, 
                          text="Login", 
                          width=10, 
                          # Sử dụng lambda để truyền các tham số cần thiết
                          command=lambda: check_login(entry_username, entry_password, login_root, main_root, connect_db_func), 
                          font=("Arial", 12, "bold"),
                          fg=color_fg)
    btn_login.pack(pady=15)
    
    # Xử lý sự kiện Enter
    login_root.bind('<Return>', lambda event: check_login(entry_username, entry_password, login_root, main_root, connect_db_func))

    # Xử lý đóng cửa sổ: Đóng toàn bộ ứng dụng nếu cửa sổ login bị đóng
    login_root.protocol("WM_DELETE_WINDOW", main_root.quit)