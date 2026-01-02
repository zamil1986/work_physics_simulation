import tkinter as tk
from tkinter import ttk
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #embed matplotlib in tkinter


class WorkSimulator:
    #constructor
    def __init__(self, root):
        self.root = root
        self.root.title("Simulasi Usaha oleh Gaya")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")

        #variable animasi awal
        self.box_x = 50  # Starting position of the box
        self.box_y = 300  # Vertical position (constant)
        self.box_size = 40
        self.animation_running = False
        self.animation_frame = 0
        self.total_frames = 60  # Smooth animation over 60 frames

        #value awal
        self.force = tk.DoubleVar(value=10.0)
        self.displacement = tk.DoubleVar(value=5.0)
        self.angle = tk.DoubleVar(value=30.0)
        self.force_type = tk.IntVar(value=1)

        self.setup_gui()

    def setup_gui(self):
        #panel kiri
        left_container = tk.Frame(self.root, bg="#f0f0f0")
        left_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        #scroller
        canvas = tk.Canvas(
            left_container, bg="#f0f0f0", highlightthickness=0, width=350
        )
        scrollbar = ttk.Scrollbar(
            left_container, orient="vertical", command=canvas.yview
        )

        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # This frame is the REAL input panel
        left_frame = tk.Frame(canvas, bg="#ffffff", padx=20, pady=20)

        canvas.create_window((0, 0), window=left_frame, anchor="nw")

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        left_frame.bind("<Configure>", on_configure)


        #title
        title = tk.Label(
            left_frame,
            text="Control Panel",
            font=("Arial", 25, "bold"),
            bg="#ffffff",
            fg="#2c3e50",
        )
        title.pack(pady=(0, 20))

        #pilihan gaya
        option_frame = tk.LabelFrame(
            left_frame,
            text="Jenis Gaya",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            padx=10,
            pady=5,
        )
        option_frame.pack(fill=tk.X, pady=10)

        rb_constant = tk.Radiobutton(
            option_frame,
            text="Gaya Konstan",
            variable=self.force_type,
            value=1,
            bg="#ffffff",
            command=self.on_force_type_change,
        )
        rb_constant.pack(anchor="w")

        rb_spring = tk.Radiobutton(
            option_frame,
            text="Gaya Bergantung Posisi (Pegas)",
            variable=self.force_type,
            value=2,
            bg="#ffffff",
            command=self.on_force_type_change,
        )
        rb_spring.pack(anchor="w")

        # Panggon Input
        self.force_frame, self.force_label = self.create_input_field(
            left_frame, "Gaya(F)[N]:", self.force, 0, 100
            )
        

        self.disp_frame, self.disp_label = self.create_input_field(
            left_frame, "Perpindahan(d)[m]:", self.displacement, 0, 10
            )

        self.angle_frame, self.angle_label = self.create_input_field(
            left_frame, "Sudut(θ)[°]:", self.angle, 0, 180
            )

      
        #Play,Reset,Show Graph
        self.btn_frame = tk.Frame(left_frame, bg="#ffffff")
        self.btn_frame.pack(pady=20)

        
        self.animate_btn = tk.Button(
            self.btn_frame,
            text="Play",
            command=self.start_animation,
            font=("Arial", 12, "bold"),
            bg="#119347",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2",
        )
        self.animate_btn.pack(pady=5, fill=tk.X)
        
        reset_btn = tk.Button(
            self.btn_frame,
            text="Reset",
            command=self.reset_animation,
            font=("Arial", 12, "bold"),
            bg="#d80d0d",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2",
        )
        reset_btn.pack(pady=5, fill=tk.X)

        graph_btn = tk.Button(
            self.btn_frame,
            text="Show Graph",
            command=self.show_graph,
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2",
        )
        graph_btn.pack(pady=5, fill=tk.X)

        # Results Information Box
        self.result_frame = tk.LabelFrame(
            left_frame,
            text="Kotak Hasil Hitung",
            font=("Arial", 20, "bold"),
            bg="#ffffff",
            padx=10,
            pady=10,
        )
        self.result_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        self.result_text = tk.Text(
            self.result_frame,
            height=15,
            width=35,
            font=("Courier", 10),
            wrap=tk.WORD,
            bg="#ecf0f1",
            relief=tk.FLAT,
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # Canvas Animasi
        right_frame = tk.Frame(self.root, bg="#ffffff")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        canvas_label = tk.Label(
            right_frame,
            text="Canvas Visualisasi",
            font=("Arial", 30, "bold"),
            bg="#ffffff",
        )
        canvas_label.pack(pady=(0, 10))

        self.canvas = tk.Canvas(
            right_frame,
            width=700,
            height=600,
            bg="#fafafa",
            highlightthickness=2,
            highlightbackground="#bdc3c7",
        )
        self.canvas.pack()

        # Initial calculation display
        self.update_calculation()

    def on_force_type_change(self):
        if self.force_type.get() == 1:
            #GAYA KONSTAN
            self.force_label.config(text="Force (F) [N]:")
            self.disp_label.config(text="Perpindahan (d) [m]")
            self.angle_frame.pack(
                pady=10,
                fill=tk.X,
                before=self.btn_frame
        )

            self.angle.set(30)

        else:
        #PEGAS
            self.force_label.config(text="Spring Constant (k) [N/m]:")
            self.disp_label.config(text="Pertambahan Panjang Pegas (x) [m]")
            self.angle_frame.pack_forget()
            self.angle.set(0)

        self.update_calculation()
        self.draw_vectors()

    def create_input_field(self, parent, label_text, variable, min_val, max_val):
        frame = tk.Frame(parent, bg="#ffffff")
        frame.pack(pady=10, fill=tk.X)

        label = tk.Label(
            frame, text=label_text, font=("Arial", 11), bg="#ffffff", anchor="w"
        )
        label.pack(anchor="w")

        entry = tk.Entry(
            frame,
            textvariable=variable,
            font=("Arial", 12),
            width=15,
            relief=tk.SOLID,
            borderwidth=1,
        )
        entry.pack(pady=(5, 5))

        slider = ttk.Scale(
            frame,
            from_=min_val,
            to=max_val,
            variable=variable,
            orient=tk.HORIZONTAL,
            command=lambda x: self.update_calculation(),
        )
        slider.pack(fill=tk.X)

        entry.bind("<KeyRelease>", lambda e: self.update_calculation())

        return frame, label

    def calculate_work(self):
        d = self.displacement.get()

        if self.force_type.get() == 1:
            #KONSTAN
            F = self.force.get()
            theta_deg = self.angle.get()
            theta_rad = math.radians(theta_deg)
            W = F * d * math.cos(theta_rad)

        else:
            #PEGAS
            k = self.force.get()
            W = 0.5 * k * d**2

            theta_deg = 0
            theta_rad = 0

        return W, self.force.get(), d, theta_deg, theta_rad

    def update_calculation(self):
        W, F, d, theta_deg, theta_rad = self.calculate_work()

        # Clear and update result text
        self.result_text.delete(1.0, tk.END)
        if self.force_type.get() == 1:
            result = f"""
╔═══════════════════════════════╗
║    Usaha oleh Gaya Konstan    ║
╚═══════════════════════════════╝

Formula:
  W = F⃗ · d⃗ = F × d × cos(θ)
Keterangan:
  W = Usaha (J)
  d = Perpindahan (m)
  θ = Sudut (°)

Nilai yang diberikan:
  F = {F:.2f} N
  d = {d:.2f} m

Hitung:
  W = {F:.2f} × {d:.2f} × cos({theta_deg:.1f}°)
  W = {F:.2f} × {d:.2f} × {math.cos(theta_rad):.4f}
  W = {W:.2f} J

Komponen gaya:
  Fx = F cos(θ) = {F * math.cos(theta_rad):.2f} N
  Fy = F sin(θ) = {F * math.sin(theta_rad):.2f} N

Teorema Usaha Energi:  
    𝐾𝐸final − 𝐾𝐸initial = ΔKE
     = Wtot(Usaha Total) = {W:.2f} J

"""
            self.result_text.insert(1.0, result)
        else:
            result = f"""
╔═══════════════════════════════╗
║     Usaha oleh Gaya Pegas     ║
╚═══════════════════════════════╝

Formula:
  W = ½ × k × x²
Keterangan:
  W = Usaha (J)
  k = Konstanta Pegas (N/m)
  x = Pertambahan panjang pegas (m)

Nilai yang diberikan:
  k = {F:.2f} N
  x = {d:.2f} m

Hitung:
  W =  0.5 × {F:.2f} × ({d:.2f})²
  W =  {W:.2f} J
  
Gaya yang diberikan:
  F = k * x = {F:.2f}*{d:.2f}
    = {F*d:.2f}

Teorema Usaha-Energi:  
    𝐾𝐸final − 𝐾𝐸initial = ΔKE 
    = Wtot(Usaha Total) = {W:.2f}

"""
            self.result_text.insert(1.0, result)

        # Redraw static vectors if not animating
        if not self.animation_running:
            self.draw_vectors()

    def start_animation(self):
        """Start the animation sequence"""
        if not self.animation_running:
            self.animation_running = True
            self.animation_frame = 0
            self.box_x = 50
            self.animate_btn.config(state=tk.DISABLED, bg="#95a5a6")
            self.animate()

    def animate(self):
        """Animate the box movement frame by frame"""
        if not self.animation_running:
            return

        # Calculate displacement per frame
        d = self.displacement.get()
        scale = 60  # pixels per meter
        total_pixels = d * scale
        pixels_per_frame = total_pixels / self.total_frames

        # Update box position
        self.box_x += pixels_per_frame
        self.animation_frame += 1

        # Draw current frame
        self.draw_vectors()

        # Continue animation or finish
        if self.animation_frame < self.total_frames:
            self.root.after(30, self.animate)  # ~33 fps
        else:
            self.animation_running = False
            self.animate_btn.config(state=tk.NORMAL, bg="#27ae60")

    def reset_animation(self):
        """Reset animation to initial state"""
        self.animation_running = False
        self.animation_frame = 0
        self.box_x = 50
        self.animate_btn.config(state=tk.NORMAL, bg="#27ae60")
        self.draw_vectors()

    def draw_vectors(self):
        """Draw all vectors and the animated box on canvas"""
        # ===== SPRING MODE =====
        if self.force_type.get() == 2:
            self.canvas.delete("all")

            wall_x = 80
            y = self.box_y

            # Wall
            self.canvas.create_rectangle(
                wall_x - 15, y - 40, wall_x, y + 40, fill="#2c3e50"
            )

            # Box
            box_left = self.box_x - self.box_size / 2
            box_right = self.box_x + self.box_size / 2

            self.canvas.create_rectangle(
                box_left,
                y - self.box_size / 2,
                box_right,
                y + self.box_size / 2,
                fill="#e74c3c",
                outline="#c0392b",
                width=3,
            )

            # Spring
            self.draw_spring(wall_x, y, box_left)

            return

        self.canvas.delete("all")

        # Get current values
        F = self.force.get()
        d = self.displacement.get()
        theta_deg = self.angle.get()
        theta_rad = math.radians(theta_deg)

        # Scaling factors
        force_scale = 30  # pixels per Newton
        displacement_scale = 60  # pixels per meter

        # Draw ground line
        self.canvas.create_line(
            0,
            self.box_y + self.box_size / 2 + 20,
            700,
            self.box_y + self.box_size / 2 + 20,
            fill="#34495e",
            width=3,
        )

        # Draw the box (object being moved)
        box_x1 = self.box_x - self.box_size / 2
        box_y1 = self.box_y - self.box_size / 2
        box_x2 = self.box_x + self.box_size / 2
        box_y2 = self.box_y + self.box_size / 2

        self.canvas.create_rectangle(
            box_x1, box_y1, box_x2, box_y2, fill="#e74c3c", outline="#c0392b", width=3
        )
        self.canvas.create_text(
            self.box_x, self.box_y, text="m", font=("Arial", 16, "bold"), fill="white"
        )

        # Draw displacement vector (always horizontal, from start to current position)
        start_x = 50
        end_x = 50 + d * displacement_scale
        self.draw_arrow(
            self.canvas,
            start_x,
            self.box_y + 80,
            end_x,
            self.box_y + 80,
            color="#2980b9",
            width=3,
            text=(f"d = {self.displacement.get():.2f} m"),
        )

        # Draw force vector from box at angle θ
        force_length = F * force_scale
        force_end_x = self.box_x + force_length * math.cos(theta_rad)
        force_end_y = self.box_y - force_length * math.sin(theta_rad)
        if not self.animation_running:
            self.draw_arrow(
                self.canvas,
                self.box_x,
                self.box_y,
                force_end_x,
                force_end_y,
                color="#e74c3c",
                width=3,
                text=(f"F = {self.force.get():.2f} N"),
            )

        # Draw force components (dashed lines)
        # Horizontal component: F cos(θ)
        if not self.animation_running:
            fx_end = self.box_x + force_length * math.cos(theta_rad)
            self.canvas.create_line(
                self.box_x,
                self.box_y,
                fx_end,
                self.box_y,
                fill="#27ae60",
                width=2,
                dash=(5, 3),
            )
            self.canvas.create_text(
                self.box_x + force_length * math.cos(theta_rad) / 2,
                self.box_y - 15,
                text="Fx = F cos(θ)",
                font=("Arial", 10),
                fill="#27ae60",
            )

            # Vertical component: F sin(θ)
            fy_end = self.box_y - force_length * math.sin(theta_rad)
            self.canvas.create_line(
                fx_end, self.box_y, fx_end, fy_end, fill="#f39c12", width=2, dash=(5, 3)
            )
            self.canvas.create_text(
                fx_end + 50,
                (self.box_y + fy_end) / 2,
                text="Fy = F sin(θ)",
                font=("Arial", 10),
                fill="#f39c12",
            )

            # Draw angle arc
            if abs(theta_deg) > 0.1 and abs(theta_deg - 180) > 0.1:
                arc_radius = 50
                self.canvas.create_arc(
                    self.box_x - arc_radius,
                    self.box_y - arc_radius,
                    self.box_x + arc_radius,
                    self.box_y + arc_radius,
                    start=0,
                    extent=theta_deg,
                    style=tk.ARC,
                    outline="#9b59b6",
                    width=2,
                )

                # Angle label
                label_angle_rad = theta_rad / 2
                label_x = self.box_x + 35 * math.cos(label_angle_rad)
                label_y = self.box_y - 35 * math.sin(label_angle_rad)
                self.canvas.create_text(
                    label_x,
                    label_y,
                    text="θ",
                    font=("Arial", 14, "bold"),
                    fill="#9b59b6",
                )

                # Draw legend
                legend_y = 50
                self.canvas.create_text(
                    350,
                    legend_y,
                    text="θ is the angle between F⃗ and d⃗",
                    font=("Arial", 11, "italic"),
                    fill="#2c3e50",
                )

        # Draw coordinate system
        self.canvas.create_line(
            630, 550, 680, 550, arrow=tk.LAST, fill="#34495e", width=2
        )
        self.canvas.create_line(
            630, 550, 630, 500, arrow=tk.LAST, fill="#34495e", width=2
        )
        self.canvas.create_text(690, 550, text="x", font=("Arial", 10, "bold"))
        self.canvas.create_text(630, 490, text="y", font=("Arial", 10, "bold"))

    def draw_spring(self, x1, y, x2, coils=12, amplitude=10, color="#8e44ad"):
        """
        Draw a horizontal spring from x1 to x2 at height y
        """
        if x2 <= x1:
            return

        points = []
        length = x2 - x1
        step = length / (coils * 2)

        x = x1
        direction = 1

        points.append((x1, y))

        for _ in range(coils * 2):
            x += step
            points.append((x, y + amplitude * direction))
            direction *= -1

        points.append((x2, y))

        for i in range(len(points) - 1):
            self.canvas.create_line(
                points[i][0],
                points[i][1],
                points[i + 1][0],
                points[i + 1][1],
                width=3,
                fill=color,
            )

    def draw_arrow(self, canvas, x1, y1, x2, y2, color, width, text):
        """Draw an arrow with label"""
        canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            arrow=tk.LAST,
            fill=color,
            width=width,
            arrowshape=(12, 15, 5),
        )
        # Label at midpoint
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        canvas.create_text(
            mid_x, mid_y - 20, text=text, font=("Arial", 12, "bold"), fill=color
        )

    def show_graph(self):
        # Window Baru untuk grafik
        graph_window = tk.Toplevel(self.root)
        graph_window.geometry("720x600")

        fig, ax = plt.subplots(figsize=(8, 6))

        d = self.displacement.get()
        F = self.force.get()
        angle_deg = self.angle.get()
        angle = math.cos(math.radians(angle_deg))


        # Gaya Konstan
        if self.force_type.get() == 1:
            graph_window.title("Grafik Gaya(F) - Perpindahan(d)")
            F *=angle

            x_vals = [0, d]
            F_vals = [F, F]

            ax.plot(x_vals, F_vals, linewidth=3, label="F Konstan")
            ax.fill_between(x_vals, 0, F_vals, alpha=0.3)

            ax.set_title("Usaha oleh Gaya Konstan\nUsaha adalah luas daerah dibawah kurva")

            work_text = f"W = {F*d:.2f} J"
            ax.set_xlabel("Perpindahan(d)[m]", fontsize=11)


        # Gaya Pegas (HOOKE)
        else:
            k=F
            graph_window.title("Grafik Gaya(k*x) - Pertambahan panjang pegas(x)")
            x_vals = [i * d / 100 for i in range(101)]
            F_vals = [k * x for x in x_vals]

            ax.plot(x_vals, F_vals, linewidth=3, label="F = kx")
            ax.fill_between(x_vals, 0, F_vals, alpha=0.3)

            ax.set_title("Usaha oleh Gaya Pegas(Hooke)\nUsaha adalah luas kurva yang diarsir")

            work_text = f"W = {0.5*k*d*d:.2f} J"
            ax.set_xlabel("Pertambahan panjang pegas(x)[m]", fontsize=11)

        # Peletakan 
        
        ax.set_ylabel("Gaya(F)[N]", fontsize=11)
        ax.grid(True)
        ax.legend()

        ax.text(
            0.5,
            0.95,
            work_text,
            transform=ax.transAxes,
            fontsize=11,
            verticalalignment="top",
            horizontalalignment="center",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.6),
        )

        # Embed matplotlib into Tkinter
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = WorkSimulator(root)
    root.mainloop()
