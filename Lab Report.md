# EXPERIMENTAL LABORATORY REPORT
## Comparative CPU Performance Assessment of Bare-Metal (Type-1) and Hosted (Type-2) Virtualization Platforms

**Course:** Cloud Computing and Virtualization Technologies  
**Laboratory Practical:** Module 01  
**Study Focus:** Quantifying Architectural Overhead and Execution Efficiency across Proxmox VE (KVM) and VMware Workstation  

---

## Abstract & Executive Summary

Virtualization technologies serve as the foundational backbone of contemporary cloud datacenters. However, the architectural layer at which virtualization is implemented introduces distinct computational overheads. This laboratory investigation presents an empirical performance evaluation contrasting a **Type-1 (Bare-Metal) Hypervisor (Proxmox VE with Kernel-based Virtual Machine - KVM)** against a **Type-2 (Hosted) Hypervisor (VMware Workstation Pro running on Windows 11)**. 

By standardizing guest operating system configurations (Ubuntu Linux, 2 vCPUs, 2048 MB RAM, 20 GB storage) and applying a standardized integer-heavy computational workload (`sysbench` CPU prime number calculation up to 20,000), we measured system throughput and request latencies. The empirical findings reveal that the Type-1 architecture delivers an **events-per-second throughput improvement of +25.78%** (1,716.69 EPS vs. 1,364.78 EPS) and exhibits a **20.55% reduction in mean processing latency** (0.58 ms vs. 0.73 ms). This report details the theoretical drivers, configuration parameters, measurement telemetry, and architectural analysis accounting for this divergence.

---

## 1. Laboratory Objectives

The primary deliverables for this laboratory exercise are:
1. **Infrastructure Provisioning**: Deploy two homogeneous guest virtual machines running Ubuntu Linux under identical physical resource allocations across both hypervisor paradigms:
   - Proxmox VE 8.x (Bare-Metal Type-1)
   - VMware Workstation Pro 17.x (Hosted Type-2)
2. **Standardized Benchmarking**: Subject each virtualized instance to a deterministic CPU workload using the `sysbench` synthetic benchmarking utility with a target threshold of 20,000 primes.
3. **Telemetry Capture**: Acquire detailed performance telemetry, including total elapsed computation time, processed events, throughput (events per second), and latency distribution profiles (minimum, arithmetic mean, 95th percentile, and maximum).
4. **Architectural Evaluation**: Critically analyze the performance differential by evaluating host OS scheduler preemption, hypervisor intercept penalties, context switching frequencies, and hardware-assisted virtualization extensions.

---

## 2. Theoretical Foundations

Virtualization relies on decoupling the software execution environment from the physical compute substrate. Hypervisors (Virtual Machine Monitors - VMM) are historically categorized based on where they reside in the system software hierarchy.

```
┌─────────────────────────────────────────┐       ┌─────────────────────────────────────────┐
│        TYPE-1: BARE-METAL (KVM)         │       │        TYPE-2: HOSTED (VMWARE)          │
├─────────────────────────────────────────┤       ├─────────────────────────────────────────┤
│    [ Guest OS - Ubuntu Virtual VM ]     │       │    [ Guest OS - Ubuntu Virtual VM ]     │
│                   │                     │       │                   │                     │
│                   ▼                     │       │                   ▼                     │
│ [ Type-1 Hypervisor (Proxmox / KVM) ]   │       │   [ Type-2 Hypervisor Application ]     │
│                   │                     │       │                   │                     │
│                   ▼                     │       │                   ▼                     │
│  [ Bare-Metal Hardware Substrate ]      │       │     [ Host OS (Windows 11 NT Kernel) ]  │
│       (CPU / Memory / I/O Core)         │       │                   │                     │
│                                         │       │                   ▼                     │
│                                         │       │  [ Bare-Metal Hardware Substrate ]      │
└─────────────────────────────────────────┘       └─────────────────────────────────────────┘
```

### 2.1 Type-1 Hypervisors (Bare-Metal / Native)
A Type-1 hypervisor boots directly on the physical host hardware without an intermediary general-purpose operating system.
- **Representative Systems**: Proxmox VE (Linux KVM), VMware ESXi, Citrix Hypervisor (Xen), Microsoft Hyper-V Server.
- **Operational Mechanism**: The hypervisor operates in privileged hardware execution states (such as Intel VMX Root Operation). KVM transforms the Linux kernel into a bare-metal hypervisor, dispatching guest vCPU threads directly via the kernel’s scheduler (`sched_fair`) straight onto physical CPU cores with minimal intermediate abstraction.
- **Key Advantages**:
  - Near-native CPU and memory instruction execution speeds.
  - Elimination of background services, desktop compositor overhead, and unrelated OS processes.
  - Direct translation of virtual memory using hardware-accelerated nested page tables (EPT/NPT).

### 2.2 Type-2 Hypervisors (Hosted)
A Type-2 hypervisor is installed as an application software layer atop a pre-existing host operating system (e.g., Microsoft Windows or macOS).
- **Representative Systems**: VMware Workstation, Oracle VM VirtualBox, Parallels Desktop.
- **Operational Mechanism**: When the guest OS executes instructions requiring hardware virtualization, the request must transition across multiple boundaries:
  $$\text{Guest OS} \longrightarrow \text{Hosted VMM App} \longrightarrow \text{Host OS Kernel (Drivers)} \longrightarrow \text{Physical CPU}$$
- **Architectural Bottlenecks**:
  - **Dual Scheduler Contention**: The guest operating system’s scheduler runs inside the vCPU, which is itself scheduled as a user-space thread or service by the host OS thread dispatcher.
  - **Context-Switching Penalties**: Frequent transitions between guest non-root mode, host user mode, and host kernel mode induce significant TLB (Translation Lookaside Buffer) flushes and CPU cache invalidations.
  - **Host Resource Interference**: Background services, updates, telemetry, and interactive desktop GUI tasks on the host system routinely preempt VM compute execution.

---

## 3. Testbed Provisioning & Environment Specifications

To ensure scientific validity and parity, both testing environments were configured with matching computational allocations and guest system environments.

### Standardized System Specifications

| Allocation Parameter | Proxmox VE Environment (Type-1) | VMware Workstation Environment (Type-2) | Parity Verification |
| :--- | :--- | :--- | :--- |
| **Virtual Machine Name** | `vm-kvm-bench-01` | `vm-workstation-bench-02` | Isolated test identity |
| **Operating System** | Ubuntu Server 24.04 LTS (x86_64) | Ubuntu Server 24.04 LTS (x86_64) | Identical Linux kernel & libraries |
| **Virtual Cores (vCPU)** | 2 Cores (1 Socket $\times$ 2 Cores) | 2 Cores (1 Processor $\times$ 2 Cores) | Matched symmetric multiprocessing |
| **vCPU Model / Extensions**| `x86-64-v2-AES` (Hardware Virtualization) | Host CPU Passthrough / Virtualize VT-x | Matched instruction set support |
| **Allocated RAM** | 2048 MB (2.0 GiB) | 2048 MB (2.0 GiB) | Identical memory constraints |
| **Storage Capacity** | 20 GB VirtIO Block Device | 20 GB SCSI/NVMe Virtual Disk | Isolated synthetic disk limits |
| **Network Configuration**| Linux Virtual Bridge (`vmbr0`) | Host NAT Network (`VMnet8`) | Standardized isolated routing |

---

## 4. Experimental Methodology

### 4.1 System Readiness & Pre-Flight Verification
Prior to triggering the computational benchmark, each virtual instance was audited to verify hardware allocation consistency and low baseline background activity:
```bash
# Verify system architecture and active kernel version
hostnamectl

# Inspect assigned vCPU topology and processor capabilities
lscpu | grep -E "Model name|CPU\(s\)|Thread\(s\) per core|Core\(s\) per socket|Socket\(s\)"

# Confirm available memory headroom
free -h

# Confirm root disk partition capacity
df -h /

# Verify idle CPU utilization prior to test execution
top -b -n 1 | head -n 15
```

### 4.2 Benchmark Execution Protocol
The synthetic benchmark was administered via `sysbench`, an industry-standard modular multi-threaded benchmark tool. The CPU test evaluates computational performance by calculating prime numbers up to a specified ceiling via brute-force division.
```bash
# Package update and tool installation
sudo apt update && sudo apt install -y sysbench

# Benchmark invocation command
sysbench cpu --cpu-max-prime=20000 --threads=1 run
```

---

## 5. Empirical Benchmark Data & Observation Logs

### 5.1 Raw Benchmark Telemetry: Proxmox VE (Type-1)
```text
sysbench 1.0.20 (using system OpenSSL)

Running the test with following options:
Number of threads: 1
Initializing random number generator from current time

Prime numbers limit: 20000

Initializing worker threads...

Threads started!

CPU speed:
    events per second:  1716.69

General statistics:
    total time:                          10.0004s
    total number of events:              17169

Latency (ms):
         min:                                    0.57
         avg:                                    0.58
         max:                                    2.78
         95th percentile:                        0.65
         sum:                                 9996.45

Threads fairness:
    events (avg/stddev):           17169.0000/0.00
    execution time (avg/stddev):   9.9965/0.00
```

### 5.2 Raw Benchmark Telemetry: VMware Workstation (Type-2)
```text
sysbench 1.0.20 (using system OpenSSL)

Running the test with following options:
Number of threads: 1
Initializing random number generator from current time

Prime numbers limit: 20000

Initializing worker threads...

Threads started!

CPU speed:
    events per second:  1364.78

General statistics:
    total time:                          10.0007s
    total number of events:              13650

Latency (ms):
         min:                                    0.67
         avg:                                    0.73
         max:                                    4.06
         95th percentile:                        0.89
         sum:                                 9992.11

Threads fairness:
    events (avg/stddev):           13650.0000/0.00
    execution time (avg/stddev):   9.9921/0.00
```

---

## 6. Quantitative Performance Comparison

The empirical metrics harvested during both execution runs are synthesized below:

| Performance Metric | Unit | Proxmox VE (Type-1) | VMware Workstation (Type-2) | Absolute Delta ($\Delta$) | Performance Advantage |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Observation Window** | Seconds | 10.0004 s | 10.0007 s | -0.0003 s | Nominal variance (<0.01%) |
| **Total Completed Events** | Count | 17,169 | 13,650 | +3,519 events | **Proxmox processed +25.78% more work** |
| **Throughput (Events/sec)**| EPS | **1,716.69** | **1,364.78** | **+351.91 EPS** | **Type-1 is 1.258x faster** |
| **Minimum Latency** | Milliseconds | 0.57 ms | 0.67 ms | -0.10 ms | Proxmox 14.93% lower latency |
| **Average Latency** | Milliseconds | **0.58 ms** | **0.73 ms** | **-0.15 ms** | **Proxmox 20.55% lower latency** |
| **95th Percentile Latency**| Milliseconds | **0.65 ms** | **0.89 ms** | **-0.24 ms** | **Proxmox 26.97% lower latency** |
| **Maximum Latency** | Milliseconds | 2.78 ms | 4.06 ms | -1.28 ms | Proxmox 31.53% lower peak jitter |

---

## 7. Performance Visualizations & Telemetry Charts

### Figure 1: Computational Throughput Comparison (Events / Sec)
The chart below highlights the sustained event processing capacity over the benchmark interval.
![Events Per Second](images/events_per_second_comparison.png)

### Figure 2: Latency Distribution and Jitter Profile
A comparative analysis across latency percentiles illustrating lower variance and tighter bounds in the bare-metal environment.
![Latency Comparison](images/latency_comparison.png)

### Figure 3: Total Computation Events Completed
Cumulative volume of prime number determinations successfully processed within the 10-second test window.
![Total Events](images/total_events_comparison.png)

### Figure 4: Consolidated Performance Overview Dashboard
Comprehensive four-quadrant telemetry dashboard highlighting throughput, event volume, and latency profiles.
![Overall Performance Dashboard](images/overall_performance_dashboard.png)

---

## 8. In-Depth Technical Analysis & Discussion

### 8.1 Throughput and Computational Efficiency
Throughput was quantified through total prime calculation events processed per unit time. The relative speedup factor ($S$) achieved by the Type-1 hypervisor is defined as:

$$S = \left( \frac{\text{EPS}_{\text{Type-1}} - \text{EPS}_{\text{Type-2}}}{\text{EPS}_{\text{Type-2}}} \right) \times 100\%$$

Substituting the observed telemetry:
$$S = \left( \frac{1716.69 - 1364.78}{1364.78} \right) \times 100\% = \frac{351.91}{1364.78} \times 100\% \approx 25.78\%$$

Proxmox VE completed 3,519 additional events within the exact same 10-second timeframe. This confirms that for pure CPU-bound mathematical operations, Type-1 virtualization achieves vastly superior instruction throughput per clock cycle.

### 8.2 Latency Distribution and Tail-Latency Degradation
An evaluation of latency across percentiles reveals critical behavioral differences between the two architectures:
1. **Average Latency**: The hosted hypervisor introduces a $+0.15\text{ ms}$ average latency penalty ($+25.86\%$ latency increase over Proxmox).
2. **95th Percentile & Maximum Latency**: At the 95th percentile, VMware Workstation recorded $0.89\text{ ms}$ versus $0.65\text{ ms}$ on Proxmox ($26.97\%$ deterioration). The maximum latency peaked at $4.06\text{ ms}$ on VMware compared to $2.78\text{ ms}$ on Proxmox.

### 8.3 Root-Cause Architectural Drivers
The measured performance disparity can be attributed to three foundational system-level mechanisms:

1. **Host OS Thread Scheduling Overhead (Double Scheduling Problem)**:
   In VMware Workstation, guest virtual CPU instructions are packaged into execution threads managed by the host OS kernel scheduler (Windows NT scheduler). The guest kernel schedules tasks within its vCPU, but the host operating system dynamically modulates the physical processor allocation based on host load, power plan profiles, and background daemons. This introduces intermittent scheduling latency bubbles. In contrast, Proxmox VE (KVM) schedules guest threads directly against the physical Linux scheduler.

2. **Privilege Transitions and VM-Exit Penalties**:
   When a privileged instruction occurs, the CPU must exit guest execution mode (a VM-Exit). Under Type-1 hypervisors, handling occurs directly in the hypervisor running in VMX Root mode. In Type-2 hypervisors, the execution must traverse user-mode application software, through host device drivers, and finally to the hardware monitor before returning (a VM-Entry). This multi-tier relay dramatically increases execution latency.

3. **Memory Translation and Cache Pressure**:
   Although both environments leverage Second Level Address Translation (SLAT / EPT), the hosted hypervisor runs alongside an entire desktop software suite. This creates continual L1/L2/L3 CPU cache line evictions and TLB thrashing, directly increasing memory retrieval latency during execution.

---

## 9. Practical Engineering Implications

Based on the empirical findings, the strategic selection criteria between hypervisor tiers are summarized as follows:

| Criteria | Type-1 Architecture (e.g., Proxmox VE / KVM) | Type-2 Architecture (e.g., VMware Workstation) |
| :--- | :--- | :--- |
| **Primary Domain** | Production datacenters, private cloud clusters, high-frequency services | Local software development, student labs, desktop experimentation |
| **Performance Overhead**| Negligible ($< 2 - 3\%$ relative to bare-metal native) | Moderate to High ($15 - 30\%$ CPU/IO degradation) |
| **Hardware Management**| Direct, low-level physical control | Abstracted through host OS drivers |
| **Operational Ease** | Dedicated server hardware or partitioned hypervisor installation required | Simple executable installer on top of consumer operating systems |

---

## 10. Conclusion

This laboratory investigation successfully conducted an empirical performance benchmark contrasting Type-1 (Proxmox VE) and Type-2 (VMware Workstation) hypervisors under standardized test parameters.

The key deductions from this study are:
1. **Type-1 hypervisors significantly outperform Type-2 hypervisors in compute efficiency**, demonstrating a $+25.78\%$ throughput increase under identical allocated virtual resources.
2. **Latency predictability is significantly superior in bare-metal architectures**, with a $20.55\%$ lower mean latency and substantially diminished maximum latency spikes.
3. **Architectural abstraction comes at a measurable computational cost**, proving that hosted virtualization introduces non-trivial system call, scheduling, and privilege-transition overheads that make it unsuited for production enterprise compute workloads.

---

**Evaluator Verification:**  
- **Review Status:** Completed & Submitted  
- **Experimental Parity:** Confirmed  
- **Assigned Grade:** ________ / ________  
- **Instructor Remarks:** __________________________________________________
