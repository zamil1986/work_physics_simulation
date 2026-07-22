<div align="center">

# Physics Work Simulation

An interactive desktop application for visualizing and calculating mechanical work produced by a constant force or a position-dependent spring force.

Built with Python and Tkinter.

</div>

## Overview

Physics Work Simulation is an educational desktop application that helps users understand the concept of **mechanical work** through calculations, vector visualization, and animation.

The application provides two simulation modes:

1. Work produced by a constant force
2. Work related to a spring based on Hooke's Law

Users can modify physical parameters and immediately observe how those changes affect the calculation and visualization.

## Features

- Interactive desktop GUI built with Tkinter
- Constant-force simulation
- Spring-force simulation
- Adjustable input values using sliders and text fields
- Real-time mechanical work calculations
- Force and displacement vector visualization
- Horizontal object movement animation
- Force-component visualization
- Spring extension visualization
- Work–energy theorem calculation
- Automatic final-velocity calculation
- Play and reset controls
- Scrollable input panel

## Tech Stack

- [Python](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- Python `math` module
- Object-Oriented Programming

The application only uses modules included with the standard Python installation, so it does not require third-party Python packages.

## Physics Concepts

### 1. Work Produced by a Constant Force

For a constant force applied at an angle, mechanical work is calculated using:

\[
W = F \cdot d \cdot \cos(\theta)
\]

Where:

- \(W\) = mechanical work in joules
- \(F\) = applied force in newtons
- \(d\) = displacement in meters
- \(\theta\) = angle between the force and displacement vectors

Only the component of force parallel to the displacement produces work:

\[
F_x = F\cos(\theta)
\]

Therefore:

\[
W = F_xd
\]

### 2. Hooke's Law

The relationship between spring force and extension is represented by Hooke's Law:

\[
F = kx
\]

The spring extension can therefore be calculated as:

\[
x = \frac{F}{k}
\]

Where:

- \(F\) = applied force in newtons
- \(k\) = spring constant in newtons per meter
- \(x\) = spring extension in meters

The magnitude of the work required to extend the spring is calculated using:

\[
W = \frac{1}{2}kx^2
\]

This value is also equal to the elastic potential energy stored in the spring.

> The spring force acts in the opposite direction to its displacement. Therefore, the work performed by the spring itself during extension has a negative sign, while the application displays the positive magnitude of the work required to extend it.

### 3. Work–Energy Theorem

The application also demonstrates the work–energy theorem:

\[
W_{\text{total}} = \Delta KE
\]

Assuming that the object starts from rest:

\[
W = \frac{1}{2}mv^2
\]

The final velocity is calculated using:

\[
v = \sqrt{\frac{2W}{m}}
\]

The current simulation assumes an object mass of:

\[
m = 2\text{ kg}
\]

## Simulation Modes

### Constant Force Mode

In this mode, users can configure:

- Applied force \(F\)
- Displacement \(d\)
- Force angle \(\theta\)

The application displays:

- The object and its movement
- Applied-force vector
- Horizontal and vertical force components
- Displacement vector
- Total mechanical work
- Final velocity based on the work–energy theorem

### Spring Force Mode

In this mode, users can configure:

- Spring constant \(k\)
- Applied pulling force \(F\)

The application displays:

- Spring and wall
- Equilibrium position
- Spring extension
- Applied-force vector
- Opposing spring-force vector
- Work required to extend the spring
- Final velocity based on the work–energy theorem

## Project Structure

```text
work_physics_simulation/
├── Simulasi_Usaha.py
└── README.md
```

The main program is organized inside the `WorkSimulator` class.

Important methods include:

| Method | Responsibility |
|---|---|
| `setup_gui()` | Creates the application interface |
| `create_input_field()` | Creates reusable inputs and sliders |
| `on_force_type_change()` | Changes the displayed simulation mode |
| `calculate_work()` | Performs the physics calculations |
| `update_calculation()` | Updates the calculation results |
| `start_animation()` | Starts the object animation |
| `animate()` | Updates each animation frame |
| `reset_animation()` | Resets the simulation |
| `draw_vectors()` | Draws objects, forces, and displacement vectors |
| `draw_spring()` | Draws the spring visualization |
| `draw_arrow()` | Draws reusable vector arrows |

## Getting Started

### Prerequisites

Make sure Python 3 is installed on your computer.

Check your Python installation using:

```bash
python --version
```

On some operating systems, use:

```bash
python3 --version
```

### 1. Clone the Repository

```bash
git clone https://github.com/zamil1986/work_physics_simulation.git
cd work_physics_simulation
```

### 2. Run the Application

On Windows:

```bash
python Simulasi_Usaha.py
```

On macOS or Linux:

```bash
python3 Simulasi_Usaha.py
```

## Linux Tkinter Setup

Some Linux distributions do not include Tkinter in the default Python installation.

For Ubuntu or Debian, install it using:

```bash
sudo apt update
sudo apt install python3-tk
```

After installation, run the application again:

```bash
python3 Simulasi_Usaha.py
```

## How to Use

1. Run `Simulasi_Usaha.py`.
2. Select **Gaya Konstan** or **Gaya Bergantung Posisi (Pegas)**.
3. Adjust the values using the sliders or input fields.
4. Observe the updated calculations in the result panel.
5. Click **Play** to run the constant-force movement animation.
6. Click **Reset** to restore the object to its initial position.

## Input Ranges

### Constant Force

| Input | Range | Unit |
|---|---:|---|
| Force | 0–100 | N |
| Displacement | 0–10 | m |
| Angle | 0–180 | degrees |

### Spring Force

| Input | Range | Unit |
|---|---:|---|
| Spring constant | 100–1000 | N/m |
| Applied force | -100–100 | N |

Values may also be entered manually through the input fields.

## Example Calculation

Suppose the following values are used in constant-force mode:

```text
Force       = 10 N
Displacement = 5 m
Angle        = 30°
```

The horizontal force component is:

\[
F_x = 10\cos(30^\circ)
\]

\[
F_x \approx 8.66\text{ N}
\]

The mechanical work is:

\[
W = 10 \times 5 \times \cos(30^\circ)
\]

\[
W \approx 43.30\text{ J}
\]

For an object with a mass of 2 kg that starts from rest:

\[
v = \sqrt{\frac{2(43.30)}{2}}
\]

\[
v \approx 6.58\text{ m/s}
\]

## Educational Purpose

This project can be used to study:

- Mechanical work
- Force vectors
- Vector components
- Displacement
- Hooke's Law
- Elastic potential energy
- Work–energy theorem
- Basic numerical visualization
- Event-driven programming
- Object-oriented Python
- Desktop GUI development with Tkinter

## Current Limitations

- The object mass is fixed at 2 kg.
- Friction is not included in the model.
- Constant-force movement is animated only horizontally.
- Spring mode currently provides a static visualization rather than an oscillation animation.
- The simulation uses visual scaling, so canvas distances are illustrative rather than physical measurements.
- Invalid manual text input is not yet handled with a dedicated error message.

## Roadmap

Future improvements may include:

- [ ] Make the object mass configurable
- [ ] Add kinetic and static friction
- [ ] Add spring oscillation animation
- [ ] Add configurable gravitational acceleration
- [ ] Add input-error handling
- [ ] Add work and force graphs
- [ ] Add kinetic and potential energy graphs
- [ ] Add simulation speed controls
- [ ] Add unit tests for physics calculations
- [ ] Separate physics logic from GUI code
- [ ] Export calculation results

## Contributors

This project was developed by Group 7:

- Muhammad Zamil
- Ayri
- Ezy

## Author

**Muhammad Zamil**

- GitHub: [@zamil1986](https://github.com/zamil1986)

## License

No license has been added to this project yet.
