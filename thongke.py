import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class ThongKeHoaDon:
    def __init__(self, parent, connect_db_func):
        self.parent = parent
        self.connect_db = connect_db_func
        self.create_ui()

    def create_ui(self):
        # Tạo cửa sổ thống kê
        self.window = tk.Toplevel(self.parent)
        self.window.title("THỐNG KÊ -BÁO CÁO")
        self.window.geometry("1100x650")
        self.window.configure(bg="#fff5f5")

        # Tiêu đề
        tk.Label(self.window, text="THỐNG KÊ - BÁO CÁO",
                 font=("Times New Roman", 22, "bold"),
                 fg="#a80000", bg="#fff5f5").pack(pady=20)

        # Khung thông số
        frame_stats = tk.Frame(self.window, bg="#fcdada", bd=2, relief="groove")
        frame_stats.pack(padx=30, pady=10, fill="x")

        # Kết nối DB và lấy dữ liệu
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM benhnhan;")
        total_benhnhan = cursor.fetchone()[0]

        cursor.execute("SELECT IFNULL(SUM(tongtien), 0) FROM hoadon;")
        total_doanhthu = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM hoadon;")
        total_hoadon = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM hoadon WHERE trangthai='Chưa thanh toán';")
        unpay_hoadon = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM dichvu;")
        total_dichvu = cursor.fetchone()[0]

        conn.close()

        # Hiển thị thông số
        info = [
            ("🧍‍♀️ Tổng số bệnh nhân", total_benhnhan),
            ("💰 Tổng doanh thu", f"{total_doanhthu:,.0f} VNĐ"),
            ("🧾 Tổng số hóa đơn", total_hoadon),
            ("❗ Hóa đơn chưa thanh toán", unpay_hoadon),
            ("💉 Tổng số dịch vụ", total_dichvu),
        ]

        for i, (label, value) in enumerate(info):
            tk.Label(frame_stats, text=label, font=("Times New Roman", 15, "bold"),
                     fg="#a80000", bg="#fcdada").grid(row=i, column=0, sticky="w", padx=30, pady=10)
            tk.Label(frame_stats, text=value, font=("Times New Roman", 15),
                     fg="black", bg="#fcdada").grid(row=i, column=1, sticky="w", padx=20, pady=10)

        # Khung bảng Top 10 dịch vụ
        frame_table = tk.LabelFrame(self.window, text="Top 10 dịch vụ sử dụng nhiều nhất",
                                    font=("Times New Roman", 13, "bold"),
                                    fg="#a80000", bg="#fff5f5")
        frame_table.pack(fill="both", expand=True, padx=30, pady=20)

        # Tạo style cho Treeview
        style_tree = ttk.Style()
        style_tree.configure("Custom.Treeview",
                             font=("Times New Roman", 12),
                             rowheight=25,
                             background="white",
                             fieldbackground="white",
                             bordercolor="#100f0f",
                             relief="solid")  # viền tổng thể đỏ
        style_tree.configure("Custom.Treeview.Heading",
                             font=("Times New Roman", 12, "bold"),
                             background="#fcdada",
                             foreground="#050505")
        # --- Thêm highlight màu khi chọn hàng ---
        style_tree.map("Custom.Treeview",
               background=[("selected", "#a80000")],  # màu vàng khi chọn
               foreground=[("selected", "White")])   # màu chữ khi chọn
        # Tạo Treeview với style
        tree = ttk.Treeview(frame_table, columns=("Tên dịch vụ", "Số lượng", "Tiền"),
                            show="headings", height=10, style="Custom.Treeview")

        # Cài heading và cột
        tree.heading("Tên dịch vụ", text="Tên dịch vụ")
        tree.heading("Số lượng", text="Số lượng")
        tree.heading("Tiền", text="Tiền (VNĐ)")

        tree.column("Tên dịch vụ", width=300)
        tree.column("Số lượng", width=100, anchor="center")
        tree.column("Tiền", width=150, anchor="e")

        # Scrollbar dọc
        scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Lấy dữ liệu top 10 dịch vụ
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT dv.tendv, SUM(ct.soluong), SUM(ct.thanhtien)
            FROM ct_hoadon ct
            JOIN dichvu dv ON ct.madv = dv.madv
            GROUP BY dv.tendv
            ORDER BY SUM(ct.soluong) DESC
            LIMIT 10;
        """)
        for row in cursor.fetchall():
            tree.insert("", "end", values=(row[0], row[1], f"{row[2]:,.0f}"))
        conn.close()

        # Tô màu xen kẽ các hàng
        for i, item in enumerate(tree.get_children()):
            if i % 2 == 0:
                tree.item(item, tags=("evenrow",))
            else:
                tree.item(item, tags=("oddrow",))
        style_tree.configure("evenrow", background="#fff5f5")
        style_tree.configure("oddrow", background="#f9e6e6")

        # Xử lý khi đóng cửa sổ
        def on_close():
            self.window.destroy()
            self.parent.deiconify()  # hiện lại form chính
        self.window.protocol("WM_DELETE_WINDOW", on_close)


# Hàm gọi từ form chính
def open_thongke_window(main_root, connect_db_func):
    main_root.withdraw()  # ẩn form chính
    ThongKeHoaDon(main_root, connect_db_func)
