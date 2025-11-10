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
        messagebox.showerror("Lỗi Kết Nối Database", f"Không thể kết nối MySQL: {err}")
        return None

# --- CĂN GIỮA CỬA SỔ ---
def center_window(window, width=1100, height=650):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

# --- LỚP QUẢN LÝ NHẬP VIỆN ---
class QuanLyNhapVien(tk.Frame):
    def __init__(self, master, connect_db_func):
        super().__init__(master)
        self.connect_db = connect_db_func

        # ===== MÀU GIAO DIỆN GIỐNG FILE QUẢN LÝ DỊCH VỤ =====
        self.COLOR_MAIN = "#a80000"         # màu đỏ chủ đạo
        self.BG_LIGHT = "#fff5f5"           # nền tổng thể hồng nhạt
        self.BG_INFO_FRAME = "#fcdada"      # frame thông tin
        self.BG_BUTTON_FRAME = "#f9dcdc"    # frame nút
        self.BG_BUTTON = "#fd6f6f"          # nút màu đỏ
        self.FONT_LABEL = ("Times New Roman", 13, "bold")
        self.FONT_BTN = ("Times New Roman", 12, "bold")
        self.configure(bg=self.BG_LIGHT)
      

        self.BTN_COLOR_MAIN = "#a80000"
        self.BTN_HOVER_MAIN = "#d32f2f"
        self.BTN_COLOR_SEARCH = "#faad14"
        self.BTN_HOVER_SEARCH = "#ffc53d"

        
        self.create_widgets()
        self.load_data()

    # --- LẤY DỮ LIỆU CHO COMBOBOX ---
    def load_combobox_values(self):
        conn = self.connect_db()
        if not conn:
            return [], [], []
        cur = conn.cursor()
        cur.execute("SELECT mabn FROM benhnhan")
        mabn_list = [row[0] for row in cur.fetchall()]
        cur.execute("SELECT mabs FROM bacsi")
        mabs_list = [row[0] for row in cur.fetchall()]
        cur.execute("SELECT maphong FROM phong")
        maphong_list = [row[0] for row in cur.fetchall()]
        conn.close()
        return mabn_list, mabs_list, maphong_list

    # --- XÓA INPUT ---
    def clear_input(self):
        for entry in [self.entry_stt, self.cb_mabn, self.entry_chandoan, self.entry_ghichu]:
            entry.config(state="normal")
            if isinstance(entry, ttk.Combobox):
                entry.set("")
            else:
                entry.delete(0, tk.END)
        self.cb_loaihinh.set("")
        self.cb_mabs.set("")
        self.cb_maphong.set("")
        self.date_ngaynhap.set_date(datetime.date.today())
        self.date_ngayxuat.set_date(datetime.date.today())

    # --- ĐÓNG FORM ---
    def close_form(self):
        self.master.destroy()
        if hasattr(self.master, "master"):
            self.master.master.deiconify()

    # --- TẢI DỮ LIỆU ---
    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        conn = self.connect_db()
        if not conn:
            return
        cur = conn.cursor()
        cur.execute("SELECT stt, mabn, ngaynhap, ngayxuat, loaihinh, chandoan, ghichu, mabs, maphong FROM nhapvien")
        rows = cur.fetchall()
        for row in rows:
            row_list = list(row)
            for idx in [2,3]:
                if isinstance(row_list[idx], datetime.date):
                    row_list[idx] = row_list[idx].strftime("%d/%m/%Y")
            self.tree.insert("", tk.END, values=row_list)
        conn.close()

    # --- TÌM KIẾM ---
    def tim_kiem(self):
        keyword = self.entry_search.get().strip()
        if not keyword:
            messagebox.showwarning("Chưa nhập", "Vui lòng nhập Mã BN để tìm kiếm!")
            return
        for i in self.tree.get_children():
            self.tree.delete(i)
        conn = self.connect_db()
        if not conn:
            return
        cur = conn.cursor()
        query = """
            SELECT stt, mabn, ngaynhap, ngayxuat, loaihinh, chandoan, ghichu, mabs, maphong
            FROM nhapvien
            WHERE mabn LIKE %s
        """
        cur.execute(query, (f"%{keyword}%",))
        rows = cur.fetchall()
        for row in rows:
            row_list = list(row)
            for idx in [2,3]:
                if isinstance(row_list[idx], datetime.date):
                    row_list[idx] = row_list[idx].strftime("%d/%m/%Y")
            self.tree.insert("", tk.END, values=row_list)
        conn.close()

    # --- THÊM NHẬP VIỆN ---
    def them_nhapvien(self):
        stt = self.entry_stt.get().strip()
        mabn = self.cb_mabn.get().strip()
        loaihinh = self.cb_loaihinh.get().strip()
        chandoan = self.entry_chandoan.get().strip()
        ghichu = self.entry_ghichu.get().strip()
        mabs = self.cb_mabs.get().strip()
        maphong = self.cb_maphong.get().strip()
        try:
            ngaynhap = datetime.datetime.strptime(self.date_ngaynhap.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
            ngayxuat = datetime.datetime.strptime(self.date_ngayxuat.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Lỗi ngày", "Ngày nhập/xuất không hợp lệ!")
            return
        if not stt or not mabn or not loaihinh:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ STT, Mã BN và Loại hình")
            return
        conn = self.connect_db()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO nhapvien (stt, mabn, ngaynhap, ngayxuat, loaihinh, chandoan, ghichu, mabs, maphong)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (stt, mabn, ngaynhap, ngayxuat, loaihinh, chandoan, ghichu, mabs or None, maphong or None))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã thêm nhập viện mới.")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Không thể thêm: {err}")
        finally:
            conn.close()
        self.load_data()
        self.clear_input()

    # --- SỬA NHẬP VIỆN ---
    def sua_nhapvien(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn nhập viện để sửa.")
            return
        values = self.tree.item(selected)["values"]
        self.clear_input()
        self.entry_stt.insert(0, values[0])
        self.entry_stt.config(state="readonly")
        self.cb_mabn.set(values[1])
        self.cb_loaihinh.set(values[4])
        self.entry_chandoan.insert(0, values[5])
        self.entry_ghichu.insert(0, values[6])
        self.cb_mabs.set(values[7])
        self.cb_maphong.set(values[8])
        if values[2]:
            self.date_ngaynhap.set_date(datetime.datetime.strptime(values[2], "%d/%m/%Y"))
        if values[3]:
            self.date_ngayxuat.set_date(datetime.datetime.strptime(values[3], "%d/%m/%Y"))

    # --- LƯU NHẬP VIỆN ---
    def luu_nhapvien(self):
        stt = self.entry_stt.get().strip()
        mabn = self.cb_mabn.get().strip()
        loaihinh = self.cb_loaihinh.get().strip()
        chandoan = self.entry_chandoan.get().strip()
        ghichu = self.entry_ghichu.get().strip()
        mabs = self.cb_mabs.get().strip()
        maphong = self.cb_maphong.get().strip()
        try:
            ngaynhap = datetime.datetime.strptime(self.date_ngaynhap.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
            ngayxuat = datetime.datetime.strptime(self.date_ngayxuat.get(), "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Lỗi ngày", "Ngày nhập/xuất không hợp lệ!")
            return
        conn = self.connect_db()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE nhapvien
                SET ngaynhap=%s, ngayxuat=%s, loaihinh=%s, chandoan=%s, ghichu=%s, mabs=%s, maphong=%s
                WHERE stt=%s AND mabn=%s
            """, (ngaynhap, ngayxuat, loaihinh, chandoan, ghichu, mabs or None, maphong or None, stt, mabn))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã cập nhật nhập viện.")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Không thể lưu: {err}")
        finally:
            conn.close()
        self.load_data()
        self.clear_input()

    # --- XÓA NHẬP VIỆN ---
    def xoa_nhapvien(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn nhập viện để xóa.")
            return
        stt, mabn = self.tree.item(selected)["values"][:2]
        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa nhập viện STT {stt}, BN {mabn}?"):
            return
        conn = self.connect_db()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM nhapvien WHERE stt=%s AND mabn=%s", (stt, mabn))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã xóa nhập viện.")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Không thể xóa: {err}")
        finally:
            conn.close()
        self.load_data()
        self.clear_input()

    # --- GIAO DIỆN ---
    def create_widgets(self):
        # TIÊU ĐỀ
        
        tk.Label(self, text="QUẢN LÝ NHẬP VIỆN", font=("Times New Roman", 22, "bold"),
                 fg=self.COLOR_MAIN, bg=self.BG_LIGHT).pack(pady=10)

        # TÌM KIẾM
         # --- TÌM KIẾM ---
        search_frame = tk.Frame(self, bg=self.BG_LIGHT)
        search_frame.pack(fill="x", padx=15, pady=5)

        tk.Label(search_frame, text="Tìm kiếm theo Mã BN:", font=self.FONT_LABEL, bg=self.BG_LIGHT).pack(side="left")
        self.entry_search = tk.Entry(search_frame, font=("Times New Roman",12), width=30)
        self.entry_search.pack(side="left", padx=5)
        btn_search = tk.Button(search_frame, text="Tìm Kiếm", command=self.tim_kiem,
                               font=self.FONT_BTN, bg=self.BTN_COLOR_SEARCH, fg="white",
                               width=10, relief="ridge", cursor="hand2")
        btn_search.pack(side="left", padx=5)

        # Hiệu ứng hover vàng
        btn_search.bind("<Enter>", lambda e: btn_search.config(bg=self.BTN_HOVER_SEARCH))
        btn_search.bind("<Leave>", lambda e: btn_search.config(bg=self.BTN_COLOR_SEARCH))
        
        # THÔNG TIN NHẬP VIỆN
        frame_info = tk.LabelFrame(self, text="Thông tin nhập viện", font=self.FONT_LABEL,
                                   bg=self.BG_INFO_FRAME, fg=self.COLOR_MAIN, padx=10, pady=10)
        frame_info.pack(padx=15, pady=10, fill="x")

        labels = ["STT","Mã BN","Ngày nhập","Ngày xuất","Loại hình","Chẩn đoán","Mã phòng","Mã BS","Ghi chú"]
        for i, text in enumerate(labels):
            tk.Label(frame_info, text=text+":", font=self.FONT_LABEL, bg=self.BG_INFO_FRAME).grid(
                row=i//2, column=(i%2)*2, padx=8, pady=6, sticky="e"
            )

        self.entry_stt = tk.Entry(frame_info, font=("Times New Roman", 12))
        self.entry_stt.grid(row=0, column=1, padx=8, pady=6)

        mabn_list, mabs_list, maphong_list = self.load_combobox_values()
        self.cb_mabn = ttk.Combobox(frame_info, font=("Times New Roman",12), state="readonly", values=mabn_list)
        self.cb_mabn.grid(row=0, column=3, padx=8, pady=6)

        self.date_ngaynhap = DateEntry(frame_info, font=("Times New Roman",12), date_pattern="dd/mm/yyyy")
        self.date_ngaynhap.grid(row=1, column=1, padx=8, pady=6)
        self.date_ngayxuat = DateEntry(frame_info, font=("Times New Roman",12), date_pattern="dd/mm/yyyy")
        self.date_ngayxuat.grid(row=1, column=3, padx=8, pady=6)

        self.cb_loaihinh = ttk.Combobox(frame_info, font=("Times New Roman",12), state="readonly",
                                        values=["Nội trú","Ngoại trú"])
        self.cb_loaihinh.grid(row=2, column=1, padx=8, pady=6)

        self.entry_chandoan = tk.Entry(frame_info, font=("Times New Roman",12))
        self.entry_chandoan.grid(row=2, column=3, padx=8, pady=6)

        self.cb_maphong = ttk.Combobox(frame_info, font=("Times New Roman",12), state="readonly", values=maphong_list)
        self.cb_maphong.grid(row=3, column=1, padx=8, pady=6)

        self.cb_mabs = ttk.Combobox(frame_info, font=("Times New Roman",12), state="readonly", values=mabs_list)
        self.cb_mabs.grid(row=3, column=3, padx=8, pady=6)

        self.entry_ghichu = tk.Entry(frame_info, font=("Times New Roman",12), width=70)
        self.entry_ghichu.grid(row=4, column=1, columnspan=3, padx=8, pady=6, sticky="w")

        # NÚT CHỨC NĂNG
        # --- KHUNG NÚT CHỨC NĂNG ---
        frame_btn = tk.Frame(self, bg=self.BG_BUTTON_FRAME)
        frame_btn.pack(pady=5)

        btn_conf = {
            "font": self.FONT_BTN,
            "bg":self.BTN_COLOR_MAIN,
            "fg": "white",
            "width": 10,
            "relief": "ridge",
            "cursor": "hand2"
        }

        btn_names = ["Thêm", "Sửa", "Lưu", "Xóa", "Hủy", "Thoát"]
        btn_cmds = [
            self.them_nhapvien,
            self.sua_nhapvien,
            self.luu_nhapvien,
            self.xoa_nhapvien,
            self.clear_input,
            self.close_form
        ]

        for i, (name, cmd) in enumerate(zip(btn_names, btn_cmds)):
            btn = tk.Button(frame_btn, text=name, command=cmd, **btn_conf)
            btn.grid(row=0, column=i, padx=6, pady=5)

            # Hiệu ứng hover đỏ
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.BTN_HOVER_MAIN))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.BTN_COLOR_MAIN))
        

        # ===== TREEVIEW =====
       
        lbl_ds = tk.Label(self, text="Danh sách nhập viện", fg=self.COLOR_MAIN, font=self.FONT_LABEL, bg=self.BG_LIGHT)
        lbl_ds.pack(pady=5, anchor="w", padx=15)

        columns = ("stt","mabn","ngaynhap","ngayxuat","loaihinh","chandoan","ghichu","mabs","maphong")
        headings = ["STT","Mã BN","Ngày nhập","Ngày xuất","Loại hình","Chẩn đoán","Ghi chú","Mã BS","Mã phòng"]
        widths = [50,80,100,100,100,150,150,80,80]

        # Tạo frame chứa Treeview và Scrollbar
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)

        style = ttk.Style()
        style.configure("Treeview", font=("Times New Roman", 12))
        style.configure("Treeview.Heading", font=("Times New Roman", 13, "bold"))
        style.map("Treeview", background=[("selected", self.COLOR_MAIN)], foreground=[("selected", "white")])

        for col, head, w in zip(columns, headings, widths):
            self.tree.heading(col, text=head)
            self.tree.column(col, width=w, anchor="center")

        # Scrollbar dọc
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

# --- CHẠY CHƯƠNG TRÌNH ---
'''
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Quản lý Nhập Viện")
    center_window(root, 1100, 650)
    app = QuanLyNhapVien(master=root, connect_db_func=connect_db)
    app.pack(fill="both", expand=True)
    root.mainloop()'''
