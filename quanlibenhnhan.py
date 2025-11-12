import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector
import datetime

# --- KẾT NỐI DATABASE ---
def connect_db():
    try:
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

# Canh giữa cửa sổ
def center_window(win, w=1150, h=670):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

# --- QUẢN LÝ BỆNH NHÂN ---
def create_quanlybenhnhan(window):
    

    main_root = tk._default_root  # lấy root chính
    window.title("Quản lý bệnh nhân")
    window.geometry("1150x670")
    window.resizable(True, True)

    def on_close():
        main_root.deiconify()
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_close)

    # ===== MÀU GIAO DIỆN GIỐNG FILE QUẢN LÝ DỊCH VỤ =====
    COLOR_MAIN = "#a80000"         # màu đỏ chủ đạo
    BG_LIGHT = "#fff5f5"           # nền tổng thể hồng nhạt
    BG_INFO_FRAME = "#fcdada"      # frame thông tin hồng nhạt hơn
    BG_BUTTON_FRAME = "#f9dcdc"    # frame nút
    BG_BUTTON = "#fd6f6f"          # nút màu đỏ
    FONT_LABEL = ("Times New Roman", 13, "bold")
    BTN_COLOR3 = "#faad14"    # vàng đậm cho nút           
    BTN_COLOR1 = "#2e7d32"
    window.configure(bg=BG_LIGHT)
    # ==== Container chính ====
    container = tk.Frame(window, bg="#fff5f5")
    container.place(relx=0.5, rely=0.5, anchor="center")  # căn giữa toàn bộ nội dung


    # ===== Tiêu đề =====
    tk.Label(window, text="THÔNG TIN BỆNH NHÂN", 
             font=("Times New Roman", 18, "bold"), fg=COLOR_MAIN, bg=BG_LIGHT).pack(pady=10)

    # ===== Frame Tìm kiếm =====
    frame_search = tk.LabelFrame(window, text="Tìm kiếm bệnh nhân", font=FONT_LABEL,
                                 fg=COLOR_MAIN, bg=BG_INFO_FRAME, padx=10, pady=10)
    frame_search.pack(padx=10, pady=5, fill="x")

    tk.Label(frame_search, text="Mã BN:", font=FONT_LABEL, bg=BG_INFO_FRAME).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_search = tk.Entry(frame_search, width=20)
    entry_search.grid(row=0, column=1, padx=5, pady=5)

    tk.Button(frame_search, text="Tìm kiếm", font=FONT_LABEL, bg=BTN_COLOR3, fg="white",
              command=lambda: tim_kiem(entry_search, tree)).grid(row=0, column=2, padx=5, pady=5)
    tk.Button(frame_search, text="Hiện tất cả", font=FONT_LABEL, bg=BTN_COLOR1, fg="white",
              command=lambda: load_data()).grid(row=0, column=3, padx=5, pady=5)

    # ===== Frame nhập thông tin =====
    frame_info = tk.LabelFrame(window, text="Thông tin bệnh nhân", font=FONT_LABEL,
                               fg=COLOR_MAIN, bg=BG_INFO_FRAME, padx=10, pady=10)
    frame_info.pack(pady=5, padx=10, fill="x")

    tk.Label(frame_info, text="Mã bệnh nhân", font=FONT_LABEL, bg=BG_INFO_FRAME).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_mabn = tk.Entry(frame_info, width=15)
    entry_mabn.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Họ và lót", font=FONT_LABEL, bg=BG_INFO_FRAME).grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_holot = tk.Entry(frame_info, width=25)
    entry_holot.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Tên", font=FONT_LABEL, bg=BG_INFO_FRAME).grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_ten = tk.Entry(frame_info, width=15)
    entry_ten.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    gender_var = tk.StringVar(value="Nam")
    tk.Label(frame_info, text="Phái", font=FONT_LABEL, bg=BG_INFO_FRAME).grid(row=3, column=0, padx=5, pady=5, sticky="w")
    tk.Radiobutton(frame_info, text="Nam", variable=gender_var, value="Nam", font=FONT_LABEL, bg=BG_INFO_FRAME).grid(row=3, column=1, padx=5, sticky="w")
    tk.Radiobutton(frame_info, text="Nữ", variable=gender_var, value="Nữ", font=FONT_LABEL, bg=BG_INFO_FRAME).grid(row=3, column=2, padx=5, sticky="w")

    tk.Label(frame_info, text="Ngày sinh", font=FONT_LABEL, bg=BG_INFO_FRAME).grid(row=0, column=2, padx=(90,5), pady=5, sticky="w")
    date_entry = DateEntry(frame_info, width=12, background="darkblue", foreground="white", date_pattern="dd/mm/yyyy")
    date_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Địa chỉ", font=FONT_LABEL, bg=BG_INFO_FRAME).grid(row=1, column=2, padx=(90,5), pady=5, sticky="w")
    entry_diachi = tk.Entry(frame_info, width=55)
    entry_diachi.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="SĐT", font=FONT_LABEL, bg=BG_INFO_FRAME).grid(row=2, column=2, padx=(90,5), pady=5, sticky="w")
    entry_sdt = tk.Entry(frame_info, width=20)
    entry_sdt.grid(row=2, column=3, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="CCCD", font=FONT_LABEL, bg=BG_INFO_FRAME).grid(row=3, column=2, padx=(90,5), pady=5, sticky="w")
    entry_cccd = tk.Entry(frame_info, width=25)
    entry_cccd.grid(row=3, column=3, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Ngày đăng ký", font=FONT_LABEL, bg=BG_INFO_FRAME).grid(row=4, column=0, padx=5, pady=5, sticky="w")
    date_dk = DateEntry(frame_info, width=12, background="darkblue", foreground="white", date_pattern="dd/mm/yyyy")
    date_dk.grid(row=4, column=1, padx=5, pady=5, sticky="w")

    # ===== Frame nút CRUD =====
    frame_btn = tk.Frame(window, bg=BG_LIGHT)
    frame_btn.pack(pady=5)

    # --- Các hàm CRUD ---
    def clear_input():
        entry_mabn.config(state="normal")
        entry_mabn.delete(0, tk.END)
        entry_holot.delete(0, tk.END)
        entry_ten.delete(0, tk.END)
        entry_diachi.delete(0, tk.END)
        entry_sdt.delete(0, tk.END)
        entry_cccd.delete(0, tk.END)
        gender_var.set("Nam")
        date_entry.set_date("01-01-2000")
        date_dk.set_date(datetime.date.today())

    def load_data():
        for i in tree.get_children():
            tree.delete(i)
        conn = connect_db()
        if not conn:
            return
        cur = conn.cursor()
        cur.execute("SELECT mabn, holot, ten, phai, ngaysinh, diachi, sdt, cccd, ngaydangky FROM benhnhan")
        rows = cur.fetchall()
        for row in rows:
            row_list = list(row)
            for i in [4,8]:
                if isinstance(row_list[i], datetime.date):
                    row_list[i] = row_list[i].strftime("%d/%m/%Y")
            tree.insert("", tk.END, values=row_list)
        conn.close()

    def them_nv():
        mabn = entry_mabn.get().strip()
        holot = entry_holot.get().strip()
        ten = entry_ten.get().strip()
        phai = gender_var.get()
        diachi = entry_diachi.get().strip()
        sdt = entry_sdt.get().strip()
        cccd = entry_cccd.get().strip()
        try:
            ngaysinh_sql = datetime.datetime.strptime(date_entry.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
            ngaydk_sql = datetime.datetime.strptime(date_dk.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Lỗi định dạng ngày", "Ngày sinh hoặc ngày đăng ký không hợp lệ!")
            return
        if not all([mabn, holot, ten, diachi, sdt, cccd]):
            messagebox.showerror("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
            return
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO benhnhan (mabn, holot, ten, phai, ngaysinh, diachi, sdt, cccd, ngaydangky)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (mabn, holot, ten, phai, ngaysinh_sql, diachi, sdt, cccd, ngaydk_sql))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã thêm bệnh nhân mới.")
            load_data()
            clear_input()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        conn.close()

    def xoa_nv():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn bệnh nhân để xóa")
            return
        mabn_to_delete = tree.item(selected)["values"][0]
        if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn xóa bệnh nhân có Mã: {mabn_to_delete}?"):
            conn = connect_db()
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM benhnhan WHERE mabn=%s", (mabn_to_delete,))
                conn.commit()
                messagebox.showinfo("Thành công", "Đã xóa bệnh nhân.")
            except Exception as e:
                messagebox.showerror("Lỗi xóa", str(e))
            finally:
                conn.close()
            load_data()
            clear_input()

    def sua_nv():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn bệnh nhân để sửa")
            return
        values = tree.item(selected)["values"]
        entry_mabn.delete(0, tk.END)
        entry_mabn.insert(0, values[0])
        entry_mabn.config(state="readonly")
        entry_holot.delete(0, tk.END)
        entry_holot.insert(0, values[1])
        entry_ten.delete(0, tk.END)
        entry_ten.insert(0, values[2])
        gender_var.set(values[3])
        date_entry.set_date(values[4])
        entry_diachi.delete(0, tk.END)
        entry_diachi.insert(0, values[5])
        entry_sdt.delete(0, tk.END)
        entry_sdt.insert(0, values[6])
        entry_cccd.delete(0, tk.END)
        entry_cccd.insert(0, values[7])
        date_dk.set_date(values[8])

    def luu_nv():
        mabn = entry_mabn.get().strip()
        holot = entry_holot.get().strip()
        ten = entry_ten.get().strip()
        phai = gender_var.get()
        diachi = entry_diachi.get().strip()
        sdt = entry_sdt.get().strip()
        cccd = entry_cccd.get().strip()
        try:
            ngaysinh_sql = datetime.datetime.strptime(date_entry.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
            ngaydangky_sql = datetime.datetime.strptime(date_dk.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Lỗi định dạng ngày", "Ngày sinh hoặc ngày đăng ký không hợp lệ!")
            return
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE benhnhan SET holot=%s, ten=%s, phai=%s, ngaysinh=%s, diachi=%s, sdt=%s, cccd=%s, ngaydangky=%s
                WHERE mabn=%s
            """, (holot, ten, phai, ngaysinh_sql, diachi, sdt, cccd, ngaydangky_sql, mabn))
            conn.commit()
            messagebox.showinfo("Thành công", f"Đã cập nhật thông tin bệnh nhân: {mabn}")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()
        load_data()
        clear_input()

    def tim_kiem(entry_search, tree):
        mabn = entry_search.get().strip()
        if not mabn:
            messagebox.showwarning("Chưa nhập", "Vui lòng nhập mã bệnh nhân để tìm kiếm!")
            return
        for i in tree.get_children():
            tree.delete(i)
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("SELECT mabn, holot, ten, phai, ngaysinh, diachi, sdt, cccd, ngaydangky FROM benhnhan WHERE mabn LIKE %s", (f"%{mabn}%",))
            rows = cur.fetchall()
            if not rows:
                messagebox.showinfo("Kết quả", "Không tìm thấy bệnh nhân nào!")
            for row in rows:
                row_list = list(row)
                for i in [4,8]:
                    if isinstance(row_list[i], datetime.date):
                        row_list[i] = row_list[i].strftime("%d/%m/%Y")
                tree.insert("", tk.END, values=row_list)
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()

    # ===== Buttons CRUD =====
        # ===== Buttons CRUD =====
    btns = [
        ("Thêm", them_nv),
        ("Lưu", luu_nv),
        ("Sửa", sua_nv),
        ("Hủy", clear_input),
        ("Xóa", xoa_nv),
        ("Thoát", on_close)
    ]
    for idx, (txt, cmd) in enumerate(btns):
        tk.Button(frame_btn, text=txt, width=8, command=cmd, font=FONT_LABEL, 
                  bg="#a80000", fg="white").grid(row=0, column=idx, padx=20)

    # ===== Treeview =====
    lbl_ds = tk.Label(window, text="Danh sách bệnh nhân", fg=COLOR_MAIN, font=FONT_LABEL, bg=BG_LIGHT)
    lbl_ds.pack(pady=5, anchor="w", padx=10)

    columns = ("mabn", "holot", "ten", "phai", "ngaysinh", "diachi", "sdt", "cccd", "ngaydangky")
    headings = ["Mã BN","Họ và lót","Tên","Phái","Ngày sinh","Địa chỉ","SĐT","CCCD","Ngày đăng ký"]
    widths = [60,120,70,50,100,250,100,120,100]

    tree_frame = tk.Frame(window)
    tree_frame.pack(pady=5, padx=10, fill="both", expand=True)

    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)

    style = ttk.Style()
    style.configure("Treeview", font=("Times New Roman", 12))
    style.configure("Treeview.Heading", font=("Times New Roman", 13, "bold"))
    style.map("Treeview", background=[("selected", "#a80000")], foreground=[("selected", "white")])

    for col, head, w in zip(columns, headings, widths):
        tree.heading(col, text=head)
        tree.column(col, width=w, anchor="center")

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)
