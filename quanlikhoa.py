import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# --- LỚP QUẢN LÝ KHOA ---
class QuanLyKhoa(tk.Frame):
    def __init__(self, master, connect_db_func, root):
        super().__init__(master, bg="#fff5f5")  # nền tổng thể hồng nhạt
        self.connect_db = connect_db_func
        self.root = root  # root chính
        self.create_widgets()
        self.load_data()

    # --- HỦY NHẬP LIỆU ---
    def clear_input(self):
        self.entry_makhoa.config(state="normal")
        self.entry_makhoa.delete(0, tk.END)
        self.entry_tenkhoa.delete(0, tk.END)
        self.text_ghichu.delete("1.0", tk.END)

    # --- THOÁT FORM CON ---
    def thoat(self):
        if messagebox.askyesno("Thoát", "Bạn có chắc muốn thoát không?"):
            self.master.destroy()
            self.root.deiconify()

    # --- TẢI DỮ LIỆU ---
    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        conn = self.connect_db()
        if not conn:
            return
        cur = conn.cursor()
        cur.execute("SELECT makhoa, tenkhoa, ghichu FROM khoa")
        for i, row in enumerate(cur.fetchall()):
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
            SELECT makhoa, tenkhoa, ghichu
            FROM khoa
            WHERE makhoa LIKE %s OR tenkhoa LIKE %s
        """
        like_str = f"%{keyword}%"
        cur.execute(query, (like_str, like_str))
        for i, row in enumerate(cur.fetchall()):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", tk.END, values=row, tags=(tag,))
        conn.close()

    # --- THÊM KHOA ---
    def them_khoa(self):
        makhoa = self.entry_makhoa.get().strip()
        tenkhoa = self.entry_tenkhoa.get().strip()
        ghichu = self.text_ghichu.get("1.0", tk.END).strip()

        if not makhoa or not tenkhoa:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập Mã khoa và Tên khoa.")
            return

        conn = self.connect_db()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO khoa (makhoa, tenkhoa, ghichu) VALUES (%s, %s, %s)",
                        (makhoa, tenkhoa, ghichu))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã thêm khoa mới.")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Không thể thêm khoa: {err}")
        finally:
            conn.close()
        self.load_data()
        self.clear_input()

    # --- SỬA KHOA ---
    def sua_khoa(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn 1 khoa để sửa.")
            return

        values = self.tree.item(selected)["values"]
        self.clear_input()
        self.entry_makhoa.insert(0, values[0])
        self.entry_tenkhoa.insert(0, values[1])
        self.text_ghichu.insert("1.0", values[2])
        self.entry_makhoa.config(state="readonly")

    # --- LƯU CẬP NHẬT ---
    def luu_khoa(self):
        makhoa = self.entry_makhoa.get().strip()
        tenkhoa = self.entry_tenkhoa.get().strip()
        ghichu = self.text_ghichu.get("1.0", tk.END).strip()

        if not makhoa:
            messagebox.showerror("Lỗi", "Mã khoa không hợp lệ.")
            return

        conn = self.connect_db()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE khoa
                SET tenkhoa=%s, ghichu=%s
                WHERE makhoa=%s
            """, (tenkhoa, ghichu, makhoa))
            conn.commit()
            messagebox.showinfo("Thành công", f"Đã cập nhật thông tin khoa {makhoa}.")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Không thể lưu thay đổi: {err}")
        finally:
            conn.close()
        self.load_data()
        self.clear_input()
        self.entry_makhoa.config(state="normal")

    # --- XÓA KHOA ---
    def xoa_khoa(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn khoa để xóa.")
            return
        makhoa = self.tree.item(selected)["values"][0]
        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa khoa: {makhoa}?"):
            return

        conn = self.connect_db()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM khoa WHERE makhoa=%s", (makhoa,))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã xóa khoa.")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Không thể xóa khoa: {err}")
        finally:
            conn.close()
        self.load_data()
        self.clear_input()

    # --- GIAO DIỆN ---
    def create_widgets(self):
        COLOR_MAIN = "#a80000"
        BG_LIGHT = "#fff5f5"
        BG_INFO_FRAME = "#fcdada"
        BG_BUTTON = "#fd6f6f"
        FONT_LABEL = ("Times New Roman", 13, "bold")
        FONT_TITLE = ("Times New Roman", 18, "bold")

        self.master.configure(bg=BG_LIGHT)
        self.configure(bg=BG_LIGHT)

        # Tiêu đề
        tk.Label(self, text="QUẢN LÝ KHOA", font=FONT_TITLE, fg=COLOR_MAIN, bg=BG_LIGHT).pack(pady=10)

        # Frame thông tin
        frame_info = tk.Frame(self, bg=BG_INFO_FRAME)
        frame_info.pack(pady=5, padx=20, fill="x")

        tk.Label(frame_info, text="Mã khoa:", fg=COLOR_MAIN, font=FONT_LABEL, bg=BG_INFO_FRAME).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_makhoa = tk.Entry(frame_info, width=20)
        self.entry_makhoa.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_info, text="Tên khoa:", fg=COLOR_MAIN, font=FONT_LABEL, bg=BG_INFO_FRAME).grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.entry_tenkhoa = tk.Entry(frame_info, width=40)
        self.entry_tenkhoa.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_info, text="Ghi chú:", fg=COLOR_MAIN, font=FONT_LABEL, bg=BG_INFO_FRAME).grid(row=1, column=0, sticky="ne", padx=5, pady=5)
        self.text_ghichu = tk.Text(frame_info, width=70, height=2, font=("Times New Roman", 12))
        self.text_ghichu.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

        # Frame tìm kiếm
        frame_search = tk.Frame(self, bg=BG_LIGHT)
        frame_search.pack(pady=10)
        tk.Label(frame_search, text="Tìm kiếm:", fg=COLOR_MAIN, font=FONT_LABEL, bg=BG_LIGHT).pack(side="left", padx=(0,5))
        self.entry_search = tk.Entry(frame_search, width=30)
        self.entry_search.pack(side="left", padx=5)
        tk.Button(frame_search, text="Tìm", command=self.tim_kiem, fg="white", bg=BG_BUTTON, font=FONT_LABEL).pack(side="left", padx=5)
        tk.Button(frame_search, text="Hiện tất cả", command=self.load_data, fg="white", bg=BG_BUTTON, font=FONT_LABEL).pack(side="left", padx=5)

        # Frame nút
        frame_btn = tk.Frame(self, bg=BG_LIGHT)
        frame_btn.pack(pady=10)
        btn_conf = {"width": 8, "fg": "white", "bg": BG_BUTTON, "font": FONT_LABEL}
        tk.Button(frame_btn, text="Thêm", command=self.them_khoa, **btn_conf).grid(row=0, column=0, padx=10)
        tk.Button(frame_btn, text="Lưu", command=self.luu_khoa, **btn_conf).grid(row=0, column=1, padx=10)
        tk.Button(frame_btn, text="Sửa", command=self.sua_khoa, **btn_conf).grid(row=0, column=2, padx=10)
        tk.Button(frame_btn, text="Hủy", command=self.clear_input, **btn_conf).grid(row=0, column=3, padx=10)
        tk.Button(frame_btn, text="Xóa", command=self.xoa_khoa, **btn_conf).grid(row=0, column=4, padx=10)
        tk.Button(frame_btn, text="Thoát", command=self.thoat, **btn_conf).grid(row=0, column=5, padx=10)

        # Treeview
        tk.Label(self, text="Danh sách khoa", fg=COLOR_MAIN, font=FONT_LABEL, bg=BG_LIGHT).pack(pady=5, anchor="w", padx=15)
        columns = ("makhoa", "tenkhoa", "ghichu")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=12)

        style = ttk.Style()
        style.configure("Treeview", font=("Times New Roman", 12))
        style.configure("Treeview.Heading", font=("Times New Roman", 13, "bold"))
        style.map("Treeview", background=[("selected", COLOR_MAIN)], foreground=[("selected", "white")])

        for col, text, width in zip(columns, ["Mã khoa", "Tên khoa", "Ghi chú"], [100, 250, 400]):
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor="center" if col != "ghichu" else "w")

        self.tree.tag_configure('evenrow', background="#fff0f0")
        self.tree.tag_configure('oddrow', background="#ffffff")
        self.tree.pack(padx=15, pady=5, fill="both", expand=True)
