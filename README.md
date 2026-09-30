# Unified Quantum-Safe Communication Framework
### End-to-End Integration of QKD, Resilient State Backbone, and Post-Quantum Cryptography

An architectural implementation bridging **UC-024 (PQC Migration)**, **UC-025 (Quantum Key Distribution)**, and **UC-030 (State Quantum Backbone)** for the Plus Qiskit Fall Fest 2026.

---

## 📌 Project Overview
Classical digital communication infrastructures relying on RSA and ECC are vulnerable to quantum cryptanalysis via Shor's Algorithm and present-day "Harvest-Now, Decrypt-Later" (HNDL) threats. 

This repository implements a **3-Layer Defense-in-Depth Model**:
1. **Layer 1 (Physical Plane - UC-025):** Hardware-level BB84 QKD protocol simulation using Qiskit.
2. **Layer 2 (Network Plane - UC-030):** Automated QBER monitoring engine with an 11% threshold failover lock.
3. **Layer 3 (Application Plane - UC-024):** Quantum-derived key orchestration with symmetric AES-256-GCM authenticated payload encryption.

---

## 🛠 Tech Stack
- **Quantum Simulation:** Qiskit 1.x, Qiskit Aer
- **Cryptographic Engine:** Cryptography (AES-256-GCM), Open Quantum Safe (`liboqs`)
- **Language:** Python 3.10+

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone [https://github.com/](https://github.com/)[YOUR_USERNAME]/quantum-safe-backbone.git
cd quantum-safe-backbone
