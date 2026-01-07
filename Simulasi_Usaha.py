import tkinter as tk#library utama GUI
from tkinter import ttk#widget tambahan tkinter
import math#library matematika

class WorkSimulator:#kelas utama simulasi
    #konstruktor 
    def __init__(self, root):
        #inisialisasi window utama
        self.root=root#menyimpan referensi window utama
        self.root.title("Simulasi Usaha oleh Gaya")#judul window
        self.root.geometry("1200x700")#ukuran window
        self.root.configure(bg="#f0f0f0")#warna latar window
        #konfigurasi grid window
        self.box_x=50#posisi horizontal awal kotak
        self.box_y=300#posisi vertikal awal kotak
        self.box_size=40#ukuran sisi kotak
        self.animation_running=False#status animasi berjalan atau tidak
        #variabel input
        self.force=tk.DoubleVar(value=10.0)#nilai gaya konstan
        self.displacement=tk.DoubleVar(value=5.0) #nilai perpindahan
        self.angle=tk.DoubleVar(value=30.0)#nilai sudut gaya
        self.force_type=tk.IntVar(value=1)#jenis gaya yang dipilih
        self.k_spring=tk.DoubleVar(value=410.0) #konstanta pegas
        self.f_applied=tk.DoubleVar(value=55.0)#gaya luar pada pegas
        self.setup_gui() #memanggil pembuatan user interface

    #fungsi building GUI
    def setup_gui(self):
        left_container=tk.Frame(self.root,bg="#f0f0f0")#wadah panel kiri
        left_container.grid(row=0,column=0,sticky="nsew",padx=10,pady=10)#penempatan panel kiri
        canvas=tk.Canvas(left_container,bg="#f0f0f0",highlightthickness=0,width=350)#canvas untuk scroll
        scrollbar=ttk.Scrollbar(left_container,orient="vertical",command=canvas.yview)#scrollbar vertikal
        canvas.configure(yscrollcommand=scrollbar.set)#sinkronisasi scroll
        scrollbar.pack(side="right",fill="y")#menempatkan scrollbar
        canvas.pack(side="left",fill="both",expand=True)#menempatkan canvas
        self.left_frame=tk.Frame(canvas,bg="#ffffff",padx=20,pady=20)#frame isi panel input
        canvas.create_window((0,0),window=self.left_frame,anchor="nw")#menempatkan frame dalam canvas
        def on_configure(event):#fungsi update area scroll
            canvas.configure(scrollregion=canvas.bbox("all"))#mengatur area scroll
        self.left_frame.bind("<Configure>",on_configure)#binding resize frame
        title=tk.Label(self.left_frame,text="Panel Input\n& Hasil Hitung",font=("Arial",25,"bold"),bg="#ffffff",fg="#2c3e50")#judul panel
        title.pack(pady=(0,20))#menempatkan judul
        option_frame=tk.LabelFrame(self.left_frame,text="Jenis Gaya",font=("Arial",11,"bold"),bg="#ffffff",padx=10,pady=5)#frame pilihan gaya
        option_frame.pack(fill=tk.X,pady=10)#menempatkan frame pilihan
        rb_constant=tk.Radiobutton(option_frame,text="Gaya Konstan",variable=self.force_type,value=1,bg="#ffffff",command=self.on_force_type_change)#radio gaya konstan
        rb_constant.pack(anchor="w")#menempatkan radio button
        rb_spring=tk.Radiobutton(option_frame,text="Gaya Bergantung Posisi(Pegas)",variable=self.force_type,value=2,bg="#ffffff",command=self.on_force_type_change)#radio gaya pegas
        rb_spring.pack(anchor="w")#menempatkan radio button
        self.force_frame,self.force_label=self.create_input_field(self.left_frame,"Gaya(F)[N]:",self.force,0,100)#input gaya
        self.disp_frame,self.disp_label=self.create_input_field(self.left_frame,"Perpindahan(d)[m]:",self.displacement,0,10)#input perpindahan
        self.angle_frame,self.angle_label=self.create_input_field(self.left_frame,"Sudut(θ)[°]:",self.angle,0,180)#input sudut
        self.btn_frame=tk.Frame(self.left_frame,bg="#ffffff")#frame tombol
        self.btn_frame.pack(pady=20)#menempatkan frame tombol
        self.animate_btn=tk.Button(self.btn_frame,text="Play",command=self.start_animation,font=("Arial",12,"bold"),bg="#119347",fg="white",padx=20,pady=10,cursor="hand2")#tombol play
        self.animate_btn.pack(pady=5,fill=tk.X)#menempatkan tombol play
        self.reset_btn=tk.Button(self.btn_frame,text="Reset",command=self.reset_animation,font=("Arial",12,"bold"),bg="#d80d0d",fg="white",padx=20,pady=10,cursor="hand2")#tombol reset
        self.reset_btn.pack(pady=5,fill=tk.X)#menempatkan tombol reset
        self.result_frame=tk.LabelFrame(self.left_frame,text="Kotak Hasil Hitung",font=("Arial",20,"bold"),bg="#ffffff",padx=10,pady=10)#frame hasil
        self.result_frame.pack(pady=20,fill=tk.BOTH,expand=True)#menempatkan frame hasil
        self.result_text=tk.Text(self.result_frame,height=15,width=35,font=("Courier",10),wrap=tk.WORD,bg="#ecf0f1",relief=tk.FLAT)#kotak teks hasil
        self.result_text.pack(fill=tk.BOTH,expand=True)#menempatkan kotak teks
        right_frame=tk.Frame(self.root,bg="#ffffff")#frame sisi kanan
        right_frame.grid(row=0,column=1,sticky="nsew",padx=10,pady=10)#posisi frame kanan
        canvas_label=tk.Label(right_frame,text="Simulasi Usaha by Kelompok 7: Zamil, Ayri, Ezy",font=("Arial",30,"bold"),bg="#ffffff")#judul canvas
        canvas_label.pack(pady=(0,10))#menempatkan judul
        self.canvas=tk.Canvas(right_frame,width=700,height=600,bg="#fafafa",highlightthickness=2,highlightbackground="#bdc3c7")#canvas animasi
        self.canvas.pack()#menempatkan canvas
        self.update_calculation()#menampilkan hasil awal

    #handler perubahan jenis gaya
    def on_force_type_change(self):
        for widget in self.left_frame.winfo_children():#loop semua widget panel kiri
            if widget not in [self.left_frame.winfo_children()[0],self.left_frame.winfo_children()[1]]:#kecuali judul dan opsi gaya
                widget.pack_forget()#hapus widget lama
        if self.force_type.get()==1:#jika gaya konstan
            self.force_frame,self.force_label=self.create_input_field(self.left_frame,"Gaya(F) [N]:",self.force,0,100)#input gaya
            self.disp_frame,self.disp_label=self.create_input_field(self.left_frame,"Perpindahan(d) [m]:",self.displacement,0,10)#input perpindahan
            self.angle_frame,self.angle_label=self.create_input_field(self.left_frame,"Sudut(θ) [°]:",self.angle,0,180)#input sudut
        else:#jika gaya pegas
            self.force_frame,self.force_label=self.create_input_field(self.left_frame,"Konstanta Pegas(k) [N/m]:",self.k_spring,100,1000)#input konstanta pegas
            self.disp_frame,self.disp_label=self.create_input_field(self.left_frame,"Gaya Tarik(F) [N]:",self.f_applied,-100,100)#input gaya pegas
            self.btn_frame.pack_forget()#sembunyikan tombol sementara
        self.btn_frame.pack(pady=20)#tampilkan kembali tombol
        self.result_frame.pack(pady=20,fill=tk.BOTH,expand=True)#tampilkan kotak hasil
        self.update_calculation()#update perhitungan
        self.draw_vectors()#gambar vektor gaya

    def create_input_field(self,parent,label_text,variable,min_val,max_val,pack_now=True):#fungsi membuat input
        frame=tk.Frame(parent,bg="#ffffff")#frame input
        if pack_now:# jika diizinkan pack
            frame.pack(pady=10,fill=tk.X)#menempatkan frame
        label=tk.Label(frame,text=label_text,font=("Arial",11),bg="#ffffff",anchor="w")#label input
        label.pack(anchor="w")#menempatkan label
        entry=tk.Entry(frame,textvariable=variable,font=("Arial",12),width=15,relief=tk.SOLID,borderwidth=1)#entry input
        entry.pack(pady=(5,5))#menempatkan entry
        slider=ttk.Scale(frame,from_=min_val,to=max_val,variable=variable,orient=tk.HORIZONTAL,command=lambda x:self.update_calculation())#slider input
        slider.pack(fill=tk.X)#menempatkan slider
        entry.bind("<KeyRelease>",lambda e:self.update_calculation())#update saat mengetik
        return frame,label#mengembalikan frame dan label
    
    #menghitung usaha berdasarkan input
    def calculate_work(self):
        if self.force_type.get()==1:#mode gaya konstan
            F=self.force.get()#ambil gaya
            d=self.displacement.get()#ambil perpindahan
            theta_deg=self.angle.get()#ambil sudut derajat
            theta_rad=math.radians(theta_deg)#konversi ke radian
            W=F*d*math.cos(theta_rad)#hitung usaha
            return W,F,d,theta_deg,theta_rad,0#kembalian hasil
        else:#mode pegas
            k=self.k_spring.get()#ambil konstanta pegas
            F_app=self.f_applied.get()#ambil gaya pegas
            if k==0:k=1#hindari pembagian nol
            x=F_app/k#hitung pertambahan panjang pegas
            W=0.5*k*(x**2)#hitung usaha pegas
            return W,k,x,0,0,F_app#kembalian hasil
        
    #fungsi memperbarui perhitungan dan tampilan hasil
    def update_calculation(self):
        W,val1,d,theta_deg,theta_rad,F_app=self.calculate_work()#ambil hasil perhitungan
        self.result_text.delete(1.0,tk.END)#hapus teks lama
        massa = 2.0 #asumsi massa benda 2 kg
        v_akhir = math.sqrt(2 * abs(W) / massa) if W >= 0 else 0 #hitung kecepatan akhir (jika usaha positif)
        if self.force_type.get()==1:#mode gaya konstan
            #hasil gaya konstan
            result=f"""
╔═══════════════════════════════╗
║    Usaha oleh Gaya Konstan    ║
╚═══════════════════════════════╝
Formula: W = F • d • cos(θ)

Data Input:
  F⃗ (Gaya)        = {val1:.2f} N
  d⃗ (Perpindahan) = {d:.2f} m
  θ (Sudut)       = {theta_deg:.1f}°

Hasil:
  Fx = {val1*math.cos(theta_rad):.2f} N
  W  = {W:.2f} J

Teorema Usaha-Energi:  
  ΔKE = W_tot
  ½mv² - 0 = {W:.2f} J
  Jika massa (m) = {massa} kg, maka:
  Kecepatan Akhir (v) = {v_akhir:.2f} m/s
"""
            self.result_text.insert(1.0,result)#tampilkan hasil
        else:#mode pegas
            #string hasil pegas
            result=f"""
╔═══════════════════════════════╗
║     Hukum Hooke & Usaha       ║
╚═══════════════════════════════╝
Formula:
  1. Perpanjangan pegas: Δx = F⃗ / k
  2. Usaha Pegas: W = ½ • k • (Δx)²

Data Input:
  k (Konstanta)   = {val1:.1f} N/m
  F⃗ (Gaya Tarik)  = {F_app:.1f} N

Hasil Perhitungan:
  Perpanjangan pegas (Δx) 
  = {F_app:.1f} / {val1:.1f}
  = {d:.3f} m  

  Usaha(W) 
  = 0.5 • {val1:.1f} • ({d:.3f})²
  = {W:.2f} J

Teorema Usaha-Energi:  
  ΔKE = W_tot
  ½mv² - 0 = {W:.2f} J
  Jika massa (m) = {massa} kg, maka:
  Kecepatan Akhir (v) = {v_akhir:.2f} m/s
"""
            self.result_text.insert(1.0,result)#tampilkan hasil
        if not self.animation_running:#jika animasi berhenti
            self.draw_vectors()#gambar ulang vektor

    #mulai animasi
    def start_animation(self):
        if not self.animation_running:#cek animasi belum berjalan
            self.box_x=50#reset posisi kotak
            self.animation_running=True#aktifkan animasi
            self.animate_btn.config(state=tk.DISABLED,bg="#95a5a6")#disable tombol
            self.animate()#mulai loop animasi

    def animate(self):#fungsi loop animasi
        if not self.animation_running:#jika animasi berhenti
            return#keluar fungsi
        if self.force_type.get()==1:#mode gaya konstan
            d=self.displacement.get()#ambil perpindahan
            scale=60#skala meter ke pixel
            start_x=50#posisi awal
            target_x=start_x+(d*scale)#posisi tujuan
            if d==0:#jika tidak ada perpindahan
                self.animation_running=False#hentikan animasi
            else:#jika ada perpindahan
                step=(target_x-start_x)/60#langkah per frame
                self.box_x+=step#geser posisi kotak
                if (step>0 and self.box_x>=target_x) or (step<0 and self.box_x<=target_x):#cek batas
                    self.box_x=target_x#kunci posisi akhir
                    self.animation_running=False#hentikan animasi
        else:#mode pegas
            self.animation_running=False#nonaktifkan animasi
        self.draw_vectors()#gambar ulang canvas
        if self.animation_running:#jika masih berjalan
            self.root.after(30,self.animate)#panggil frame berikutnya
        else:#jika selesai
            self.animate_btn.config(state=tk.NORMAL,bg="#119347")#aktifkan tombol

    #fungsi reset animasi
    def reset_animation(self):
        self.animation_running=False#matikan animasi
        self.box_x=50#kembalikan posisi kotak
        self.animate_btn.config(state=tk.NORMAL,bg="#27ae60")#reset tombol
        self.draw_vectors()#gambar ulang

    #fungsi menggambar objek dan vektor
    def draw_vectors(self):
        self.canvas.delete("all")#hapus canvas
        if self.force_type.get()==2:
            #mode pegas
            W,k,x,_,_,F_app=self.calculate_work() #ambil data pegas
            wall_x=20 #posisi tembok
            base_y=300 #posisi vertikal
            equilibrium_x=350 #titik setimbang
            pixel_scale=200#skala visual
            current_x=equilibrium_x+(x*pixel_scale) #posisi pegas
            self.canvas.create_rectangle(0,base_y-60,wall_x,base_y+60,fill="#7f8c8d",outline="gray") #gambar tembok
            self.canvas.create_line(0,base_y+70,750,base_y+70,fill="#bdc3c7",width=2)#gambar lantai
            self.canvas.create_line(equilibrium_x,base_y-80,equilibrium_x,base_y+80,fill="#2ecc71",dash=(4,4),width=2)#garis setimbang
            self.canvas.create_text(equilibrium_x,base_y-95,text="(Δx=0)",fill="#27ae60",font=("Arial",10))#label setimbang
            self.draw_spring(wall_x,base_y,current_x,coils=15,amplitude=25,color="#3498db") #gambar pegas
            grip_radius=15#radius jepitan
            self.canvas.create_oval(current_x-grip_radius,base_y-grip_radius,current_x+grip_radius,base_y+grip_radius,outline="black",width=3)#jepitan
            self.canvas.create_polygon(current_x+grip_radius, base_y-12,current_x+grip_radius+30,base_y-12,current_x+grip_radius+40,base_y,current_x+grip_radius+30,base_y+12,current_x+grip_radius,base_y+12,fill="#e74c3c",outline="black")#mesin penarik
            self.canvas.create_rectangle(current_x+grip_radius+40,base_y-5,750,base_y+5,fill="#ecf0f1",outline="#bdc3c7")#batang
            self.canvas.create_rectangle(50, 450, 400, 580, fill="#ffffff", outline="#bdc3c7", width=2)
            
            # Keterangan Gaya yang Dikenakan (Oranye)
            self.canvas.create_text(180, 480, text="Gaya yang dikenakan", font=("Arial", 12, "bold"), anchor="w")
            self.draw_arrow(self.canvas, 330, 480, 380, 480, color="#d35400", width=3, text="")
            
            # Keterangan Gaya Pegas (Biru)
            self.canvas.create_text(180, 530, text="Gaya Pegas", font=("Arial", 12, "bold"), anchor="w")
            self.draw_arrow(self.canvas, 380, 530, 330, 530, color="#2980b9", width=3, text="")
            
            # Simbol centang dekoratif (Opsional, agar mirip gambar)
            self.canvas.create_text(100, 480, text="✔", font=("Arial", 18), fill="#2c3e50")
            self.canvas.create_text(100, 530, text="✔", font=("Arial", 18), fill="#2c3e50")
            # --------------------------------------------------
            if abs(F_app)>0.1:  #jika gaya ada
                self.draw_arrow(self.canvas,current_x,base_y-50,current_x+F_app,base_y-50,color="#d35400",width=4,text=f"{F_app:.1f} N")#panah gaya luar
                self.draw_arrow(self.canvas,current_x,base_y-50,current_x-F_app,base_y-50,color="#2980b9",width=4,text=f"{-F_app:.1f} N")#panah gaya pegas
            if abs(x)>0.001:  #jika ada perpindahan
                self.draw_arrow(self.canvas,equilibrium_x,base_y+40,current_x,base_y+40,color="#2ecc71",width=3,text=f"\n\n\n\n\nΔx = {x:.2f} m")#panah perpindahan
            return#akhiri fungsi
        #mode gaya konstan
        F=self.force.get()#ambil gaya
        d=self.displacement.get()#ambil perpindahan
        theta_deg=self.angle.get()#ambil sudut
        theta_rad=math.radians(theta_deg)#ubah ke radian
        self.canvas.create_line(0,self.box_y+self.box_size/2+20,700,self.box_y+self.box_size/2+20,fill="#34495e",width=3)#gambar lantai
        box_x1=self.box_x-self.box_size/2#koordinat kiri kotak
        box_y1=self.box_y-self.box_size/2#koordinat atas kotak
        box_x2=self.box_x+self.box_size/2#koordinat kanan kotak
        box_y2=self.box_y+self.box_size/2#koordinat bawah kotak
        self.canvas.create_rectangle(box_x1,box_y1,box_x2,box_y2,fill="#e74c3c",outline="#c0392b",width=3)#gambar kotak
        self.canvas.create_text(self.box_x,self.box_y,text="m",font=("Arial",16,"bold"),fill="white")#label massa
        start_x=50#posisi awal vektor
        end_x=self.box_x if self.animation_running else 50+d*60#posisi akhir vektor
        self.draw_arrow(self.canvas,start_x,self.box_y+80,end_x,self.box_y+80,color="#2980b9",width=3,text=f"d⃗ = {(end_x-start_x)/60:.2f} m")#panah perpindahan
        force_length=F*5#skala gaya
        force_end_x=self.box_x+force_length*math.cos(theta_rad)#ujung gaya x
        force_end_y=self.box_y-force_length*math.sin(theta_rad)#ujung gaya y
        if not self.animation_running:#jika tidak animasi
            self.draw_arrow(self.canvas,self.box_x,self.box_y,force_end_x,force_end_y,color="#e74c3c",width=3,text=f"F⃗ = {F:.2f} N")#panah gaya
            fx_end=self.box_x+force_length*math.cos(theta_rad)#ujung fx
            fy_end=self.box_y-force_length*math.sin(theta_rad)#ujung fy
            self.canvas.create_line(self.box_x,self.box_y,fx_end,self.box_y,fill="#27ae60",width=2,dash=(5,3))#komponen fx
            self.canvas.create_line(fx_end,self.box_y,fx_end,fy_end,fill="#f39c12",width=2,dash=(5,3))#komponen fy

    #fungsi menggambar pegas
    def draw_spring(self,x1,y,x2,coils=12,amplitude=10,color="#8e44ad"):
        points= []#daftar titik pegas
        length = x2-x1#panjang pegas
        step = length/(coils*2)#jarak antar titik
        x = x1#posisi awal x
        direction=1#arah osilasi
        points.append((x1,y))#titik awal
        for _ in range(coils*2):#loop jumlah lilitan
            x+=step#geser x
            points.append((x,y+amplitude*direction))#tambah titik pegas
            direction*=-1#balik arah osilasi
        points.append((x2,y))#titik akhir
        for i in range(len(points)-1):#loop gambar garis
            self.canvas.create_line(points[i][0],points[i][1],points[i+1][0],points[i+1][1],width=4,fill=color,capstyle=tk.ROUND,joinstyle=tk.ROUND)#gambar segmen pegas

    #fungsi menggambar panah
    def draw_arrow(self,canvas,x1,y1,x2,y2,color,width,text):
        self.canvas.create_line(x1,y1,x2,y2,arrow=tk.LAST,fill=color,width=width,arrowshape=(12,15,5)) #gambar panah
        mid_x,mid_y=(x1+x2)/2,(y1+y2)/2 #titik tengah panah
        canvas.create_text(mid_x,mid_y-20,text=text,font=("Arial",12,"bold"),fill=color)#label panah

#eksekusi program utama
if __name__=="__main__":#entry point program
    root=tk.Tk()#buat window utama
    app=WorkSimulator(root)#inisialisasi aplikasi
    root.mainloop()#jalankan event loop
