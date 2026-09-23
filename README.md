# Hypervisor Computational Performance Benchmarking
### Empirical Evaluation of Type-1 (Bare-Metal KVM) vs. Type-2 (Hosted VMware) Virtualization

![Virtualization Paradigm](https://img.shields.io/badge/Virtualization-Type--1_vs_Type--2-blue)
![Benchmark Tool](https://img.shields.io/badge/Workload-Sysbench_CPU-green)
![Guest OS](https://img.shields.io/badge/Guest_OS-Ubuntu_24.04_LTS-orange)
![Analysis](https://img.shields.io/badge/Status-Complete-brightgreen)

---

## 📌 Executive Summary

Virtual machine monitor (VMM) placement within the system hierarchy dictates the latency, throughput, and overhead of virtualized compute instances. This repository documents a controlled performance evaluation comparing:

- **Type-1 (Bare-Metal) Architecture:** Proxmox VE utilizing Kernel-based Virtual Machine (`KVM`)
- **Type-2 (Hosted) Architecture:** VMware Workstation Pro operating atop a Windows 11 host operating system

Both hypervisors were provisioned with identically configured guest environments (**Ubuntu Server 24.04 LTS, 2 vCPUs, 2 GB RAM, 20 GB Disk**). A deterministic integer-heavy workload—calculating prime numbers up to 20,000 using `sysbench`—was deployed across both systems to quantitatively analyze throughput, latency variance, and virtualization penalties.

---

## 🏛️ Architectural Context

The core structural difference between the two environments is the presence or absence of an intermediary general-purpose host OS:

```text
┌─────────────────────────────────────────────────────────────┐
│                    ARCHITECTURAL COMPARISON                 │
├──────────────────────────────┬──────────────────────────────┤
│    TYPE-1: PROXMOX VE (KVM)  │ TYPE-2: VMWARE WORKSTATION   │
├──────────────────────────────┼──────────────────────────────┤
│  [ Guest Ubuntu VM ]         │  [ Guest Ubuntu VM ]         │
│         │                    │         │                    │
│         ▼                    │         ▼                    │
│  [ Proxmox VE / KVM ]        │  [ VMware Workstation VMM ]  │
│  (Bare-Metal Hypervisor)     │  (Application Software)      │
│         │                    │         │                    │
│         │                    │         ▼                    │
│         │                    │  [ Windows 11 Host OS ]      │
│         │                    │  (NT Kernel & Scheduler)     │
│         ▼                    │         │                    │
│  [ Physical Hardware ]       │         ▼                    │
│  (CPU / RAM / I/O)           │  [ Physical Hardware ]       │
└──────────────────────────────┴──────────────────────────────┘
```

- **Type-1 (Proxmox VE):** Guest processes execute directly via hardware virtualization extensions (Intel VT-x / AMD-V) in coordination with the Linux kernel scheduler.
- **Type-2 (VMware Workstation):** Execution involves a layered traversal through the VMware runtime application and the underlying Windows NT thread dispatcher before dispatching to physical hardware.

---

## ⚙️ Standardized Environment Specifications

To eliminate skew and ensure reproducible benchmarking, the virtual hardware profiles were strictly aligned:

| Property | Bare-Metal Node (Type-1) | Hosted Instance (Type-2) | Validation State |
| :--- | :--- | :--- | :--- |
| **Hypervisor Software** | Proxmox VE 8.x (Linux KVM) | VMware Workstation Pro 17.x | Validated |
| **Host OS** | None (Direct Bare-Metal) | Windows 11 64-bit | Validated |
| **Guest OS Distribution** | Ubuntu 24.04 LTS AMD64 | Ubuntu 24.04 LTS AMD64 | Identical Kernel |
| **Virtual CPUs** | 2 vCPUs (1 socket, 2 cores) | 2 vCPUs (1 socket, 2 cores) | Parity Enforced |
| **Virtual Memory** | 2048 MB (2.0 GiB) | 2048 MB (2.0 GiB) | Parity Enforced |
| **Virtual Storage** | 20 GB SCSI/VirtIO | 20 GB Virtual SCSI Disk | Parity Enforced |
| **Network Device** | VirtIO Bridge | NAT Virtual Adapter | Standardized |

---

## 📊 Empirical Benchmark Results

### Performance Summary Table

| Metric | Proxmox VE (Type-1) | VMware Workstation (Type-2) | Difference ($\Delta$) | Impact Analysis |
| :--- | :---: | :---: | :---: | :--- |
| **Throughput (Events/sec)** | **1,716.69** | **1,364.78** | **+351.91 EPS** | **+25.78% higher throughput** |
| **Total Events (10s Window)**| **17,169** | **13,650** | **+3,519 events** | **+25.78% total work completed** |
| **Total Test Duration** | 10.0004 s | 10.0007 s | -0.0003 s | Nominal variance (<0.01%) |
| **Minimum Latency** | **0.57 ms** | **0.67 ms** | **-0.10 ms** | **14.93% faster best-case** |
| **Average Latency** | **0.58 ms** | **0.73 ms** | **-0.15 ms** | **20.55% lower mean latency** |
| **95th Percentile Latency** | **0.65 ms** | **0.89 ms** | **-0.24 ms** | **26.97% tighter tail-latency** |
| **Maximum Latency** | **2.78 ms** | **4.06 ms** | **-1.28 ms** | **31.53% reduction in max spike** |

### Key Formula
Throughput advantage was quantified using:
$$\text{Speedup (\%)} = \frac{\text{EPS}_{\text{Proxmox}} - \text{EPS}_{\text{VMware}}}{\text{EPS}_{\text{VMware}}} \times 100 = \frac{1716.69 - 1364.78}{1364.78} \times 100 = 25.78\%$$

---

## 📈 Visual Telemetry & Analysis

Visual plots generated from the benchmark telemetry are located under the [`images/`](images/) directory:

| Visualization | Description | Preview |
| :--- | :--- | :--- |
| **Throughput (EPS)** | Demonstrates the +25.78% sustained throughput gain on Type-1. | [View Plot](images/events_per_second_comparison.png) |
| **Latency Distribution** | Compares Minimum, Mean, 95th Percentile, and Maximum latency metrics. | [View Plot](images/latency_comparison.png) |
| **Total Processed Events** | Highlights the absolute event processing volume delta over 10 seconds. | [View Plot](images/total_events_comparison.png) |
| **Performance Dashboard** | Consolidated 4-quadrant telemetry dashboard. | [View Dashboard](images/overall_performance_dashboard.png) |

---

## 🔬 Architectural Diagnostics: Why Do The Results Diverge?

The empirical throughput and latency differences stem from three primary architectural factors:

1. **Host Scheduler Interleaving (Double-Scheduling Penalty):**
   Under Type-2 virtualization, the guest operating system's CPU scheduler runs within a thread pool scheduled by the Windows host kernel. Windows background threads, audio/graphics drivers, and interactive user applications routinely interrupt and deschedule the VM process. Type-1 hypervisors execute the guest directly via the native hypervisor scheduler with dedicated core binding.

2. **VM-Exit and Mode-Switching Cost:**
   Privileged instructions that trigger a VM-Exit in Type-1 are resolved directly in hypervisor mode (Ring 0 / VMX Root). On Type-2, an exit requires passing the trap through the host application layer down to the host OS kernel and back, significantly amplifying latency penalties.

3. **Memory Bus and Cache Contention:**
   The host OS on a Type-2 setup continually executes background tasks, degrading CPU L1/L2/L3 cache residency and inducing Translation Lookaside Buffer (TLB) evictions. In Type-1, memory management via Extended Page Tables (EPT) operates with minimal cache thrashing.

---

## 📂 Repository Structure

```text
cloud-computing-/
├── Lab Report.md                  # Comprehensive academic laboratory write-up
├── README.md                      # Project documentation and performance synthesis
│
├── images/                        # Performance plots and raw benchmark screenshots
│   ├── Lab 1.jpeg                 # Telemetry proof / terminal screenshot (Node 1)
│   ├── Lab 2.jpeg                 # Telemetry proof / terminal screenshot (Node 2)
│   ├── events_per_second_comparison.png
│   ├── latency_comparison.png
│   ├── total_events_comparison.png
│   └── overall_performance_dashboard.png
│
└── script/                        # Automation, ingestion, and visualization scripts
    ├── benchmark.sh               # Shell script to automate sysbench runs & hardware audit
    ├── parse_sysbench.py          # Python analytical script to calculate deltas & metrics
    └── generate_plots.py          # Matplotlib script to generate publication-grade charts
```

---

## 🛠️ Step-by-Step Reproduction Guide

### 1. Execute Benchmark Inside Guest VM
Log into the Ubuntu virtual machine and execute the following commands:
```bash
# Update repositories and install benchmark utility
sudo apt update && sudo apt install -y sysbench

# Run deterministic CPU prime computation test
sysbench cpu --cpu-max-prime=20000 --threads=1 run
```
*Alternatively, transfer and execute the automated script:*
```bash
chmod +x script/benchmark.sh
./script/benchmark.sh
```

### 2. Parse & Compare Performance Metrics
Analyze output differences locally using the Python parsing script:
```bash
python script/parse_sysbench.py
```

### 3. Generate Graphical Figures
To recreate all analytical figures:
```bash
python script/generate_plots.py
```

---

## 🏁 Conclusions & Best Practices

- **Production Clouds & Datacenters:** Always deploy **Type-1 hypervisors** (Proxmox VE, KVM, ESXi) for server infrastructure, database engines, and performance-critical microservices where latency variance and throughput loss are unacceptable.
- **Local Development & Testing:** **Type-2 hypervisors** (VMware Workstation, VirtualBox) provide convenient sandboxing and quick evaluation environments for developers, despite the ~20–30% compute overhead.
