import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from tkcalendar import DateEntry
import datetime

# --- KẾT NỐI DATABASE ---
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="071005",
            database="qlbenhnhan"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi", f"Không thể kết nối MySQL: {err}")
        return None

# --- LỚP QUẢN LÝ THANH TOÁN ---
class QuanLyThanhToan(tk.Frame):
    def __init__(self, master, connect_db_func, parent_root=None):
        super().__init__(master)
        self.connect_db = connect_db_func
        self.parent_root = parent_root

        self.var_trangthai = tk.StringVar(value="Chưa thanh toán")
        self.cb_mabn = None
        self.cb_madv = None
        self.entry_mahd = None
        self.date_entry_ngaylap = None
        self.entry_tongtien = None
        self.entry_soluong = None
        self.tree_cthd = None

        self.create_widgets()
        self.load_benhnhan()
        self.load_dichvu()

    # --- FORMAT TIỀN ---
    def format_money(self, value):
        try:
            return f"{float(value):,.0f} VNĐ"
        except:
            return value

    def unformat_money(self, formatted):
        return float(str(formatted).replace(",", "").replace(" VNĐ", "").strip() or 0)

    # --- LOAD COMBOBOX ---
    def load_benhnhan(self):
        conn = self.connect_db()
        if not conn: return
        cur = conn.cursor()
        try:
            cur.execute("SELECT mabn FROM benhnhan")
            rows = [r[0] for r in cur.fetchall()]
            self.cb_mabn["values"] = rows
        except mysql.connector.Error as err:
            if err.errno != 1146: messagebox.showerror("Lỗi", str(err))
        conn.close()

    def load_dichvu(self):
        conn = self.connect_db()
        if not conn: return
        cur = conn.cursor()
        try:
            cur.execute("SELECT madv FROM dichvu")
            rows = [r[0] for r in cur.fetchall()]
            self.cb_madv["values"] = rows
        except mysql.connector.Error as err:
            if err.errno != 1146: messagebox.showerror("Lỗi", str(err))
        conn.close()

    # --- LẤY GIÁ DỊCH VỤ ---
    def get_service_info(self, madv):
        conn = self.connect_db()
        if not conn: return None, 0
        cur = conn.cursor()
        cur.execute("SELECT tendv, dongia FROM dichvu WHERE madv=%s", (madv,))
        result = cur.fetchone()
        conn.close()
        if result:
            return result[0], float(result[1])
        return None, 0

    # --- RESET FORM ---
    def clear_input(self):
        self.entry_mahd.config(state="normal")
        self.entry_mahd.delete(0, tk.END)
        self.cb_mabn.set("")
        self.cb_madv.set("")
        self.date_entry_ngaylap.set_date(datetime.date.today())
        self.entry_soluong.delete(0, tk.END)
        self.entry_tongtien.config(state="normal")
        self.entry_tongtien.delete(0, tk.END)
        self.entry_tongtien.insert(0, self.format_money(0))
        self.entry_tongtien.config(state="readonly")
        self.var_trangthai.set("Chưa thanh toán")
        for i in self.tree_cthd.get_children():
            self.tree_cthd.delete(i)

    # --- LOAD CHI TIẾT HÓA ĐƠN ---
    def load_cthd(self, mahd):
        conn = self.connect_db()
        if not conn: return 0
        cur = conn.cursor()
        for i in self.tree_cthd.get_children():
            self.tree_cthd.delete(i)
        query = """SELECT c.id_ct, c.madv, d.tendv, c.soluong, d.dongia, c.thanhtien 
                   FROM ct_hoadon c JOIN dichvu d ON c.madv = d.madv WHERE c.mahd = %s"""
        cur.execute(query, (mahd,))
        rows = cur.fetchall()
        conn.close()
        total = 0
        for row in rows:
            id_ct, madv, tendv, soluong, dongia, thanhtien = row
            self.tree_cthd.insert("", tk.END, values=(id_ct, madv, tendv, soluong, self.format_money(dongia), self.format_money(thanhtien)))
            total += thanhtien
        return total

    # --- THÊM CHI TIẾT DỊCH VỤ ---
    def add_detail(self):
        madv = self.cb_madv.get().strip()
        soluong_str = self.entry_soluong.get().strip()
        if not madv or not soluong_str:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng chọn Mã dịch vụ và nhập Số lượng!")
            return
        try:
            soluong = int(soluong_str)
            if soluong <= 0: raise ValueError
        except ValueError:
            messagebox.showwarning("Lỗi", "Số lượng phải là số nguyên dương.")
            return
        tendv, dongia = self.get_service_info(madv)
        if not tendv:
            messagebox.showerror("Lỗi", f"Không tìm thấy dịch vụ: {madv}")
            return
        thanhtien = soluong * dongia
        id_ct = len(self.tree_cthd.get_children()) + 1
        self.tree_cthd.insert("", tk.END, values=(id_ct, madv, tendv, soluong, self.format_money(dongia), self.format_money(thanhtien)))
        self.update_total()
        self.entry_soluong.delete(0, tk.END)
        self.cb_madv.set("")

    # --- XÓA DỊCH VỤ CHỌN ---
    def delete_detail(self):
        selected = self.tree_cthd.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Chọn dịch vụ muốn xóa trong bảng chi tiết!")
            return
        for item in selected:
            self.tree_cthd.delete(item)
        self.update_total()
        self.renumber_treeview()

    # --- CẬP NHẬT TỔNG TIỀN ---
    def update_total(self):
        total = 0
        for item in self.tree_cthd.get_children():
            thanhtien = self.unformat_money(self.tree_cthd.item(item)["values"][5])
            total += thanhtien
        self.entry_tongtien.config(state="normal")
        self.entry_tongtien.delete(0, tk.END)
        self.entry_tongtien.insert(0, self.format_money(total))
        self.entry_tongtien.config(state="readonly")

    # --- SẮP XẾP LẠI STT ---
    def renumber_treeview(self):
        for idx, item in enumerate(self.tree_cthd.get_children(), start=1):
            values = list(self.tree_cthd.item(item)["values"])
            values[0] = idx
            self.tree_cthd.item(item, values=values)

    # --- SỬA HÓA ĐƠN ---
    def edit_invoice(self):
        mahd = self.entry_mahd.get().strip()
        if not mahd:
            messagebox.showwarning("Thiếu", "Nhập Mã hóa đơn muốn sửa!")
            return
        conn = self.connect_db()
        if not conn: return
        cur = conn.cursor()
        try:
            cur.execute("SELECT mahd, mabn, ngaylap, tongtien, trangthai FROM hoadon WHERE mahd=%s", (mahd,))
            header_row = cur.fetchone()
            if not header_row:
                messagebox.showwarning("Lỗi", f"Không tìm thấy Hóa đơn {mahd}")
                return
            self.clear_input()
            mahd_db, mabn_db, ngaylap_db, tongtien_db, trangthai_db = header_row
            self.entry_mahd.insert(0, mahd_db)
            self.cb_mabn.set(mabn_db)
            self.date_entry_ngaylap.set_date(ngaylap_db)
            self.var_trangthai.set(trangthai_db)
            self.entry_mahd.config(state="readonly")
            total_loaded = self.load_cthd(mahd)
            self.update_total()
            messagebox.showinfo("Thành công", f"Đã tải Hóa đơn {mahd} để chỉnh sửa.")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", str(err))
        finally:
            conn.close()

    # --- LƯU HÓA ĐƠN ---
    def save_invoice(self):
        mahd = self.entry_mahd.get().strip()
        mabn = self.cb_mabn.get().strip()
        ngaylap_obj = self.date_entry_ngaylap.get_date()
        tongtien = self.unformat_money(self.entry_tongtien.get())
        trangthai = self.var_trangthai.get()
        if not mahd or not mabn or not self.tree_cthd.get_children():
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đủ thông tin và dịch vụ!")
            return
        conn = self.connect_db()
        if not conn: return
        cur = conn.cursor()
        try:
            # Nếu HĐ đã tồn tại thì xóa chi tiết cũ và ghi lại
            cur.execute("SELECT 1 FROM hoadon WHERE mahd=%s", (mahd,))
            if cur.fetchone():
                cur.execute("DELETE FROM ct_hoadon WHERE mahd=%s", (mahd,))
                cur.execute("UPDATE hoadon SET mabn=%s, ngaylap=%s, tongtien=%s, trangthai=%s WHERE mahd=%s",
                            (mabn, ngaylap_obj, tongtien, trangthai, mahd))
            else:
                cur.execute("INSERT INTO hoadon (mahd, mabn, ngaylap, tongtien, trangthai) VALUES (%s, %s, %s, %s, %s)",
                            (mahd, mabn, ngaylap_obj, tongtien, trangthai))
            # Lưu chi tiết HĐ
            for item in self.tree_cthd.get_children():
                _, madv, _, soluong, _, thanhtien_formatted = self.tree_cthd.item(item)["values"]
                thanhtien_unformat = self.unformat_money(thanhtien_formatted)
                cur.execute("INSERT INTO ct_hoadon (mahd, madv, soluong, thanhtien) VALUES (%s, %s, %s, %s)",
                            (mahd, madv, soluong, thanhtien_unformat))
            conn.commit()
            messagebox.showinfo("Thành công", f"Đã lưu Hóa đơn {mahd} thành công!")
            self.clear_input()
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", str(err))
        finally:
            conn.close()

    # --- GIAO DIỆN ---
    def create_widgets(self):
        COLOR_MAIN = "#a80000"
        BG_LIGHT = "#fff5f5"
        FONT_LABEL = ("Times New Roman", 13, "bold")
        FONT_TITLE = ("Times New Roman", 22, "bold")

        tk.Label(self, text="QUẢN LÝ THANH TOÁN", font=FONT_TITLE, fg=COLOR_MAIN, bg=BG_LIGHT).pack(pady=10)
        self.configure(bg=BG_LIGHT)

        # Header
        frame_header = tk.LabelFrame(self, text="Thông tin Hóa đơn", font=FONT_LABEL, bg="#fcdada", fg=COLOR_MAIN, padx=10, pady=5, bd=2, relief="groove")
        frame_header.pack(pady=5, padx=15, fill="x")
        tk.Label(frame_header, text="Mã hóa đơn:", font=FONT_LABEL, bg="#fcdada").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_mahd = tk.Entry(frame_header, font=("Times New Roman", 12), width=18)
        self.entry_mahd.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        tk.Label(frame_header, text="Mã bệnh nhân:", font=FONT_LABEL, bg="#fcdada").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.cb_mabn = ttk.Combobox(frame_header, font=("Times New Roman", 12), width=17, state="readonly")
        self.cb_mabn.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        tk.Label(frame_header, text="Ngày lập:", font=FONT_LABEL, bg="#fcdada").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.date_entry_ngaylap = DateEntry(frame_header, width=14, date_pattern="dd/mm/yyyy", font=("Times New Roman", 12))
        self.date_entry_ngaylap.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        tk.Label(frame_header, text="Trạng thái:", font=FONT_LABEL, bg="#fcdada").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.cb_trangthai = ttk.Combobox(frame_header, textvariable=self.var_trangthai, values=["Chưa thanh toán", "Đã thanh toán"], font=("Times New Roman", 12), state="readonly", width=17)
        self.cb_trangthai.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        tk.Label(frame_header, text="TỔNG TIỀN:", font=("Times New Roman", 14, "bold"), fg="green", bg="#fcdada").grid(row=2, column=2, padx=5, pady=5, sticky="e")
        self.entry_tongtien = tk.Entry(frame_header, font=("Times New Roman", 14, "bold"), fg="darkgreen", width=15, justify="right")
        self.entry_tongtien.grid(row=2, column=3, padx=5, pady=5, sticky="w")
        self.entry_tongtien.insert(0, self.format_money(0))
        self.entry_tongtien.config(state='readonly')

        # Chi tiết dịch vụ
        frame_detail_input = tk.LabelFrame(self, text="Chi tiết Dịch vụ", font=FONT_LABEL, bg=BG_LIGHT, fg=COLOR_MAIN, padx=10, pady=5, bd=2, relief="groove")
        frame_detail_input.pack(pady=5, padx=15, fill="x")
        tk.Label(frame_detail_input, text="Mã dịch vụ:", font=FONT_LABEL, bg=BG_LIGHT).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.cb_madv = ttk.Combobox(frame_detail_input, font=("Times New Roman", 12), width=15, state="readonly")
        self.cb_madv.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame_detail_input, text="Số lượng:", font=FONT_LABEL, bg=BG_LIGHT).grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_soluong = tk.Entry(frame_detail_input, width=10)
        self.entry_soluong.grid(row=0, column=3, padx=5, pady=5)
        tk.Button(frame_detail_input, text="Thêm DV", command=self.add_detail, width=10, bg="#ffa500", fg="white", font=("Times New Roman", 12, "bold")).grid(row=0, column=4, padx=15, pady=5)
        tk.Button(frame_detail_input, text="Xóa DV", command=self.delete_detail, width=10, bg="#ff4d4d", fg="white", font=("Times New Roman", 12, "bold")).grid(row=0, column=5, padx=15, pady=5)

        

        # Nút chức năng chính
        frame_btn = tk.Frame(self, bg="#f0f8ff")
        frame_btn.pack(pady=10)
        btn_conf = {"font": ("Times New Roman", 12, "bold"), "bg": COLOR_MAIN, "fg": "white", "width": 12}
        tk.Button(frame_btn, text="Tạo HĐ mới", command=self.clear_input, **btn_conf).grid(row=0, column=0, padx=15)
        tk.Button(frame_btn, text="Sửa HĐ", command=self.edit_invoice, **btn_conf).grid(row=0, column=1, padx=15)
        tk.Button(frame_btn, text="Lưu HĐ", command=self.save_invoice, **btn_conf).grid(row=0, column=2, padx=15)
        tk.Button(frame_btn, text="Thoát", command=self.close_form, **btn_conf).grid(row=0, column=3, padx=15)
        # Bảng chi tiết
        # === BẢNG CHI TIẾT HÓA ĐƠN ===
        frame_cthd = tk.Frame(self, bg=BG_LIGHT)
        frame_cthd.pack(fill="both", expand=True, padx=15, pady=5)

        columns_cthd = ("id_ct", "madv", "tendv", "soluong", "dongia", "thanhtien")

        # Tạo style cho Treeview
        style_ct = ttk.Style(self)
        style_ct.configure("Treeview", font=("Times New Roman", 12))  # font ô dữ liệu
        style_ct.configure("Treeview.Heading", font=("Times New Roman", 12, "bold"))  # font header
        style_ct.map("Treeview", background=[("selected", COLOR_MAIN)], foreground=[("selected", "white")])

        # Tạo Treeview
        self.tree_cthd = ttk.Treeview(frame_cthd, columns=columns_cthd, show="headings", height=8, style="Treeview")

        # Scrollbar dọc
        scrollbar_y = ttk.Scrollbar(frame_cthd, orient="vertical", command=self.tree_cthd.yview)
        self.tree_cthd.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side="right", fill="y")

        # Scrollbar ngang
        scrollbar_x = ttk.Scrollbar(frame_cthd, orient="horizontal", command=self.tree_cthd.xview)
        self.tree_cthd.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(side="bottom", fill="x")

        # Cấu hình cột và tiêu đề
        self.tree_cthd.heading("id_ct", text="STT"); self.tree_cthd.column("id_ct", width=50, anchor="center")
        self.tree_cthd.heading("madv", text="Mã DV"); self.tree_cthd.column("madv", width=80, anchor="center")
        self.tree_cthd.heading("tendv", text="Tên Dịch vụ"); self.tree_cthd.column("tendv", width=250, anchor="w")
        self.tree_cthd.heading("soluong", text="Số lượng"); self.tree_cthd.column("soluong", width=80, anchor="center")
        self.tree_cthd.heading("dongia", text="Đơn giá"); self.tree_cthd.column("dongia", width=120, anchor="e")
        self.tree_cthd.heading("thanhtien", text="Thành tiền"); self.tree_cthd.column("thanhtien", width=150, anchor="e")

        # Pack Treeview
        self.tree_cthd.pack(side="left", fill="both", expand=True)

    # --- Đóng form ---
    def close_form(self):
        self.master.destroy()
        if self.parent_root:
            self.parent_root.deiconify()

# --- TEST CHẠY ---
if __name__ == "__main__":
    def center_window(win, w, h):
        ws = win.winfo_screenwidth(); hs = win.winfo_screenheight()
        x = (ws // 2) - (w // 2); y = (hs // 2) - (h // 2)
        win.geometry(f"{w}x{h}+{x}+{y}")

    root = tk.Tk()
    root.title("Quản lý Thanh toán")
    center_window(root, 950, 750) 
    app = QuanLyThanhToan(root, connect_db)
    app.pack(fill="both", expand=True)
    root.mainloop()
