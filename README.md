# Robotic Arm Simulator (Python & EMU8086 Integration) 🤖🐢

This project demonstrates a **Python-based 4DOF Robotic Arm Simulator** designed to interact with **EMU8086 assembly code** using I/O port communication.

---

## What it does

- Simulates a robotic arm with 4 degrees of freedom:
  - 3 rotational arms
  - 1 extendable arm segment
  - Gripper with open/close control
- Displays the arm visually using Python `turtle` graphics
- Communicates with **EMU8086** through a binary I/O file (`emu8086.io`), reading and writing port values
- Demonstrates how assembly IN/OUT instructions can control a Python GUI device in real-time

---

##  Requirements

- **Python 3.x**
- `turtle` library (standard)
- EMU8086 installed
- Path to `emu8086.io` correctly set in the Python script:
  ```py
  sIO_FILE = "C:\\emu8086\\emu8086.io"

---

## How to Run

1. **Prerequisites**
   - Python 3.x installed
   - Place your `emu8086.io` file at the path defined in the code (`sIO_FILE`).

2. **Run**
   ```bash
   python robotic_arm.py

---

⚠️ Note on Data
This repo contains no personal data. Example positions and movements are artificial and for demonstration only.

---

## Notes
Part of an educational project for learning hardware simulation, assembly, and Python GUIs.

