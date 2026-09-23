# Cloud Computing Laboratory Coursework
### Practical Experiments, Benchmarks, and Technical Reports

![Course](https://img.shields.io/badge/Course-Cloud_Computing_Laboratory-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active_Coursework-success?style=for-the-badge)
![Maintained](https://img.shields.io/badge/Maintained-Yes-brightgreen?style=for-the-badge)

Welcome to the **Cloud Computing Laboratory** repository. This repository serves as a centralized portfolio housing all practical experiments, automated benchmarking scripts, infrastructure analysis, and formal laboratory reports conducted throughout the course.

---

## 📚 Laboratory Experiments Index

| Exp No. | Practical Topic | Virtualization / Cloud Tech | Report & Artifacts | Status |
| :---: | :--- | :--- | :---: | :---: |
| **01** | **Comparative CPU Performance Assessment of Type-1 vs. Type-2 Hypervisors** | Proxmox VE (KVM), VMware Workstation, Sysbench | [📂 View Lab 01](./Lab-01-Hypervisor-Benchmarking/) <br> [📄 Read Report](./Lab-01-Hypervisor-Benchmarking/Lab%20Report.md) | ✅ Completed |
| **02** | *Upcoming Lab Practical* | *TBD* | — | ⏳ In Progress |
| **03** | *Upcoming Lab Practical* | *TBD* | — | ⏳ Upcoming |
| **04** | *Upcoming Lab Practical* | *TBD* | — | ⏳ Upcoming |

---

## 🗂️ Repository Architecture

To maintain modularity and avoid file collisions across different lab assignments, each experiment is structured in its own self-contained directory:

```text
cc-lab/
├── README.md                                  # Master index and course documentation
│
├── Lab-01-Hypervisor-Benchmarking/            # Experiment 01
│   ├── Lab Report.md                          # Full academic report with LaTeX math & data
│   ├── README.md                              # Lab 01 walkthrough & reproduction guide
│   ├── images/                                # High-res generated charts & terminal screenshots
│   │   ├── events_per_second_comparison.png
│   │   ├── latency_comparison.png
│   │   ├── total_events_comparison.png
│   │   ├── overall_performance_dashboard.png
│   │   ├── Lab 1.jpeg
│   │   └── Lab 2.jpeg
│   └── script/                                # Reproducible automation scripts
│       ├── benchmark.sh                       # Automated sysbench test runner
│       ├── parse_sysbench.py                  # Telemetry parsing & diff matrix generator
│       └── generate_plots.py                  # Publication-grade chart generation
│
├── Lab-02-[Topic]/                            # (Future Labs will be cleanly added here)
│   ├── Lab Report.md
│   ├── script/
│   └── ...
```

---

## 🛠️ General Environment & Tooling

Common utilities, platforms, and toolchains utilized across the coursework:
- **Operating Systems**: Ubuntu Server 24.04 LTS, Windows 11
- **Virtualization & Clouds**: Proxmox Virtual Environment (Bare-metal KVM), VMware Workstation Pro
- **Benchmarking & Telemetry**: `sysbench`, `htop`, `lscpu`, `free`, `iproute2`
- **Scripting & Analytics**: Python 3.10+, Bash shell automation, Matplotlib & NumPy

---

## 👤 Author & Academic Details

- **Student Name**: Yash Raj
- **Subject**: Cloud Computing Laboratory
