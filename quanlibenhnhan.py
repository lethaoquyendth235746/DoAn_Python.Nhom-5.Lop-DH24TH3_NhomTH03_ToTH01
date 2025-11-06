import tkinter as tk
from tkinter import ttk,messagebox
from tkcalendar import DateEntry
import mysql.connector
import datetime



# Import file đăng nhập
import giaodiendangnhap




# Kết nối đến cơ sở dữ liệu MySQL
def connect_db():
    try:
        # Thay thế các giá trị bên dưới bằng thông tin MySQL của bạn
        conn = mysql.connector.connect(
            host="localhost",
            user="root",          
            password="7777777",          
            database="qlbenhnhan" 
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi Kết Nối Database", f"Không thể kết nối đến MySQL: {err}")
        return None
# Hàm canh giữa cửa sổ
def center_window(win, w=900,h=600):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws//2) - (w//2)
    y=(hs//2) - (h//2)
    win.geometry(f'{w}x{h}+{x}+{y}')
# Cửa sổ chính
root=tk.Tk()
root.title("Quản lý bệnh nhân")
center_window(root,900,600)
root.resizable(False,False)

# Cấu hình Style để đảm bảo hiển thị đường lưới
style = ttk.Style(root)
style.theme_use("default") # Sử dụng theme mặc định, thường hỗ trợ lưới tốt hơn

# Định nghĩa các màu sắc bạn muốn
COLOR_RED_TITLE = "red"
COLOR_LIGHT_RED_BG = "#F9F9F9" 
COLOR_DARK_RED_FG = "#E21C1C"  
OLOR_PASTEL_RED_BG = "#F6C8C8"
#Tiêu đề
lbl_title=tk.Label(root,text="QUẢN LÝ BỆNH NHÂN",font=("Times New Roman",18,"bold"),fg=COLOR_DARK_RED_FG)
lbl_title.pack(pady=10)
# Frame nhập thông tin
frame_info=tk.Frame(root)
frame_info.pack(pady=5,padx=10,fill="x")

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





# ====== Chức năng CRUD ====== 
def clear_input(): 

    # === MỞ LẠI CHO PHÉP NHẬP MÃ BỆNH NHÂN ===
    entry_mabn.config(state="normal")

    entry_mabn.delete(0, tk.END) 
    entry_holot.delete(0, tk.END) 
    entry_ten.delete(0, tk.END) 
    entry_diachi.delete(0, tk.END) 
    entry_sdt.delete(0, tk.END)    
    entry_cccd.delete(0, tk.END)   
    
    gender_var.set("Nam")
    date_entry.set_date("01-01-2000")




def load_data(): 
    for i in tree.get_children(): 
        tree.delete(i) 
    conn = connect_db() 
    cur = conn.cursor() 
    # ghi ra cụ thể để dễ quản lý thứ tự cột thay vì dùng * from benhnhan
    cur.execute("SELECT mabn, holot, ten, phai, ngaysinh, diachi, sdt, cccd FROM benhnhan") 
    for row in cur.fetchall(): 
        row_list = list(row)
        ngaysinh_sql = row_list[4]

        if isinstance(ngaysinh_sql, datetime.date):
            # Chuyển đổi định dạng ngày từ YYYY-MM-DD sang DD/MM/YYYY
            ngaysinh_vn = ngaysinh_sql.strftime("%d/%m/%Y")
        else:
            ngaysinh_vn = str(ngaysinh_sql)
        row_list[4] = ngaysinh_vn

        tree.insert("", tk.END, values=row_list) 
    conn.close()






def them_nv(): 
    mabn = entry_mabn.get() 
    holot = entry_holot.get() 
    ten = entry_ten.get() 
    phai = gender_var.get() 
   
    diachi = entry_diachi.get() 
    sdt = entry_sdt.get() 
    cccd = entry_cccd.get() 

    ngaysinh_input = date_entry.get()
    try:
        ngaysinh_obj= datetime.datetime.strptime(ngaysinh_input, "%d/%m/%Y")
        ngaysinh_sql = ngaysinh_obj.strftime("%Y-%m-%d")
    except ValueError:
        messagebox.showwarning("Ngày sinh không hợp lệ", "Vui lòng nhập đúng định dạng ngày sinh (dd/mm/yyyy)")
        return

    if mabn == "" or holot == "" or ten == "" or diachi == "" or sdt == "" or cccd == "": 
        messagebox.showerror("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin") 
        return 
 
    conn = connect_db() 
    cur = conn.cursor() 
    try: 
        cur.execute("INSERT INTO benhnhan VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                    (mabn, holot, ten, phai, ngaysinh_sql, diachi, sdt, cccd)) 
        conn.commit() 
        messagebox.showinfo("Thành công", "Đã thêm bệnh nhân mới.")
        load_data() 
        clear_input() 
    except Exception as e: 
        # Hiển thị lỗi nếu trùng Mã bn ( mabn là PRIMARY KEY)
        messagebox.showerror("Lỗi", str(e)) 
    conn.close()



def xoa_nv(): 
    selected = tree.selection() 
    if not selected: 
        messagebox.showwarning("Chưa chọn", "Hãy chọn bệnh nhân để xóa") 
        return 
    mabn_to_delete = tree.item(selected)["values"][0] 
    #Xác nhận trước khi xóa
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
# === KHÔNG CHO PHÉP SỬA MÃ BỆNH NHÂN ===
# LƯU Ý: Phải cho phép sửa lại khi hủy hoặc lưu thành công!
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



def luu_nv(): 
    mabn = entry_mabn.get() 
    holot = entry_holot.get() 
    ten = entry_ten.get() 
    phai = gender_var.get() 
    ngaysinh_input = date_entry.get() 
    diachi = entry_diachi.get() 
    sdt = entry_sdt.get()
    cccd = entry_cccd.get()

    try:
        # 1. Đọc chuỗi ngày tháng theo định dạng HIỆN TẠI (DD/MM/YYYY)
        ngaysinh_obj= datetime.datetime.strptime(ngaysinh_input, "%d/%m/%Y")
        # 2. Chuyển đổi sang định dạng SQL (YYYY-MM-DD)
        ngaysinh_sql = ngaysinh_obj.strftime("%Y-%m-%d")
    except ValueError:
        messagebox.showwarning("Ngày sinh không hợp lệ", "Vui lòng nhập đúng định dạng ngày sinh (dd/mm/yyyy)")
        return

    conn = connect_db() 
    cur = conn.cursor() 
    try:

        cur.execute("""UPDATE benhnhan SET holot=%s, ten=%s, phai=%s, ngaysinh=%s, diachi=%s, sdt=%s, cccd=%s
                WHERE mabn=%s""", (holot, ten, phai, ngaysinh_sql, diachi, sdt, cccd, mabn)) 
        conn.commit() 
        messagebox.showinfo("Thành công", f"Đã cập nhật thông tin cho mã bệnh nhân: {mabn}.")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
    finally:
        conn.close() 
    load_data() 
    clear_input()










# ====== Frame nút ====== 
frame_btn = tk.Frame(root) 
frame_btn.pack(pady=5) 
 
tk.Button(frame_btn, text="Thêm", width=8, command=them_nv, fg=COLOR_DARK_RED_FG ,font=("Times New Roman",13,"bold")).grid(row=0, column=0, padx=30) 
tk.Button(frame_btn, text="Lưu", width=8, command=luu_nv,fg=COLOR_DARK_RED_FG ,font=("Times New Roman",13,"bold")).grid(row=0, column=1, padx=30) 

tk.Button(frame_btn, text="Sửa", width=8, command=sua_nv,fg=COLOR_DARK_RED_FG ,font=("Times New Roman",13,"bold")).grid(row=0, column=2, padx=30) 

tk.Button(frame_btn, text="Hủy", width=8, command=clear_input,fg=COLOR_DARK_RED_FG ,font=("Times New Roman",13,"bold")).grid(row=0, column=3, padx=30)

tk.Button(frame_btn, text="Xóa", width=8, command=xoa_nv,fg=COLOR_DARK_RED_FG ,font=("Times New Roman",13,"bold")).grid(row=0, column=4, padx=30)

tk.Button(frame_btn, text="Thoát", width=8, command=root.quit,fg=COLOR_DARK_RED_FG ,font=("Times New Roman",13,"bold")).grid(row=0, column=5, padx=30)











# ====== Bảng danh sách nhân viên ====== 
lbl_ds = tk.Label(root, text="Danh sách bệnh nhân", font=("Times New Roman", 13, "bold")) 
lbl_ds.pack(pady=5, anchor="w", padx=10)

columns = ("mabn", "holot","ten", "phai", "ngaysinh", "diachi","sdt","cccd")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)

for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor="center")
tree.heading("mabn", text="Mã BN")    
tree.column("mabn", width=60, anchor="center")
tree.heading("holot", text="Họ và lót")
tree.column("holot", width=100, anchor="center")
tree.heading("ten", text="Tên")
tree.column("ten", width=50, anchor="center")
tree.heading("phai", text="Phái")
tree.column("phai", width=50, anchor="center")
tree.heading("ngaysinh", text="Ngày sinh")
tree.column("ngaysinh", width=100, anchor="center")
tree.heading("diachi", text="Địa chỉ")
tree.column("diachi", width=250)
tree.heading("sdt", text="SĐT")
tree.column("sdt", width=70, anchor="center")
tree.heading("cccd", text="CCCD")
tree.column("cccd", width=80, anchor="center")


tree.pack(pady=5, padx=10, fill="both")






# ====== KHỐI CHẠY CHƯƠNG TRÌNH ======
root.withdraw() # Ẩn cửa sổ chính Quản lý Bệnh nhân

load_data() # Vẫn load data để khi đăng nhập xong, bảng đã sẵn sàng

# Gọi cửa sổ đăng nhập từ file login, truyền các hàm và biến cần thiết
giaodiendangnhap.show_login_window(root, connect_db, center_window, COLOR_DARK_RED_FG)






# chạy
root.mainloop()
#x










