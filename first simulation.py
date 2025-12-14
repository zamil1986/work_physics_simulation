import tkinter as tk
from tkinter import ttk
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class WorkSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Physics: Work Done by Force (W = F⃗·d⃗)")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")
        
        # Animation variables
        self.box_x = 50  # Starting position of the box
        self.box_y = 300  # Vertical position (constant)
        self.box_size = 40
        self.animation_running = False
        self.animation_frame = 0
        self.total_frames = 60  # Smooth animation over 60 frames
        
        # Physics values
        self.force = tk.DoubleVar(value=10.0)
        self.displacement = tk.DoubleVar(value=5.0)
        self.angle = tk.DoubleVar(value=30.0)
        
        self.setup_gui()
        
    def setup_gui(self):
        """Create the main GUI layout with input panel and canvas"""
        # Left Panel - Input Controls
        left_frame = tk.Frame(self.root, bg="#ffffff", padx=20, pady=20)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Title
        title = tk.Label(left_frame, text="Work by Force Simulator", 
                        font=("Arial", 18, "bold"), bg="#ffffff", fg="#2c3e50")
        title.pack(pady=(0, 20))
        
        # Input fields
        self.create_input_field(left_frame, "Force (F) [N]:", self.force, 0, 100)
        self.create_input_field(left_frame, "Displacement (d) [m]:", self.displacement, 0, 10)
        self.create_input_field(left_frame, "Angle (θ) [degrees]:", self.angle, 0, 180)
        
        # Control buttons
        btn_frame = tk.Frame(left_frame, bg="#ffffff")
        btn_frame.pack(pady=20)
        
        self.animate_btn = tk.Button(btn_frame, text="Play", 
                                     command=self.start_animation,
                                     font=("Arial", 12, "bold"),
                                     bg="#27ae60", fg="white",
                                     padx=20, pady=10, cursor="hand2")
        self.animate_btn.pack(pady=5, fill=tk.X)
        
        reset_btn = tk.Button(btn_frame, text="Reset", 
                             command=self.reset_animation,
                             font=("Arial", 12),
                             bg="#b02525", fg="white",
                             padx=20, pady=10, cursor="hand2")
        reset_btn.pack(pady=5, fill=tk.X)
        
        graph_btn = tk.Button(btn_frame, text="Show F-d Graph", 
                             command=self.show_graph,
                             font=("Arial", 12),
                             bg="#3498db", fg="white",
                             padx=20, pady=10, cursor="hand2")
        graph_btn.pack(pady=5, fill=tk.X)
        
        # Results display
        self.result_frame = tk.LabelFrame(left_frame, text="Work Calculation", 
                                         font=("Arial", 12, "bold"),
                                         bg="#ffffff", padx=10, pady=10)
        self.result_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        self.result_text = tk.Text(self.result_frame, height=15, width=35,
                                   font=("Courier", 10), wrap=tk.WORD,
                                   bg="#ecf0f1", relief=tk.FLAT)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Right Panel - Canvas for animation
        right_frame = tk.Frame(self.root, bg="#ffffff")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        canvas_label = tk.Label(right_frame, text="Vector Animation & Visualization",
                               font=("Arial", 14, "bold"), bg="#ffffff")
        canvas_label.pack(pady=(0, 10))
        
        self.canvas = tk.Canvas(right_frame, width=700, height=600, 
                               bg="#fafafa", highlightthickness=2,
                               highlightbackground="#bdc3c7")
        self.canvas.pack()
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Initial calculation display
        self.update_calculation()
        
    def create_input_field(self, parent, label_text, variable, min_val, max_val):
        """Create an input field with slider"""
        frame = tk.Frame(parent, bg="#ffffff")
        frame.pack(pady=10, fill=tk.X)
        
        label = tk.Label(frame, text=label_text, font=("Arial", 11),
                        bg="#ffffff", anchor="w")
        label.pack(anchor="w")
        
        entry = tk.Entry(frame, textvariable=variable, font=("Arial", 12),
                        width=15, relief=tk.SOLID, borderwidth=1)
        entry.pack(pady=(5, 5))
        
        slider = ttk.Scale(frame, from_=min_val, to=max_val, 
                          variable=variable, orient=tk.HORIZONTAL,
                          command=lambda x: self.update_calculation())
        slider.pack(fill=tk.X)
        
        entry.bind("<KeyRelease>", lambda e: self.update_calculation())
        
    def calculate_work(self):
        """Calculate work done by force using W = F·d·cos(θ)"""
        F = self.force.get()
        d = self.displacement.get()
        theta_deg = self.angle.get()
        theta_rad = math.radians(theta_deg)
        
        # Physics rules implementation
        if d == 0:
            # No displacement → no work done
            W = 0
            interpretation = "No work (d = 0)"
        elif abs(theta_deg - 90) < 0.01:
            # Force perpendicular to displacement → no work
            W = 0
            interpretation = "No work (θ = 90°, force ⊥ displacement)"
        elif abs(theta_deg) < 0.01:
            # Force parallel to displacement → maximum positive work
            W = F * d
            interpretation = "Maximum positive work (θ = 0°)"
        elif abs(theta_deg - 180) < 0.01:
            # Force opposite to displacement → maximum negative work
            W = -F * d
            interpretation = "Maximum negative work (θ = 180°)"
        else:
            # General case
            W = F * d * math.cos(theta_rad)
            if W > 0:
                interpretation = "Positive work (force helps motion)"
            elif W < 0:
                interpretation = "Negative work (force opposes motion)"
            else:
                interpretation = "Zero work"
        
        return W, interpretation, F, d, theta_deg, theta_rad
    
    def update_calculation(self):
        """Update the work calculation display"""
        W, interp, F, d, theta_deg, theta_rad = self.calculate_work()
        
        # Clear and update result text
        self.result_text.delete(1.0, tk.END)
        
        result = f"""
╔═══════════════════════════════╗
║     WORK CALCULATION          ║
╚═══════════════════════════════╝

Formula:
  W = F⃗ · d⃗ = F × d × cos(θ)

Given Values:
  F = {F:.2f} N
  d = {d:.2f} m
  θ = {theta_deg:.1f}°

Substitution:
  W = {F:.2f} × {d:.2f} × cos({theta_deg:.1f}°)
  W = {F:.2f} × {d:.2f} × {math.cos(theta_rad):.4f}

Result:
  W = {W:.2f} Joules (J)

Interpretation:
  {interp}

Force Components:
  Fx = F cos(θ) = {F * math.cos(theta_rad):.2f} N
  Fy = F sin(θ) = {F * math.sin(theta_rad):.2f} N
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
        self.canvas.create_line(0, self.box_y + self.box_size/2 + 20, 
                               700, self.box_y + self.box_size/2 + 20,
                               fill="#34495e", width=3)
        
        # Draw the box (object being moved)
        box_x1 = self.box_x - self.box_size/2
        box_y1 = self.box_y - self.box_size/2
        box_x2 = self.box_x + self.box_size/2
        box_y2 = self.box_y + self.box_size/2
        
        self.canvas.create_rectangle(box_x1, box_y1, box_x2, box_y2,
                                    fill="#e74c3c", outline="#c0392b", width=3)
        self.canvas.create_text(self.box_x, self.box_y, text="m",
                               font=("Arial", 16, "bold"), fill="white")
        
        # Draw displacement vector (always horizontal, from start to current position)
        start_x = 50
        end_x = 50 + d * displacement_scale
        self.draw_arrow(self.canvas, start_x, self.box_y + 80, 
                       end_x, self.box_y + 80,
                       color="#2980b9", width=3, text="d⃗")
        
        # Draw force vector from box at angle θ
        force_length = F * force_scale
        force_end_x = self.box_x + force_length * math.cos(theta_rad)
        force_end_y = self.box_y - force_length * math.sin(theta_rad)
        
        self.draw_arrow(self.canvas, self.box_x, self.box_y,
                       force_end_x, force_end_y,
                       color="#e74c3c", width=3, text="F⃗")
        
        # Draw force components (dashed lines)
        # Horizontal component: F cos(θ)
        fx_end = self.box_x + force_length * math.cos(theta_rad)
        self.canvas.create_line(self.box_x, self.box_y, fx_end, self.box_y,
                               fill="#27ae60", width=2, dash=(5, 3))
        self.canvas.create_text(self.box_x + force_length * math.cos(theta_rad) / 2,
                               self.box_y - 15, text="Fx = F cos(θ)",
                               font=("Arial", 10), fill="#27ae60")
        
        # Vertical component: F sin(θ)
        fy_end = self.box_y - force_length * math.sin(theta_rad)
        self.canvas.create_line(fx_end, self.box_y, fx_end, fy_end,
                               fill="#f39c12", width=2, dash=(5, 3))
        self.canvas.create_text(fx_end + 50, (self.box_y + fy_end) / 2,
                               text="Fy = F sin(θ)",
                               font=("Arial", 10), fill="#f39c12")
        
        # Draw angle arc
        if abs(theta_deg) > 0.1 and abs(theta_deg - 180) > 0.1:
            arc_radius = 50
            self.canvas.create_arc(self.box_x - arc_radius, 
                                  self.box_y - arc_radius,
                                  self.box_x + arc_radius, 
                                  self.box_y + arc_radius,
                                  start=0, extent=theta_deg,
                                  style=tk.ARC, outline="#9b59b6", width=2)
            
            # Angle label
            label_angle_rad = theta_rad / 2
            label_x = self.box_x + 35 * math.cos(label_angle_rad)
            label_y = self.box_y - 35 * math.sin(label_angle_rad)
            self.canvas.create_text(label_x, label_y, text="θ",
                                   font=("Arial", 14, "bold"), fill="#9b59b6")
        
        # Draw legend
        legend_y = 50
        self.canvas.create_text(350, legend_y, 
                               text="θ is the angle between F⃗ and d⃗",
                               font=("Arial", 11, "italic"), fill="#2c3e50")
        
        # Draw coordinate system
        self.canvas.create_line(630, 550, 680, 550, 
                               arrow=tk.LAST, fill="#34495e", width=2)
        self.canvas.create_line(630, 550, 630, 500, 
                               arrow=tk.LAST, fill="#34495e", width=2)
        self.canvas.create_text(690, 550, text="x", font=("Arial", 10, "bold"))
        self.canvas.create_text(630, 490, text="y", font=("Arial", 10, "bold"))
    
    def draw_arrow(self, canvas, x1, y1, x2, y2, color, width, text):
        """Draw an arrow with label"""
        canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, 
                          fill=color, width=width, arrowshape=(12, 15, 5))
        # Label at midpoint
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        canvas.create_text(mid_x, mid_y - 20, text=text,
                          font=("Arial", 12, "bold"), fill=color)
    
    def show_graph(self):
        """Display Force vs Displacement graph with work as area"""
        F = self.force.get()
        d = self.displacement.get()
        W, interp, _, _, _, _ = self.calculate_work()
        
        # Create new window for graph
        graph_window = tk.Toplevel(self.root)
        graph_window.title("Force-Displacement Graph")
        graph_window.geometry("700x600")
        
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Plot constant force
        displacements = [0, d]
        forces = [F, F]
        
        ax.plot(displacements, forces, 'b-', linewidth=3, label='Force (constant)')
        ax.fill_between(displacements, 0, forces, alpha=0.3, 
                       color='cyan', label=f'Work = {abs(W):.2f} J')
        
        # Formatting
        ax.set_xlabel('Displacement d (m)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Force F (N)', fontsize=12, fontweight='bold')
        ax.set_title('Force vs Displacement\n(Area under curve = Work done)', 
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=11)
        ax.set_xlim(-0.1 * d if d > 0 else -1, d * 1.2 if d > 0 else 1)
        ax.set_ylim(0, F * 1.3 if F > 0 else 1)
        
        # Add explanation text
        explanation = (f"For constant force:\n"
                      f"Work = Area = F × d = {F:.2f} × {d:.2f} = {F*d:.2f} J\n"
                      f"Actual work considering angle: W = {W:.2f} J")
        ax.text(0.5, 0.95, explanation, transform=ax.transAxes,
               fontsize=10, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
               horizontalalignment='center')
        
        # Embed in tkinter
        canvas_widget = FigureCanvasTkAgg(fig, master=graph_window)
        canvas_widget.draw()
        canvas_widget.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add explanation label
        info_text = tk.Label(graph_window, 
                            text="The magnitude of work equals the area under the F-d curve.\n"
                                 "Note: This shows F·d; actual work includes cos(θ) factor.",
                            font=("Arial", 10), bg="#ecf0f1", pady=10)
        info_text.pack(fill=tk.X)

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = WorkSimulator(root)
    root.mainloop()
