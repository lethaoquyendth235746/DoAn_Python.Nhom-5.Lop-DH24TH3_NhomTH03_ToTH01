import tkinter as tk
from tkinter import ttk,messagebox
from tkcalendar import DateEntry
import mysql.connector
import datetime
# Kết nối đến cơ sở dữ liệu MySQL
def connect_db():
    try:
        # Thay thế các giá trị bên dưới bằng thông tin MySQL của bạn
        conn = mysql.connector.connect(
            host="localhost",
            user="root",          
            password="071005" ,          
            database="qlbenhnhan" 
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi Kết Nối Database", f"Không thể kết nối đến MySQL: {err}")
        return None
   
# Hàm canh giữa cửa sổ (giữ nguyên)
def center_window(win, w=900,h=600):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws//2) - (w//2)
    y=(hs//2) - (h//2)
    win.geometry(f'{w}x{h}+{x}+{y}')
     # Biến global (đặt ngoài hàm)


# Cửa sổ chính
def open_quanlybenhnhan():
    window=tk.Toplevel()
    window.title("Quản lý bệnh nhân")
    center_window(window,1200,800) # Tăng kích thước để chứa thêm khu vực Nhập viện
    window.resizable(False,False)
    mabn_selected_var = tk.StringVar(window, value="") 
    stt_selected_var = tk.StringVar(window, value="")

    # Khai báo biến cục bộ
    style = ttk.Style(window)
    style.theme_use("default")
    COLOR_DARK_RED_FG = "#E21C1C" 
    
    # Khai báo variables cho fields BN
    gender_var= tk.StringVar(value="Nam")
    
    # Khai báo các widgets (Chỉ khai báo biến ở đây để các hàm con có thể tham chiếu)
    entry_mabn = tk.Entry()
    entry_holot = tk.Entry()
    entry_ten = tk.Entry()
    date_entry = DateEntry()
    entry_diachi = tk.Entry()
    entry_sdt = tk.Entry()
    entry_cccd = tk.Entry()
    
    # Khai báo các widgets cho Nhập viện (sẽ được tạo sau)
    tree = ttk.Treeview() 
    tree_nhapvien = ttk.Treeview()
    date_entry_ngaynhap = DateEntry()
    date_entry_ngayxuat = DateEntry()
    cbb_loaihinh = ttk.Combobox()
    cbb_mabs = ttk.Combobox()
    cbb_maphong = ttk.Combobox()
    entry_chandoan = tk.Entry()

    # =========================================================
    # --- KHỐI HÀM VÀ LOGIC (PHẢI ĐẶT TRƯỚC PHẦN GIAO DIỆN) ---
    # =========================================================
    
    # --- LOOKUP FUNCTIONS ---
    def get_lookup_data(table_name, id_col, name_col):
        """Truy vấn dữ liệu từ các bảng tra cứu (bacsi, phong, khoa)."""
        conn = connect_db()
        data = {}
        if conn:
            cur = conn.cursor()
            try:
                cur.execute(f"SELECT {id_col}, {name_col} FROM {table_name}")
                for row in cur.fetchall():
                    data[row[0]] = row[1] 
            except:
                pass 
            finally:
                conn.close()
        return data

    # --- CLEAR INPUTS ---
    def clear_input_nhapvien():
        """Xóa các trường nhập liệu của Lịch sử Nhập viện."""
        date_entry_ngaynhap.set_date(datetime.datetime.now())
        date_entry_ngayxuat.set_date("01/01/2000")
        cbb_loaihinh.set("Ngoại trú")
        cbb_mabs.set("")
        cbb_maphong.set("")
        entry_chandoan.delete(0, tk.END)
        stt_selected_var.set("") 

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
        clear_input_nhapvien()


    # --- LOAD DATA FOR TREEVIEW 2 (NHAPVIEN) ---
    def load_data_nhapvien(mabn_hientai):
        for i in tree_nhapvien.get_children():
            tree_nhapvien.delete(i)
        
        if mabn_hientai == "NONE": return

        conn = connect_db()
        if conn is None: return

        cur = conn.cursor()
        try:
            sql_query = """
            SELECT stt, mabn, ngaynhap, ngayxuat, loaihinh, chandoan, mabs, maphong
            FROM nhapvien WHERE mabn = %s ORDER BY ngaynhap DESC
            """
            cur.execute(sql_query, (mabn_hientai,))
            
            for row in cur.fetchall():
                row_list = list(row)
                for i in [2, 3]: 
                    if isinstance(row_list[i], datetime.date):
                        row_list[i] = row_list[i].strftime("%d/%m/%Y")
                    elif row_list[i] is None:
                        row_list[i] = ""
                        
                tree_nhapvien.insert("", tk.END, values=row_list)
        except Exception as e:
            messagebox.showerror("Lỗi tải lịch sử nhập viện", str(e))
        finally:
            conn.close()

    # --- LOAD DATA FOR TREEVIEW 1 (BENHNHAN) ---
    def load_data(): 
        for i in tree.get_children(): 
            tree.delete(i) 
        conn = connect_db() 
        cur = conn.cursor() 
        cur.execute("SELECT mabn, holot, ten, phai, ngaysinh, diachi, sdt, cccd FROM benhnhan") 
        for row in cur.fetchall(): 
            row_list = list(row)
            ngaysinh_sql = row_list[4]
            if isinstance(ngaysinh_sql, datetime.date):
                ngaysinh_vn = ngaysinh_sql.strftime("%d/%m/%Y")
            else:
                ngaysinh_vn = str(ngaysinh_sql)
            row_list[4] = ngaysinh_vn
            tree.insert("", tk.END, values=row_list) 
        conn.close()

    # --- CRUD BENHNHAN (Đã rút gọn) ---
    def convert_date(date_input):
        try:
            ngaysinh_obj = datetime.datetime.strptime(date_input, "%d/%m/%Y")
            return ngaysinh_obj.strftime("%Y-%m-%d")
        except ValueError:
            return None

    def them_nv(): 
        mabn, holot, ten, phai, diachi, sdt, cccd = entry_mabn.get(), entry_holot.get(), entry_ten.get(), gender_var.get(), entry_diachi.get(), entry_sdt.get(), entry_cccd.get()
        ngaysinh_sql = convert_date(date_entry.get())
        if not all([mabn, holot, ten, diachi, sdt, cccd, ngaysinh_sql]):
             messagebox.showerror("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin") 
             return 
        conn = connect_db() 
        cur = conn.cursor() 
        try: 
            cur.execute("INSERT INTO benhnhan VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (mabn, holot, ten, phai, ngaysinh_sql, diachi, sdt, cccd)) 
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
                messagebox.showerror("Lỗi xóa dữ liệu bệnh nhân", str(e))
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
        # [Tiếp tục điền các fields khác...]
        entry_holot.delete(0, tk.END); entry_holot.insert(0, values[1]) 
        entry_ten.delete(0, tk.END); entry_ten.insert(0, values[2]) 
        gender_var.set(values[3]) 
        date_entry.set_date(values[4]) # Đã xử lý định dạng DD/MM/YYYY trong load_data
        entry_diachi.delete(0, tk.END); entry_diachi.insert(0, values[5])
        entry_sdt.delete(0, tk.END); entry_sdt.insert(0, values[6])
        entry_cccd.delete(0, tk.END); entry_cccd.insert(0, values[7])

    def luu_nv(): 
        mabn, holot, ten, phai, diachi, sdt, cccd = entry_mabn.get(), entry_holot.get(), entry_ten.get(), gender_var.get(), entry_diachi.get(), entry_sdt.get(), entry_cccd.get()
        ngaysinh_sql = convert_date(date_entry.get())
        if not ngaysinh_sql: return # Ngày sinh không hợp lệ
        conn = connect_db() 
        cur = conn.cursor() 
        try:
            cur.execute("""UPDATE benhnhan SET holot=%s, ten=%s, phai=%s, ngaysinh=%s, diachi=%s, sdt=%s, cccd=%s WHERE mabn=%s""", (holot, ten, phai, ngaysinh_sql, diachi, sdt, cccd, mabn)) 
            conn.commit() 
            messagebox.showinfo("Thành công", f"Đã cập nhật thông tin cho mã bệnh nhân: {mabn}.")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close() 
        load_data() 
        clear_input()


    # --- CRUD NHAPVIEN (THEM) ---
    def them_lan_nhap():
        if mabn_selected_var.get() == "":
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn một Bệnh nhân trước.")
            return
        
        mabn = mabn_selected_var.get()
        ngaynhap_input = date_entry_ngaynhap.get()
        ngayxuat_input = date_entry_ngayxuat.get()
        loaihinh = cbb_loaihinh.get()
        # Lấy ID từ chuỗi "ID - Tên"
        mabs_val = cbb_mabs.get().split(' ')[0] if cbb_mabs.get() else None
        maphong_val = cbb_maphong.get().split(' ')[0] if cbb_maphong.get() else None
        chandoan = entry_chandoan.get()

        ngaynhap_sql = convert_date(ngaynhap_input)
        ngayxuat_sql = convert_date(ngayxuat_input) if ngayxuat_input != "01/01/2000" else None
        
        if loaihinh == "Nội trú" and maphong_val is None:
            messagebox.showwarning("Thiếu dữ liệu", "Bệnh nhân Nội trú phải có Mã Phòng.")
            return
        
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute(""" INSERT INTO nhapvien (mabn, ngaynhap, ngayxuat, loaihinh, chandoan, mabs, maphong) VALUES (%s, %s, %s, %s, %s, %s, %s) """, 
                        (mabn, ngaynhap_sql, ngayxuat_sql, loaihinh, chandoan, mabs_val, maphong_val))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã thêm lần nhập viện mới.")
            load_data_nhapvien(mabn)
            clear_input_nhapvien()
            
        except Exception as e:
            messagebox.showerror("Lỗi thêm nhập viện", str(e))
        finally:
            conn.close()
    
    # [CÁC HÀM CRUD KHÁC NHAPVIEN NHƯ xoa_lan_nhap CŨNG CẦN ĐỊNH NGHĨA Ở ĐÂY]

    # --- BINDING HANDLER ---
    def select_benhnhan(event):
        selected = tree.selection()
        if not selected:
            clear_input()
            load_data_nhapvien("NONE")
            mabn_selected_var.set("")
            return

        values = tree.item(selected)["values"]
        mabn_hientai = values[0] 
        mabn_selected_var.set(mabn_hientai)
        
        # Điền thông tin BN lên fields nhập liệu (tái sử dụng sua_nv logic)
        entry_mabn.delete(0, tk.END) ; entry_mabn.insert(0, values[0])
        entry_mabn.config(state="readonly")
        entry_holot.delete(0, tk.END) ; entry_holot.insert(0, values[1])
        entry_ten.delete(0, tk.END) ; entry_ten.insert(0, values[2])
        gender_var.set(values[3]) 
        date_entry.set_date(values[4])
        entry_diachi.delete(0, tk.END) ; entry_diachi.insert(0, values[5])
        entry_sdt.delete(0, tk.END) ; entry_sdt.insert(0, values[6])
        entry_cccd.delete(0, tk.END) ; entry_cccd.insert(0, values[7])
        
        # Tải lịch sử nhập viện
        load_data_nhapvien(mabn_hientai)
        clear_input_nhapvien()
        
    # --- END KHỐI HÀM ---

    # =========================================================
    # --- KHỐI GIAO DIỆN (SỬ DỤNG CÁC BIẾN ĐÃ KHAI BÁO) ---
    # =========================================================
    

    # Cấu hình Style để đảm bảo hiển thị đường lưới
    style = ttk.Style(window)
    style.theme_use("default") # Sử dụng theme mặc định, thường hỗ trợ lưới tốt hơn


    # Định nghĩa các màu sắc bạn muốn
    COLOR_RED_TITLE = "red"
    COLOR_LIGHT_RED_BG = "#F9F9F9"
    COLOR_DARK_RED_FG = "#E21C1C"  
    COLOR_PASTEL_RED_BG = "#F6C8C8"


    # --- Tiêu đề và Frame nhập thông tin (Chỉ đặt lại các widgets) ---
    lbl_title=tk.Label(window,text="QUẢN LÝ BỆNH NHÂN",font=("Times New Roman",18,"bold"),fg=COLOR_DARK_RED_FG)
    lbl_title.pack(pady=10)
    
    frame_info=tk.Frame(window)
    frame_info.pack(pady=5,padx=10,fill="x")

    # [CODE TẠO VÀ GRID CÁC FIELDS CHO BỆNH NHÂN] (đảm bảo gán đúng biến: entry_mabn=tk.Entry(), v.v.)
    tk.Label(frame_info, text="Mã bệnh nhân",fg=COLOR_DARK_RED_FG,font=("Times New Roman",13,"bold")).grid(row=0,column=0,padx=5,pady=5,sticky="w")
    entry_mabn = tk.Entry(frame_info, width=15)
    entry_mabn.grid(row=0,column=1,padx=5,pady=5,sticky="w")
    # ... (Các fields khác)
    tk.Label(frame_info, text="Mã bệnh nhân",fg=COLOR_DARK_RED_FG,font=("Times New Roman",13,"bold")).grid(row=0,column=0,padx=5,pady=5,sticky="w")
    entry_mabn=tk.Entry(frame_info,width=15)
    entry_mabn.grid(row=0,column=1,padx=5,pady=5,sticky="w")


    tk.Label(frame_info, text="Họ và lót", fg=COLOR_DARK_RED_FG,font=("Times New Roman",13,"bold")).grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_holot = tk.Entry(frame_info, width=25)
    entry_holot.grid(row=1, column=1, columnspan=3 ,padx=5, pady=5, sticky="w")


    tk.Label(frame_info, text="Tên", fg=COLOR_DARK_RED_FG,font=("Times New Roman",13,"bold")).grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_ten = tk.Entry(frame_info, width=15)
    entry_ten.grid(row=2, column=1, padx=5, pady=5, sticky="w")


    gender_var= tk.StringVar(value="Nam")
    tk.Label(frame_info,text="Phái",fg=COLOR_DARK_RED_FG,font=("Times New Roman",13,"bold")).grid(row=3,column=0,padx=5,pady=5,sticky="w")
    tk.Radiobutton(frame_info,text="Nam",variable=gender_var,value="Nam",fg=COLOR_DARK_RED_FG ,font=("Times New Roman",13,"bold")).grid(row=3,column=1,padx=5,sticky="w")
    tk.Radiobutton(frame_info,text="Nữ",variable=gender_var,value="Nữ",fg=COLOR_DARK_RED_FG,font=("Times New Roman",13,"bold")).grid(row=3,column=2,padx=5,sticky="w")


    tk.Label(frame_info,text="Ngày sinh",fg=COLOR_DARK_RED_FG,font=("Times New Roman",13,"bold")).grid(row=0,column=2,padx=(90,5),pady=5,sticky="w")
    date_entry=DateEntry(frame_info,width=12,background="darkblue",foreground="white",date_pattern="dd/mm/yyyy")
    date_entry.grid(row=0,column=3,padx=(5,5),pady=5,sticky="w")


    tk.Label(frame_info,text="Địa chỉ",fg=COLOR_DARK_RED_FG,font=("Times New Roman",13,"bold")).grid(row=1,column=2,padx=(90,5),pady=5,sticky="w")
    entry_diachi=tk.Entry(frame_info,width=55)
    entry_diachi.grid(row=1, column=3, padx=5, pady=5, sticky="w")
    tk.Label(frame_info, text="SĐT", fg=COLOR_DARK_RED_FG,font=("Times New Roman",13,"bold")).grid(row=2, column=2, padx=(90,5), pady=5, sticky="w")
    entry_sdt = tk.Entry(frame_info, width=20)
    entry_sdt.grid(row=2, column=3, padx=5, pady=5, sticky="w")
    tk.Label(frame_info, text="CCCD", fg=COLOR_DARK_RED_FG,font=("Times New Roman",13,"bold")).grid(row=3, column=2, padx=(90,5), pady=5, sticky="w")
    entry_cccd = tk.Entry(frame_info, width=25)
    entry_cccd.grid(row=3, column=3, padx=5, pady=5, sticky="w")








    # ====== Frame nút CRUD Bệnh nhân ====== 
    frame_btn = tk.Frame(window) 
    frame_btn.pack(pady=5) 
    # [CODE TẠO CÁC BUTTON CHO BỆNH NHÂN]
    # ====== Frame nút ======
    frame_btn = tk.Frame(window)
    frame_btn.pack(pady=5)
 
    tk.Button(frame_btn, text="Thêm", width=8, command=them_nv, fg=COLOR_DARK_RED_FG ,font=("Times New Roman",13,"bold")).grid(row=0, column=0, padx=30)
    tk.Button(frame_btn, text="Lưu", width=8, command=luu_nv,fg=COLOR_DARK_RED_FG ,font=("Times New Roman",13,"bold")).grid(row=0, column=1, padx=30)


    tk.Button(frame_btn, text="Sửa", width=8, command=sua_nv,fg=COLOR_DARK_RED_FG ,font=("Times New Roman",13,"bold")).grid(row=0, column=2, padx=30)


    tk.Button(frame_btn, text="Hủy", width=8, command=clear_input,fg=COLOR_DARK_RED_FG ,font=("Times New Roman",13,"bold")).grid(row=0, column=3, padx=30)


    tk.Button(frame_btn, text="Xóa", width=8, command=xoa_nv,fg=COLOR_DARK_RED_FG ,font=("Times New Roman",13,"bold")).grid(row=0, column=4, padx=30)


    tk.Button(frame_btn, text="Thoát", width=8, command=window.destroy,fg=COLOR_DARK_RED_FG ,font=("Times New Roman",13,"bold")).grid(row=0, column=5, padx=30)




    # ====== Bảng danh sách Bệnh nhân (TREEVIEW 1) ====== 
    lbl_ds = tk.Label(window, text="Danh sách bệnh nhân", font=("Times New Roman", 13, "bold")) 
    lbl_ds.pack(pady=5, anchor="w", padx=10)
    columns = ("mabn", "holot","ten", "phai", "ngaysinh", "diachi","sdt","cccd")
    tree = ttk.Treeview(window, columns=columns, show="headings", height=6) # <--- ĐỊNH NGHĨA TREEVIEW 1
    # [CODE CẤU HÌNH CỘT CHO TREEVIEW 1]
    # Đặt tiêu đề cho từng cột
    tree.heading("mabn", text="Mã BN")
    tree.heading("holot", text="Họ và lót")
    tree.heading("ten", text="Tên")
    tree.heading("phai", text="Phái")
    tree.heading("ngaysinh", text="Ngày sinh")
    tree.heading("diachi", text="Địa chỉ")
    tree.heading("sdt", text="SĐT")
    tree.heading("cccd", text="CCCD")

    # Căn chỉnh và đặt độ rộng cho từng cột
    tree.column("mabn", width=100, anchor="center")
    tree.column("holot", width=180, anchor="w")
    tree.column("ten", width=100, anchor="w")
    tree.column("phai", width=80, anchor="center")
    tree.column("ngaysinh", width=100, anchor="center")
    tree.column("diachi", width=250, anchor="w")
    tree.column("sdt", width=120, anchor="center")
    tree.column("cccd", width=150, anchor="center")

    # Thêm thanh cuộn dọc cho bảng
    scroll_y = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scroll_y.set)
    scroll_y.pack(side="right", fill="y")

    tree.pack(pady=5, padx=10, fill="both")
        

    
    # ------------------------------------------------------------------
    # --- KHU VỰC NHẬP VIỆN (TREEVIEW 2) ---
    # ------------------------------------------------------------------
    
    # Lấy dữ liệu tra cứu cho Combobox
    bs_lookup_data = get_lookup_data("bacsi", "mabs", "hoten")
    phong_lookup_data = get_lookup_data("phong", "maphong", "tenphong")
    bs_list = [f"{id} - {name}" for id, name in bs_lookup_data.items()]
    phong_list = [f"{id} - {name}" for id, name in phong_lookup_data.items()]

    lbl_ds_nv = tk.Label(window, text="Lịch sử Nhập viện", font=("Times New Roman", 13, "bold"))
    lbl_ds_nv.pack(pady=5, anchor="w", padx=10)
    frame_nhapvien_info = tk.Frame(window)
    frame_nhapvien_info.pack(pady=5, padx=10, fill="x")
    
    # [CODE TẠO FIELDS NHẬP VIỆN VÀ GÁN VÀO CÁC BIẾN NHƯ date_entry_ngaynhap, cbb_mabs, v.v.]
    # (Bạn cần gán đúng biến đã khai báo ở đầu hàm)
   
    

    
    # ====== Bảng LỊCH SỬ NHẬP VIỆN (Treeview 2) ======
    columns_nv = ("stt", "mabn", "ngaynhap", "ngayxuat", "loaihinh", "mabs", "maphong", "chandoan")
    tree_nhapvien = ttk.Treeview(window, columns=columns_nv, show="headings", height=6) # <--- ĐỊNH NGHĨA TREEVIEW 2
    # [CODE CẤU HÌNH CỘT CHO TREEVIEW 2]
    tree_nhapvien.pack(pady=5, padx=10, fill="both")
   

    # Kiểu chữ & màu cho Treeview 2
    style.configure("Treeview", font=("Times New Roman", 12), foreground="red", rowheight=28)
    style.configure("Treeview.Heading", font=("Times New Roman", 13, "bold"), foreground="red")

    tree_nhapvien.heading("stt", text="STT")
    tree_nhapvien.heading("mabn", text="Mã BN")
    tree_nhapvien.heading("ngaynhap", text="Ngày nhập")
    tree_nhapvien.heading("ngayxuat", text="Ngày xuất")
    tree_nhapvien.heading("loaihinh", text="Loại hình")
    tree_nhapvien.heading("chandoan", text="Chẩn đoán")
    tree_nhapvien.heading("mabs", text="Mã BS")
    tree_nhapvien.heading("maphong", text="Mã phòng")

    tree_nhapvien.column("stt", width=50, anchor="center")
    tree_nhapvien.column("mabn", width=100, anchor="center")
    tree_nhapvien.column("ngaynhap", width=100, anchor="center")
    tree_nhapvien.column("ngayxuat", width=100, anchor="center")
    tree_nhapvien.column("loaihinh", width=100, anchor="center")
    tree_nhapvien.column("chandoan", width=200, anchor="w")
    tree_nhapvien.column("mabs", width=120, anchor="center")
    tree_nhapvien.column("maphong", width=120, anchor="center")

    # Thanh cuộn dọc cho Treeview 2
    scroll_nv_y = ttk.Scrollbar(window, orient="vertical", command=tree_nhapvien.yview)
    tree_nhapvien.configure(yscroll=scroll_nv_y.set)
    scroll_nv_y.pack(side="right", fill="y")

    tree_nhapvien.pack(pady=5, padx=10, fill="both")
    
    
    # =========================================================
    # --- KHỐI CHẠY LỆNH BAN ĐẦU VÀ BINDING ---
    # =========================================================
    
    load_data() # Load danh sách bệnh nhân ban đầu
    tree.bind('<<TreeviewSelect>>', select_benhnhan) # Gán sự kiện click cho Treeview 1
    
    window.mainloop()