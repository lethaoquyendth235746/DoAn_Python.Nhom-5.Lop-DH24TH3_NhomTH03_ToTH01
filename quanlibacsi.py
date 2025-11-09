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
        super().__init__(master, bg="#fff5f5")  # nền tổng thể hồng nhạt
        self.connect_db = connect_db_func
        self.main_root = main_root
        self.create_widgets()
        self.load_data()

    # --- XÓA INPUT ---
    def clear_input(self):
        for entry in [self.entry_mabs, self.entry_hoten, self.entry_chuyenkhoa, self.entry_sdt, self.entry_makhoa]:
            entry.config(state="normal")
            entry.delete(0, tk.END)

    # --- TẢI DỮ LIỆU ---
    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        conn = self.connect_db()
        if not conn:
            return
        cur = conn.cursor()
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
        makhoa = self.entry_makhoa.get().strip()

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
        self.entry_hoten.insert(0, values[1])
        self.entry_chuyenkhoa.insert(0, values[2])
        self.entry_sdt.insert(0, values[3])
        self.entry_makhoa.insert(0, values[4])
        self.entry_mabs.config(state="readonly")

    # --- LƯU ---
    def luu_bs(self):
        mabs = self.entry_mabs.get().strip()
        hoten = self.entry_hoten.get().strip()
        chuyenkhoa = self.entry_chuyenkhoa.get().strip()
        sdt = self.entry_sdt.get().strip()
        makhoa = self.entry_makhoa.get().strip()

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
        tk.Label(self, text="QUẢN LÝ BÁC SĨ", font=FONT_TITLE, fg=COLOR_MAIN, bg=BG_LIGHT).pack(pady=10)

        # Frame thông tin
        frame_info = tk.Frame(self, bg=BG_INFO_FRAME)
        frame_info.pack(pady=5, padx=20, fill="x")

        # Dòng 1
        tk.Label(frame_info, text="Mã bác sĩ:", fg=COLOR_MAIN, font=FONT_LABEL, bg=BG_INFO_FRAME).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_mabs = tk.Entry(frame_info, width=20)
        self.entry_mabs.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_info, text="Họ tên:", fg=COLOR_MAIN, font=FONT_LABEL, bg=BG_INFO_FRAME).grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.entry_hoten = tk.Entry(frame_info, width=30)
        self.entry_hoten.grid(row=0, column=3, padx=5, pady=5)

        # Dòng 2
        tk.Label(frame_info, text="Chuyên khoa:", fg=COLOR_MAIN, font=FONT_LABEL, bg=BG_INFO_FRAME).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_chuyenkhoa = tk.Entry(frame_info, width=25)
        self.entry_chuyenkhoa.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_info, text="SĐT:", fg=COLOR_MAIN, font=FONT_LABEL, bg=BG_INFO_FRAME).grid(row=1, column=2, sticky="e", padx=5, pady=5)
        self.entry_sdt = tk.Entry(frame_info, width=30)
        self.entry_sdt.grid(row=1, column=3, padx=5, pady=5)

        # Dòng 3
        tk.Label(frame_info, text="Mã khoa:", fg=COLOR_MAIN, font=FONT_LABEL, bg=BG_INFO_FRAME).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.entry_makhoa = tk.Entry(frame_info, width=20)
        self.entry_makhoa.grid(row=2, column=1, padx=5, pady=5)

        # Frame nút
        frame_btn = tk.Frame(self, bg=BG_LIGHT)
        frame_btn.pack(pady=15)
        btn_conf = {"width": 8, "fg": "white", "bg": BG_BUTTON, "font": FONT_LABEL}
        tk.Button(frame_btn, text="Thêm", command=self.them_bs, **btn_conf).grid(row=0, column=0, padx=10)
        tk.Button(frame_btn, text="Lưu", command=self.luu_bs, **btn_conf).grid(row=0, column=1, padx=10)
        tk.Button(frame_btn, text="Sửa", command=self.sua_bs, **btn_conf).grid(row=0, column=2, padx=10)
        tk.Button(frame_btn, text="Hủy", command=self.clear_input, **btn_conf).grid(row=0, column=3, padx=10)
        tk.Button(frame_btn, text="Xóa", command=self.xoa_bs, **btn_conf).grid(row=0, column=4, padx=10)
        tk.Button(frame_btn, text="Thoát", command=self.quit_window, **btn_conf).grid(row=0, column=5, padx=10)

        # Treeview
        lbl_ds = tk.Label(self, text="Danh sách bác sĩ", fg=COLOR_MAIN, font=FONT_LABEL, bg=BG_LIGHT)
        lbl_ds.pack(pady=5, anchor="w", padx=15)

        columns = ("mabs", "hoten", "chuyenkhoa", "sdt", "makhoa")
        headings = ["Mã BS", "Họ và tên", "Chuyên khoa", "SĐT", "Mã khoa"]
        widths = [100, 200, 180, 120, 100]

        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=12)

        style = ttk.Style()
        style.configure("Treeview", font=("Times New Roman", 12))
        style.configure("Treeview.Heading", font=("Times New Roman", 13, "bold"))
        style.map("Treeview", background=[("selected", COLOR_MAIN)], foreground=[("selected", "white")])

        for col, head, w in zip(columns, headings, widths):
            self.tree.heading(col, text=head)
            self.tree.column(col, width=w, anchor="center")

        self.tree.pack(padx=15, pady=5, fill="both", expand=True)
        self.tree.tag_configure('evenrow', background="#fff0f0")  # hồng nhạt
        self.tree.tag_configure('oddrow', background="#ffffff")

    # --- THOÁT ---
    def quit_window(self):
        
            self.master.destroy()
            self.main_root.deiconify()

# --- CHẠY CHƯƠNG TRÌNH ---
'''
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Quản lý bác sĩ")
    root.geometry("900x600")
    app = QuanLyBacSi(root, connect_db, root)
    app.pack(fill="both", expand=True)
    root.mainloop()
'''
