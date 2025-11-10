import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# --- KẾT NỐI DATABASE (Định nghĩa Global) ---
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="071005",  # đổi nếu cần
            database="qlbenhnhan"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi kết nối", f"Không thể kết nối MySQL: {err}")
        return None

# --- LỚP QUẢN LÝ DỊCH VỤ ---
class QuanLyDichVu(tk.Frame):
    def __init__(self, master, connect_db_func, parent_root=None):
        super().__init__(master)
        self.connect_db = connect_db_func
        self.parent_root = parent_root
        self.configure(bg="#fff5f5")

        # ===== Khai báo biến =====
        self.entry_madv = None
        self.entry_tendv = None
        self.entry_dongia = None
        self.cb_donvitinh = None
        self.cb_loaihinh = None
        self.entry_tonkho = None
        self.entry_ghichu = None
        self.entry_search = None
        self.tree = None

        # **BẮT BUỘC PHẢI GỌI**
        self.create_widgets()  # <- thêm dòng này
        self.load_data()       # <- nếu muốn load dữ liệu ngay khi mở form

    # Định dạng đơn giá khi hiển thị
    def format_money(self, value):
        try:
            value = float(value)
            return f"{value:,.0f}"
        except:
            return value

    # Xóa định dạng tiền để lưu DB
    def unformat_money(self, formatted):
        return formatted.replace(",", "")

    # --- HIỆN / ẨN TỒN KHO TUY THEO LOẠI HÌNH ---
    def change_loaihinh(self, event):
        loai = self.cb_loaihinh.get()
        self.entry_tonkho.delete(0, tk.END)
        if loai == "Thuốc":
            self.entry_tonkho.config(state="normal")
        else:
            self.entry_tonkho.config(state="disabled")
    
    # --- XÓA INPUT ---
    def clear_input(self):
        self.entry_madv.config(state="normal") 
        
        for widget in [self.entry_madv, self.entry_tendv, self.entry_dongia, self.cb_donvitinh, self.cb_loaihinh]:
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, ttk.Combobox):
                widget.set("")
                
        self.entry_ghichu.delete("1.0", tk.END)
        
        self.entry_tonkho.delete(0, tk.END)
        self.entry_tonkho.config(state="disabled")
        self.entry_madv.config(state="normal")

    # --- TẢI DỮ LIỆU ---
    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        conn = self.connect_db()
        if not conn: return
        cur = conn.cursor()
        
        try:
            cur.execute("SELECT madv, tendv, dongia, donvitinh, loaihinh, tonkho, ghichu FROM dichvu")
            rows = cur.fetchall()
        except mysql.connector.Error as err:
            if err.errno == 1146:
                 rows = []
            else:
                 messagebox.showerror("Lỗi Truy Vấn", str(err))
                 return
                 
        for i, row in enumerate(rows):
            row = list(row)
            row[2] = self.format_money(row[2])
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", tk.END, values=row, tags=(tag,))
        conn.close()

    # --- TÌM KIẾM ---
    def tim_kiem(self):
        keyword = self.entry_search.get().strip()
        for i in self.tree.get_children():
            self.tree.delete(i)

        conn = self.connect_db()
        if not conn: return
        cur = conn.cursor()
        query = """
            SELECT madv, tendv, dongia, donvitinh, loaihinh, tonkho, ghichu
            FROM dichvu
            WHERE madv LIKE %s OR tendv LIKE %s
        """
        like_str = f"%{keyword}%"
        cur.execute(query, (like_str, like_str))
        rows = cur.fetchall()

        for i, row in enumerate(rows):
            row = list(row)
            row[2] = self.format_money(row[2])
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", tk.END, values=row, tags=(tag,))
        conn.close()

    # --- THÊM ---
    def them_dichvu(self):
        madv = self.entry_madv.get().strip()
        tendv = self.entry_tendv.get().strip()
        dongia = self.unformat_money(self.entry_dongia.get().strip())
        donvitinh = self.cb_donvitinh.get().strip()
        loaihinh = self.cb_loaihinh.get().strip()
        tonkho = self.entry_tonkho.get().strip() or 0
        ghichu = self.entry_ghichu.get("1.0", tk.END).strip()

        if not madv or not tendv or not loaihinh or not dongia:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ Mã DV, Tên DV, Loại hình và Đơn giá.")
            return

        conn = self.connect_db()
        if not conn: return
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO dichvu (madv, tendv, dongia, donvitinh, loaihinh, tonkho, ghichu) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (madv, tendv, dongia, donvitinh or None, loaihinh, tonkho, ghichu or None)
            )
            conn.commit()
            messagebox.showinfo("Thành công", "Đã thêm dịch vụ mới.")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Không thể thêm dịch vụ: {err}")
        finally:
            conn.close()
        self.load_data()
        self.clear_input()

    # --- SỬA ---
    def sua_dichvu(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn dịch vụ để sửa.")
            return
        values = self.tree.item(selected)["values"]
        
        # Tắt sự kiện và xóa input
        self.cb_loaihinh.unbind("<<ComboboxSelected>>")
        self.clear_input() 
        
        self.entry_madv.insert(0, values[0])
        self.entry_tendv.insert(0, values[1])
        self.entry_dongia.insert(0, self.unformat_money(values[2]))
        self.cb_donvitinh.set(values[3])
        self.cb_loaihinh.set(values[4])
        self.entry_ghichu.insert("1.0", values[6])
        self.entry_madv.config(state="readonly")

        # LOGIC TỒN KHO ĐÃ SỬA LỖI
        loaihinh_current = values[4]
        tonkho_value = values[5]
        
        if loaihinh_current == "Thuốc":
            self.entry_tonkho.config(state="normal")
            self.entry_tonkho.insert(0, tonkho_value)
        else:
            self.entry_tonkho.delete(0, tk.END)
            self.entry_tonkho.config(state="disabled")

        # Bật lại sự kiện
        self.cb_loaihinh.bind("<<ComboboxSelected>>", self.change_loaihinh)

    # --- LƯU ---
    def luu_dichvu(self):
        madv = self.entry_madv.get().strip()
        tendv = self.entry_tendv.get().strip()
        dongia = self.unformat_money(self.entry_dongia.get().strip())
        donvitinh = self.cb_donvitinh.get().strip()
        loaihinh = self.cb_loaihinh.get().strip()
        tonkho = self.entry_tonkho.get().strip() or 0
        ghichu = self.entry_ghichu.get("1.0", tk.END).strip()

        conn = self.connect_db()
        if not conn: return
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE dichvu
                SET tendv=%s, dongia=%s, donvitinh=%s, loaihinh=%s, tonkho=%s, ghichu=%s
                WHERE madv=%s
            """, (tendv, dongia, donvitinh or None, loaihinh, tonkho, ghichu or None, madv))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã cập nhật dịch vụ.")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Không thể lưu thay đổi: {err}")
        finally:
            conn.close()
        self.load_data()
        self.clear_input()
    def close_form(self):
        """Đóng form con và hiện lại form cha"""
        self.master.destroy()
        if self.parent_root:
            self.parent_root.deiconify()  # hiện lại form chính


    # --- XÓA ---
    def xoa_dichvu(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn dịch vụ để xóa.")
            return
        madv = self.tree.item(selected)["values"][0]
        if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa dịch vụ: {madv}?"):
            return

        conn = self.connect_db()
        if not conn: return
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM dichvu WHERE madv=%s", (madv,))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã xóa dịch vụ.")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Không thể xóa dịch vụ: {err}")
        finally:
            conn.close()
        self.load_data()
        self.clear_input()

    # --- GIAO DIỆN ---
    def create_widgets(self):
        # MÀU CHỦ ĐẠO ĐỎ TƯƠNG TỰ QUẢN LÝ PHÒNG
        COLOR_MAIN = "#a80000" 
        BG_LIGHT = "#fff5f5" 
        BG_INFO_FRAME = "#fcdada" 
        BG_BUTTON_FRAME = "#f9dcdc"
        BG_BUTTON = "#fd6f6f"
        
        FONT_LABEL = ("Times New Roman", 13, "bold")

        tk.Label(self, text="QUẢN LÝ DỊCH VỤ", font=("Times New Roman", 22, "bold"),
                 fg=COLOR_MAIN, bg=BG_LIGHT).pack(pady=10)
        BTN_COLOR3 = "#faad14"    # vàng đậm cho nút           

        # Định nghĩa Frame Thông tin (LabelFrame)
        frame_info = tk.LabelFrame(self, text="Thông tin dịch vụ", font=FONT_LABEL, bg=BG_INFO_FRAME,
                                    fg=COLOR_MAIN, padx=10, pady=10, bd=2, relief="groove")
        frame_info.pack(pady=10, padx=40, fill="x")

        # Khai báo Labels
        tk.Label(frame_info, text="Mã DV:", font=FONT_LABEL, bg=BG_INFO_FRAME).grid(row=0, column=0, sticky="e", padx=8, pady=6)
        tk.Label(frame_info, text="Tên DV:", font=FONT_LABEL, bg=BG_INFO_FRAME).grid(row=0, column=2, sticky="e", padx=8, pady=6)
        tk.Label(frame_info, text="Đơn giá:", font=FONT_LABEL, bg=BG_INFO_FRAME).grid(row=1, column=0, sticky="e", padx=8, pady=6)
        tk.Label(frame_info, text="Đơn vị tính:", font=FONT_LABEL, bg=BG_INFO_FRAME).grid(row=1, column=2, sticky="e", padx=8, pady=6)
        tk.Label(frame_info, text="Loại hình:", font=FONT_LABEL, bg=BG_INFO_FRAME).grid(row=2, column=0, sticky="e", padx=8, pady=6)
        tk.Label(frame_info, text="Tồn kho:", font=FONT_LABEL, bg=BG_INFO_FRAME).grid(row=2, column=2, sticky="e", padx=8, pady=6)
        tk.Label(frame_info, text="Ghi chú:", font=FONT_LABEL, bg=BG_INFO_FRAME).grid(row=3, column=0, sticky="ne", padx=8, pady=6)

        # Khai báo Entries/Combobox/Text
        self.entry_madv = tk.Entry(frame_info, font=("Times New Roman", 12))
        self.entry_tendv = tk.Entry(frame_info, font=("Times New Roman", 12))
        self.entry_dongia = tk.Entry(frame_info, font=("Times New Roman", 12))
        self.entry_tonkho = tk.Entry(frame_info, font=("Times New Roman", 12))
        self.entry_ghichu = tk.Text(frame_info, font=("Times New Roman", 12), height=3, width=50)

        self.cb_donvitinh = ttk.Combobox(frame_info, font=("Times New Roman", 12), state="readonly",
                                          values=["Lần", "Lọ", "Gói", "Viên"])
        self.cb_loaihinh = ttk.Combobox(frame_info, font=("Times New Roman", 12), state="readonly",
                                         values=["Khám bệnh", "Xét nghiệm", "Dịch vụ khác", "Thanh toán", "Thuốc", "Tư vấn", "Cấp cứu"])

        # Đặt vị trí Entries
        self.entry_madv.grid(row=0, column=1, padx=8, pady=6)
        self.entry_tendv.grid(row=0, column=3, padx=8, pady=6)
        self.entry_dongia.grid(row=1, column=1, padx=8, pady=6)
        self.cb_donvitinh.grid(row=1, column=3, padx=8, pady=6)
        self.cb_loaihinh.grid(row=2, column=1, padx=8, pady=6)
        self.entry_tonkho.grid(row=2, column=3, padx=8, pady=6)
        self.entry_ghichu.grid(row=3, column=1, columnspan=3, padx=8, pady=6, sticky="we")

        self.entry_tonkho.config(state="disabled")

        self.cb_loaihinh.bind("<<ComboboxSelected>>", self.change_loaihinh)

        # === KHUNG CHỨC NĂNG NÚT ===
        frame_btn = tk.LabelFrame(self, text="Chức năng", font=FONT_LABEL, bg=BG_BUTTON_FRAME,
                                     fg=COLOR_MAIN, padx=10, pady=10, bd=2, relief="groove")
        frame_btn.pack(pady=5, padx=15, fill="x")

        btn_conf = {"font": ("Times New Roman", 12, "bold"), "bg": BG_BUTTON, "fg": "white", "width": 12}
        
        # Các nút CRUD
        # Nút CRUD, Hủy, Thoát với tone đỏ giống quản lý bác sĩ
        btn_conf = {"font": ("Times New Roman", 12, "bold"), "bg":"#a80000" , "fg": "white", "width": 12, "activebackground": "#a80000", "activeforeground": "white"}

        tk.Button(frame_btn, text="Thêm", command=self.them_dichvu, **btn_conf).grid(row=0, column=0, padx=15, pady=5)
        tk.Button(frame_btn, text="Sửa", command=self.sua_dichvu, **btn_conf).grid(row=0, column=1, padx=15, pady=5)
        tk.Button(frame_btn, text="Lưu", command=self.luu_dichvu, **btn_conf).grid(row=0, column=2, padx=15, pady=5)
        tk.Button(frame_btn, text="Xóa", command=self.xoa_dichvu, **btn_conf).grid(row=0, column=3, padx=15, pady=5)
        tk.Button(frame_btn, text="Hủy", command=self.clear_input, **btn_conf).grid(row=0, column=4, padx=15, pady=5)
        tk.Button(frame_btn, text="Thoát", command=self.close_form, **btn_conf).grid(row=0, column=5, padx=15, pady=5)


       

        # === TÌM KIẾM ===
        
        search_frame = tk.Frame(self, bg=BG_LIGHT)
        search_frame.pack(fill="x", padx=15, pady=(5, 0))

        tk.Label(search_frame, text="Tìm kiếm:", font=FONT_LABEL, bg=BG_LIGHT).pack(side="left", padx=5)
        self.entry_search = tk.Entry(search_frame, font=("Times New Roman", 12), width=30)
        self.entry_search.pack(side="left", padx=5)

        # Cấu hình nút tìm kiếm màu vàng đậm
        search_btn_conf = {
            "font": ("Times New Roman", 12, "bold"),
            "bg": "#faad14",           # vàng đậm
            "fg": "white",
            "activebackground": "#d99800",  # vàng đậm hơn khi click
            "activeforeground": "white",
            "width": 12
        }

        tk.Button(search_frame, text="Tìm kiếm", command=self.tim_kiem, **search_btn_conf).pack(side="left", padx=5)


            
                
        # === BẢNG DANH SÁCH ===
               
        columns = ("madv", "tendv", "dongia", "donvitinh", "loaihinh", "tonkho", "ghichu")
        headers = ["Mã dịch vụ", "Tên dịch vụ", "Đơn giá", "Đơn vị tính", "Loại hình", "Tồn kho", "Ghi chú"]
        widths = [100, 200, 120, 100, 130, 80, 350]

        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)

        # Scrollbar dọc
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        # Cấu hình các cột
        for col, header, w in zip(columns, headers, widths):
            self.tree.heading(col, text=header)
            self.tree.column(col, anchor="center", width=w)

# --- CHẠY ---
'''if __name__ == "__main__":
    root = tk.Tk()
    root.title("Quản lý Dịch vụ")
    root.geometry("1100x650")
    # Khởi tạo ứng dụng
    app = QuanLyDichVu(root, connect_db)
    app.pack(fill="both", expand=True)
    root.mainloop()'''