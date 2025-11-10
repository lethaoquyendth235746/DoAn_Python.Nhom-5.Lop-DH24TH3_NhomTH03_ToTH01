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
        messagebox.showerror("Lỗi kết nối", f"Không thể kết nối MySQL: {err}")
        return None


# --- LỚP QUẢN LÝ PHÒNG ---
class QuanLyPhong(tk.Frame):
    def __init__(self, master, connect_db_func):
        super().__init__(master)
        self.connect_db = connect_db_func
        self.configure(bg="#fff5f5")
        self.create_widgets()
        self.load_khoa_combobox()
        self.load_data()

    # --- XÓA INPUT ---
    def clear_input(self):
        for entry in [self.entry_maphong, self.entry_tenphong, self.entry_sogiuong]:
            entry.config(state="normal")
            entry.delete(0, tk.END)
        self.cb_loaiphong.set("")
        self.cb_makhoa.set("")
    def close_form(self):
        self.master.destroy()  # đóng form con
        if hasattr(self.master, "master"):  # kiểm tra có form chính
            self.master.master.deiconify()  # hiện lại form chính


    # --- TẢI DANH SÁCH KHOA ---
    def load_khoa_combobox(self):
        conn = self.connect_db()
        if not conn:
            return
        cur = conn.cursor()
        cur.execute("SELECT makhoa FROM khoa")
        data = [row[0] for row in cur.fetchall()]
        conn.close()
        self.cb_makhoa["values"] = data

    # --- TẢI DỮ LIỆU PHÒNG ---
    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        conn = self.connect_db()
        if not conn:
            return
        cur = conn.cursor()
        cur.execute("SELECT maphong, tenphong, loaiphong, sogiuong, makhoa FROM phong")
        rows = cur.fetchall()
        for i, row in enumerate(rows):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", tk.END, values=row, tags=(tag,))
        conn.close()

    # --- TÌM KIẾM ---
    def tim_kiem(self):
        keyword = self.entry_search.get().strip()
        for i in self.tree.get_children():
            self.tree.delete(i)

        conn = self.connect_db()
        if not conn:
            return
        cur = conn.cursor()
        query = """
            SELECT maphong, tenphong, loaiphong, sogiuong, makhoa
            FROM phong
            WHERE maphong LIKE %s OR tenphong LIKE %s
        """
        like_str = f"%{keyword}%"
        cur.execute(query, (like_str, like_str))
        rows = cur.fetchall()
        for i, row in enumerate(rows):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", tk.END, values=row, tags=(tag,))
        conn.close()

    # --- THÊM ---
    def them_phong(self):
        maphong = self.entry_maphong.get().strip()
        tenphong = self.entry_tenphong.get().strip()
        loaiphong = self.cb_loaiphong.get().strip()
        sogiuong = self.entry_sogiuong.get().strip()
        makhoa = self.cb_makhoa.get().strip()

        if not maphong or not tenphong:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập Mã phòng và Tên phòng.")
            return

        conn = self.connect_db()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO phong (maphong, tenphong, loaiphong, sogiuong, makhoa) VALUES (%s, %s, %s, %s, %s)",
                (maphong, tenphong, loaiphong, sogiuong or None, makhoa or None)
            )
            conn.commit()
            messagebox.showinfo("Thành công", "Đã thêm phòng mới.")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Không thể thêm phòng: {err}")
        finally:
            conn.close()
        self.load_data()
        self.clear_input()

    # --- SỬA ---
    def sua_phong(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn 1 phòng để sửa.")
            return

        values = self.tree.item(selected)["values"]
        self.clear_input()
        self.entry_maphong.insert(0, values[0])
        self.entry_tenphong.insert(0, values[1])
        self.cb_loaiphong.set(values[2])
        self.entry_sogiuong.insert(0, values[3])
        self.cb_makhoa.set(values[4])
        self.entry_maphong.config(state="readonly")

    # --- LƯU (CẬP NHẬT) ---
    def luu_phong(self):
        maphong = self.entry_maphong.get().strip()
        tenphong = self.entry_tenphong.get().strip()
        loaiphong = self.cb_loaiphong.get().strip()
        sogiuong = self.entry_sogiuong.get().strip()
        makhoa = self.cb_makhoa.get().strip()

        conn = self.connect_db()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE phong
                SET tenphong=%s, loaiphong=%s, sogiuong=%s, makhoa=%s
                WHERE maphong=%s
            """, (tenphong, loaiphong, sogiuong or None, makhoa or None, maphong))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin phòng.")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Không thể lưu thay đổi: {err}")
        finally:
            conn.close()
        self.load_data()
        self.clear_input()

    # --- XÓA ---
    def xoa_phong(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn phòng để xóa.")
            return
        maphong = self.tree.item(selected)["values"][0]
        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa phòng: {maphong}?"):
            return

        conn = self.connect_db()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM phong WHERE maphong=%s", (maphong,))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã xóa phòng.")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Không thể xóa phòng: {err}")
        finally:
            conn.close()
        self.load_data()
        self.clear_input()

    # --- GIAO DIỆN ---
    def create_widgets(self):
        
        COLOR_MAIN = "#a80000"  # đỏ chủ đạo
        FONT_LABEL = ("Times New Roman", 13, "bold")
        BG_LIGHT = "#fff5f5"

        # === TIÊU ĐỀ ===
        tk.Label(self, text="QUẢN LÝ PHÒNG", font=("Times New Roman", 22, "bold"),
                fg=COLOR_MAIN, bg=BG_LIGHT).pack(pady=10)

        # === THÔNG TIN PHÒNG ===
        frame_info = tk.LabelFrame(self, text="Thông tin phòng", font=FONT_LABEL, bg="#fcdada",
                                fg=COLOR_MAIN, padx=10, pady=10, bd=2, relief="groove")
        frame_info.pack(pady=10, padx=15, fill="x")

        tk.Label(frame_info, text="Mã phòng:", font=FONT_LABEL, bg="#ffeaea").grid(row=0, column=0, padx=8, pady=6, sticky="e")
        self.entry_maphong = tk.Entry(frame_info, font=("Times New Roman", 12))
        self.entry_maphong.grid(row=0, column=1, padx=8, pady=6)

        tk.Label(frame_info, text="Tên phòng:", font=FONT_LABEL, bg="#ffeaea").grid(row=0, column=2, padx=8, pady=6, sticky="e")
        self.entry_tenphong = tk.Entry(frame_info, font=("Times New Roman", 12))
        self.entry_tenphong.grid(row=0, column=3, padx=8, pady=6)

        tk.Label(frame_info, text="Loại phòng:", font=FONT_LABEL, bg="#ffeaea").grid(row=1, column=0, padx=8, pady=6, sticky="e")
        self.cb_loaiphong = ttk.Combobox(frame_info, font=("Times New Roman", 12), state="readonly",
                                        values=["Phòng thường", "Phòng VIP", "Phòng cấp cứu"])
        self.cb_loaiphong.grid(row=1, column=1, padx=8, pady=6)

        tk.Label(frame_info, text="Số giường:", font=FONT_LABEL, bg="#ffeaea").grid(row=1, column=2, padx=8, pady=6, sticky="e")
        self.entry_sogiuong = tk.Entry(frame_info, font=("Times New Roman", 12))
        self.entry_sogiuong.grid(row=1, column=3, padx=8, pady=6)

        tk.Label(frame_info, text="Mã khoa:", font=FONT_LABEL, bg="#ffeaea").grid(row=2, column=0, padx=8, pady=6, sticky="e")
        self.cb_makhoa = ttk.Combobox(frame_info, font=("Times New Roman", 12), state="readonly")
        self.cb_makhoa.grid(row=2, column=1, padx=8, pady=6)

        # === CHỨC NĂNG ===
        frame_btn = tk.LabelFrame(self, text="Chức năng", font=FONT_LABEL, bg="#f9dcdc",
                                fg=COLOR_MAIN, padx=10, pady=10, bd=2, relief="groove")
        frame_btn.pack(pady=5, padx=15, fill="x")

        # Cấu hình nút đỏ đậm
        btn_red_conf = {
            "font": ("Times New Roman", 12, "bold"),
            "bg": "#a80000",
            "fg": "white",
            "activebackground": "#7f0000",
            "activeforeground": "white",
            "width": 10
        }

        tk.Button(frame_btn, text="Thêm", command=self.them_phong, **btn_red_conf).grid(row=0, column=0, padx=25, pady=5)
        tk.Button(frame_btn, text="Sửa", command=self.sua_phong, **btn_red_conf).grid(row=0, column=1, padx=25, pady=5)
        tk.Button(frame_btn, text="Lưu", command=self.luu_phong, **btn_red_conf).grid(row=0, column=2, padx=25, pady=5)
        tk.Button(frame_btn, text="Xóa", command=self.xoa_phong, **btn_red_conf).grid(row=0, column=3, padx=25, pady=5)
        tk.Button(frame_btn, text="Hủy", command=self.clear_input, **btn_red_conf).grid(row=0, column=4, padx=25, pady=5)
        tk.Button(frame_btn, text="Thoát", command=self.close_form, **btn_red_conf).grid(row=0, column=5, padx=25, pady=5)

        # === TÌM KIẾM ===
        search_frame = tk.Frame(self, bg=BG_LIGHT)
        search_frame.pack(fill="x", padx=15, pady=(5, 0))
        tk.Label(search_frame, text="Tìm kiếm:", font=FONT_LABEL, bg=BG_LIGHT).pack(side="left", padx=5)
        self.entry_search = tk.Entry(search_frame, font=("Times New Roman", 12), width=30)
        self.entry_search.pack(side="left", padx=5)

        # Nút tìm kiếm màu vàng đậm
        btn_search_conf = {
            "font": ("Times New Roman", 12, "bold"),
            "bg": "#faad14",
            "fg": "white",
            "activebackground": "#d99800",
            "activeforeground": "white",
            "width": 8
        }
        tk.Button(search_frame, text="Tìm Kiếm", command=self.tim_kiem, **btn_search_conf).pack(side="left", padx=5)

        # === BẢNG DANH SÁCH ===
        # === BẢNG DANH SÁCH ===
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=15, pady=10)

        columns = ("maphong", "tenphong", "loaiphong", "sogiuong", "makhoa")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)

        # Scrollbar dọc
        scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side="right", fill="y")

        # Scrollbar ngang 
        scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side="bottom", fill="x")

        # Cấu hình cột và tiêu đề
        for col, text in zip(columns, ["Mã phòng", "Tên phòng", "Loại phòng", "Số giường", "Mã khoa"]):
            self.tree.heading(col, text=text)
            self.tree.column(col, anchor="center", width=150)

        # Style Treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Times New Roman", 13, "bold"))
        style.configure("Treeview", font=("Times New Roman", 12))
        style.map("Treeview", background=[("selected", "#a80000")], foreground=[("selected", "white")])

        self.tree.tag_configure('evenrow', background="#fff0f0")
        self.tree.tag_configure('oddrow', background="#ffffff")

        # Pack Treeview
        self.tree.pack(side="left", fill="both", expand=True)


# --- CHẠY THỬ ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Quản lý Phòng")
    root.geometry("950x650")
    app = QuanLyPhong(root, connect_db)
    app.pack(fill="both", expand=True)
    root.mainloop()
