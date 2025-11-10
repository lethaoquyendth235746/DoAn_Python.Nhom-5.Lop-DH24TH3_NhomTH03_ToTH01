import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

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

# --- QUẢN LÝ BÁC SĨ ---
class QuanLyBacSi(tk.Frame):
    def __init__(self, master, connect_db_func, main_root):
        super().__init__(master, bg="#fff5f5")
        self.connect_db = connect_db_func
        self.main_root = main_root

        # --- TONE MÀU ---
        self.COLOR_MAIN = "#a80000"
        self.BG_LIGHT = "#fff5f5"
        self.BG_INFO_FRAME = "#fcdada"
        self.BG_BUTTON_FRAME = "#f9dcdc"
        self.BTN_COLOR_MAIN = "#a80000"
        self.BTN_HOVER_MAIN = "#d32f2f"
        self.BTN_COLOR_SEARCH = "#faad14"
        self.BTN_HOVER_SEARCH = "#ffc53d"
        self.FONT_LABEL = ("Times New Roman", 13, "bold")
        self.FONT_BTN = ("Times New Roman", 12, "bold")
        self.FONT_TITLE = ("Times New Roman", 18, "bold")

        self.create_widgets()
        self.load_data()

    # --- XÓA INPUT ---
    def clear_input(self):
        for entry in [self.entry_mabs, self.entry_hoten, self.entry_chuyenkhoa, self.entry_sdt, self.cb_makhoa]:
            entry.config(state="normal")
            if isinstance(entry, ttk.Combobox):
                entry.set("")
            else:
                entry.delete(0, tk.END)

    # --- TẢI DỮ LIỆU ---
    def load_data(self, filter_keyword=""):
        for i in self.tree.get_children():
            self.tree.delete(i)
        conn = self.connect_db()
        if not conn:
            return
        cur = conn.cursor()
        if filter_keyword:
            query = """
                SELECT mabs, hoten, chuyenkhoa, sdt, makhoa 
                FROM bacsi 
                WHERE mabs LIKE %s OR hoten LIKE %s
            """
            cur.execute(query, (f"%{filter_keyword}%", f"%{filter_keyword}%"))
        else:
            cur.execute("SELECT mabs, hoten, chuyenkhoa, sdt, makhoa FROM bacsi")
        for i, row in enumerate(cur.fetchall()):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", tk.END, values=row, tags=(tag,))
        conn.close()

    # --- THÊM ---
    def them_bs(self):
        mabs = self.entry_mabs.get().strip()
        hoten = self.entry_hoten.get().strip()
        chuyenkhoa = self.entry_chuyenkhoa.get().strip()
        sdt = self.entry_sdt.get().strip()
        makhoa = self.cb_makhoa.get().strip()

        if not mabs or not hoten or not chuyenkhoa:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập Mã bác sĩ, Họ tên và Chuyên khoa.")
            return

        conn = self.connect_db()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO bacsi (mabs, hoten, chuyenkhoa, sdt, makhoa) VALUES (%s, %s, %s, %s, %s)",
                (mabs, hoten, chuyenkhoa, sdt, makhoa)
            )
            conn.commit()
            messagebox.showinfo("Thành công", "Đã thêm bác sĩ mới.")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Không thể thêm bác sĩ: {err}")
        finally:
            conn.close()

        self.load_data()
        self.clear_input()

    # --- SỬA ---
    def sua_bs(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn 1 bác sĩ để sửa.")
            return
        values = self.tree.item(selected)["values"]
        self.clear_input()
        self.entry_mabs.insert(0, values[0])
        self.entry_mabs.config(state="readonly")
        self.entry_hoten.insert(0, values[1])
        self.entry_chuyenkhoa.insert(0, values[2])
        self.entry_sdt.insert(0, values[3])
        self.cb_makhoa.set(values[4])

    # --- LƯU ---
    def luu_bs(self):
        mabs = self.entry_mabs.get().strip()
        hoten = self.entry_hoten.get().strip()
        chuyenkhoa = self.entry_chuyenkhoa.get().strip()
        sdt = self.entry_sdt.get().strip()
        makhoa = self.cb_makhoa.get().strip()

        if not mabs:
            messagebox.showerror("Lỗi", "Mã bác sĩ không hợp lệ.")
            return

        conn = self.connect_db()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE bacsi
                SET hoten=%s, chuyenkhoa=%s, sdt=%s, makhoa=%s
                WHERE mabs=%s
            """, (hoten, chuyenkhoa, sdt, makhoa, mabs))
            conn.commit()
            messagebox.showinfo("Thành công", f"Đã cập nhật thông tin bác sĩ: {mabs}.")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Không thể lưu thay đổi: {err}")
        finally:
            conn.close()

        self.load_data()
        self.clear_input()
        self.entry_mabs.config(state="normal")

    # --- XÓA ---
    def xoa_bs(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn bác sĩ để xóa.")
            return
        mabs = self.tree.item(selected)["values"][0]
        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa bác sĩ có mã: {mabs}?"):
            return

        conn = self.connect_db()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM bacsi WHERE mabs=%s", (mabs,))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã xóa bác sĩ.")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Không thể xóa bác sĩ: {err}")
        finally:
            conn.close()
        self.load_data()
        self.clear_input()

    # --- TÌM KIẾM ---
    def tim_kiem(self):
        keyword = self.entry_search.get().strip()
        if not keyword:
            messagebox.showwarning("Chưa nhập", "Vui lòng nhập Mã BS hoặc Họ tên để tìm kiếm!")
            return
        self.load_data(filter_keyword=keyword)

    # --- THOÁT ---
    def quit_window(self):
        self.master.destroy()
        self.main_root.deiconify()

    # --- GIAO DIỆN ---
    def create_widgets(self):
        self.master.configure(bg=self.BG_LIGHT)
        self.configure(bg=self.BG_LIGHT)

        # Tiêu đề
        tk.Label(self, text="QUẢN LÝ BÁC SĨ", font=self.FONT_TITLE, fg=self.COLOR_MAIN, bg=self.BG_LIGHT).pack(pady=10)

        # --- SEARCH ---
        search_frame = tk.Frame(self, bg=self.BG_LIGHT)
        search_frame.pack(fill="x", padx=20, pady=5)
        tk.Label(search_frame, text="Tìm kiếm Mã BS / Họ tên:", font=self.FONT_LABEL, bg=self.BG_LIGHT).pack(side="left")
        self.entry_search = tk.Entry(search_frame, font=("Times New Roman", 12), width=30)
        self.entry_search.pack(side="left", padx=5)
        btn_search = tk.Button(search_frame, text="Tìm Kiếm", command=self.tim_kiem,
                               font=self.FONT_BTN, bg=self.BTN_COLOR_SEARCH, fg="white", width=10, relief="ridge", cursor="hand2")
        btn_search.pack(side="left", padx=5)
        btn_search.bind("<Enter>", lambda e: btn_search.config(bg=self.BTN_HOVER_SEARCH))
        btn_search.bind("<Leave>", lambda e: btn_search.config(bg=self.BTN_COLOR_SEARCH))

        # Frame thông tin
        frame_info = tk.Frame(self, bg=self.BG_INFO_FRAME)
        frame_info.pack(pady=5, padx=20, fill="x")

        # Dòng 1
        tk.Label(frame_info, text="Mã bác sĩ:", fg=self.COLOR_MAIN, font=self.FONT_LABEL, bg=self.BG_INFO_FRAME).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_mabs = tk.Entry(frame_info, width=20)
        self.entry_mabs.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_info, text="Họ tên:", fg=self.COLOR_MAIN, font=self.FONT_LABEL, bg=self.BG_INFO_FRAME).grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.entry_hoten = tk.Entry(frame_info, width=30)
        self.entry_hoten.grid(row=0, column=3, padx=5, pady=5)

        # Dòng 2
        tk.Label(frame_info, text="Chuyên khoa:", fg=self.COLOR_MAIN, font=self.FONT_LABEL, bg=self.BG_INFO_FRAME).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_chuyenkhoa = tk.Entry(frame_info, width=25)
        self.entry_chuyenkhoa.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_info, text="SĐT:", fg=self.COLOR_MAIN, font=self.FONT_LABEL, bg=self.BG_INFO_FRAME).grid(row=1, column=2, sticky="e", padx=5, pady=5)
        self.entry_sdt = tk.Entry(frame_info, width=30)
        self.entry_sdt.grid(row=1, column=3, padx=5, pady=5)

        # Dòng 3 - Mã khoa combobox
        tk.Label(frame_info, text="Mã khoa:", fg=self.COLOR_MAIN, font=self.FONT_LABEL, bg=self.BG_INFO_FRAME).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.cb_makhoa = ttk.Combobox(frame_info, width=20, state="readonly", values=self.load_makhoa_values())
        self.cb_makhoa.grid(row=2, column=1, padx=5, pady=5)

        # Frame nút
        frame_btn = tk.Frame(self, bg=self.BG_BUTTON_FRAME)
        frame_btn.pack(pady=10)
        btn_conf = {"font": self.FONT_BTN, "bg": self.BTN_COLOR_MAIN, "fg": "white", "width": 10, "relief": "ridge", "cursor": "hand2"}
        btns = [("Thêm", self.them_bs), ("Sửa", self.sua_bs), ("Lưu", self.luu_bs),
                ("Hủy", self.clear_input), ("Xóa", self.xoa_bs), ("Thoát", self.quit_window)]
        for i, (name, cmd) in enumerate(btns):
            btn = tk.Button(frame_btn, text=name, command=cmd, **btn_conf)
            btn.grid(row=0, column=i, padx=5)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.BTN_HOVER_MAIN))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.BTN_COLOR_MAIN))

        # Treeview
                # Treeview với Scrollbar dọc
        lbl_ds = tk.Label(self, text="Danh sách bác sĩ", fg=self.COLOR_MAIN, font=self.FONT_LABEL, bg=self.BG_LIGHT)
        lbl_ds.pack(pady=5, anchor="w", padx=15)

        columns = ("mabs", "hoten", "chuyenkhoa", "sdt", "makhoa")
        headings = ["Mã BS", "Họ và tên", "Chuyên khoa", "SĐT", "Mã khoa"]
        widths = [100, 200, 180, 120, 100]

        # Frame chứa Treeview + Scrollbar
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=15, pady=5)

        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)

        # Scrollbar dọc
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview", font=("Times New Roman", 12))
        style.configure("Treeview.Heading", font=("Times New Roman", 13, "bold"))
        style.map("Treeview", background=[("selected", self.COLOR_MAIN)], foreground=[("selected", "white")])

        for col, head, w in zip(columns, headings, widths):
            self.tree.heading(col, text=head)
            self.tree.column(col, width=w, anchor="center")

        self.tree.tag_configure('evenrow', background="#fff0f0")
        self.tree.tag_configure('oddrow', background="#ffffff")


    # --- LẤY DANH SÁCH MÃ KHOA ---
    def load_makhoa_values(self):
        conn = self.connect_db()
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute("SELECT makhoa FROM khoa")
        values = [row[0] for row in cur.fetchall()]
        conn.close()
        return values
