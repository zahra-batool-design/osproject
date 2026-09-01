# 🚗 Smart Campus Parking OS Simulator

A Python + Streamlit project that demonstrates core **Operating System concepts** through a smart campus parking system.

## ✨ Features

- 📋 **Gate Scheduling** — Priority-based scheduling for Faculty and Student cars.
- 🚦 **Counting Semaphore** — Controls available parking spaces and waiting cars.
- 🔒 **Mutex Synchronization** — Prevents multiple cars from accessing Spot #12 simultaneously.
- 🚨 **Deadlock Detection & Resolution** — Detects cars stuck on a single-lane ramp and resolves the deadlock by forcing one car to reverse.

## 🧠 OS Concepts

| Concept | Implementation |
|---|---|
| Priority Scheduling | Gate management |
| Queue | Waiting cars |
| Semaphore | Parking capacity |
| Mutex | Spot #12 protection |
| Deadlock | Opposite-direction ramp traffic |
| Deadlock Resolution | Force one car to reverse |

## 🛠️ Technologies

- Python
- Streamlit

## 📂 Project Structure

```text
Smart-Campus-Parking-OS-Simulator/
├── app.py
├── requirements.txt
├── README.md
└── screenshots/
    ├── gate-scheduling.png
    ├── semaphore.png
    ├── mutex.png
    ├── deadlock-detection.png
    └── deadlock-resolution.png
