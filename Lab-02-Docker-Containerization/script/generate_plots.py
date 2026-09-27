#!/usr/bin/env python3
"""
Visualization Generator for Containerization vs. Hardware Virtualization Benchmarks
Creates publication-quality comparative evaluation plots contrasting:
  - OS-Level Virtualization (Docker Containers)
  - Type-1 Bare-Metal Hypervisors (Proxmox VE / KVM)
  - Type-2 Hosted Hypervisors (VMware Workstation Pro)
"""

from __future__ import annotations
import os
import sys

try:
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    print("[!] matplotlib or numpy is not installed.")
    print("    Install dependencies via: pip install matplotlib numpy")
    sys.exit(0)

# Output directory configuration
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Styling and theme definitions matching Lab-01 design system
PALETTE = {
    "docker": "#0284c7",       # Vivid Sky Blue
    "docker_light": "#e0f2fe", # Light Sky Blue
    "type1": "#3730a3",        # Deep Indigo / Navy (Bare-Metal KVM)
    "type1_light": "#e0e7ff",  # Light Indigo
    "type2": "#ea580c",        # Vivid Orange / Amber (Hosted VMware)
    "type2_light": "#ffedd5",  # Light Amber
    "text": "#1e293b",         # Slate Dark
    "grid": "#e2e8f0",         # Light Grey
}

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 10,
    "axes.edgecolor": "#94a3b8",
    "axes.linewidth": 0.8,
    "grid.color": PALETTE["grid"],
    "grid.linestyle": "--",
    "grid.alpha": 0.7,
})

DPI = 300
ARCH_LABELS = [
    "Docker Container\n(OS-Level)",
    "Proxmox VE\n(Type-1 Bare-Metal)",
    "VMware Workstation\n(Type-2 Hosted)"
]
COLORS = [PALETTE["docker"], PALETTE["type1"], PALETTE["type2"]]


def plot_startup_time() -> None:
    """Generates Figure 1: Application Startup / Boot Latency Comparison."""
    startup_times = [0.8, 22.5, 42.0]
    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=DPI)

    bars = ax.bar(ARCH_LABELS, startup_times, color=COLORS, width=0.45, edgecolor="#0f172a", linewidth=1.1)
    ax.set_ylabel("Startup / Boot Latency (Seconds - Lower is Better)", fontsize=11, fontweight="bold", color=PALETTE["text"])
    ax.set_title("Cold Startup Latency: Docker Container vs Virtual Machines", fontsize=13, fontweight="bold", pad=15)
    ax.set_ylim(0, 50)
    ax.grid(axis="y")

    for bar in bars:
        h = bar.get_height()
        label = f"{h:.1f} s (<1s)" if h < 1 else f"{h:.1f} s"
        ax.annotate(
            label,
            xy=(bar.get_x() + bar.get_width() / 2, h),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontweight="bold",
            fontsize=10.5,
        )

    ax.text(
        0.5, 0.85,
        "Docker Container Initialization: ~52x Faster than Type-2\nand ~28x Faster than Type-1 VM",
        transform=ax.transAxes,
        ha="center",
        fontsize=10.5,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.6", facecolor=PALETTE["docker_light"], edgecolor=PALETTE["docker"], alpha=0.9),
    )

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "docker_vs_vm_startup_time.png"))
    plt.close()


def plot_memory_footprint() -> None:
    """Generates Figure 2: Memory Footprint Overhead Comparison."""
    ram_mb = [24.5, 2048.0, 2048.0]
    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=DPI)

    bars = ax.bar(ARCH_LABELS, ram_mb, color=COLORS, width=0.45, edgecolor="#0f172a", linewidth=1.1)
    ax.set_ylabel("RAM Consumption (Megabytes - Log Scale)", fontsize=11, fontweight="bold", color=PALETTE["text"])
    ax.set_title("Runtime Memory Footprint Comparison", fontsize=13, fontweight="bold", pad=15)
    ax.set_yscale("log")
    ax.set_ylim(1, 6000)
    ax.grid(axis="y", which="both")

    for bar in bars:
        h = bar.get_height()
        label = f"{h:.1f} MB" if h < 100 else f"{int(h)} MB (2.0 GB)"
        ax.annotate(
            label,
            xy=(bar.get_x() + bar.get_width() / 2, h),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontweight="bold",
            fontsize=10.5,
        )

    ax.text(
        0.5, 0.85,
        "Docker Memory Consumption: ~83x Smaller\n(Shared Host Kernel vs Dedicated Guest OS Reserve)",
        transform=ax.transAxes,
        ha="center",
        fontsize=10.5,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.6", facecolor=PALETTE["docker_light"], edgecolor=PALETTE["docker"], alpha=0.9),
    )

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "docker_vs_vm_memory_footprint.png"))
    plt.close()


def plot_disk_overhead() -> None:
    """Generates Figure 3: Image / Storage Footprint Comparison."""
    disk_mb = [145.0, 20480.0, 20480.0]
    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=DPI)

    bars = ax.bar(ARCH_LABELS, disk_mb, color=COLORS, width=0.45, edgecolor="#0f172a", linewidth=1.1)
    ax.set_ylabel("Storage Footprint (Megabytes - Log Scale)", fontsize=11, fontweight="bold", color=PALETTE["text"])
    ax.set_title("Storage Footprint: Container Image vs Virtual Disk Allocation", fontsize=13, fontweight="bold", pad=15)
    ax.set_yscale("log")
    ax.set_ylim(10, 60000)
    ax.grid(axis="y", which="both")

    for bar in bars:
        h = bar.get_height()
        label = f"{int(h)} MB" if h < 1000 else f"{int(h/1024)} GB ({int(h):,} MB)"
        ax.annotate(
            label,
            xy=(bar.get_x() + bar.get_width() / 2, h),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontweight="bold",
            fontsize=10.5,
        )

    ax.text(
        0.5, 0.85,
        "Storage Density: ~141x Smaller Footprint\n(Thin Multi-Layer Image vs Full VHD Virtual Disk)",
        transform=ax.transAxes,
        ha="center",
        fontsize=10.5,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.6", facecolor=PALETTE["docker_light"], edgecolor=PALETTE["docker"], alpha=0.9),
    )

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "docker_vs_vm_disk_overhead.png"))
    plt.close()


def plot_dashboard() -> None:
    """Generates Figure 4: Comprehensive 4-Quadrant Containerization Dashboard."""
    fig, axes = plt.subplots(2, 2, figsize=(13.5, 9.5), dpi=DPI)
    fig.suptitle("Containerization vs. Virtualization Telemetry Dashboard", fontsize=15, fontweight="bold", y=0.98)

    # Subplot 1: Startup Latency
    b1 = axes[0, 0].bar(ARCH_LABELS, [0.8, 22.5, 42.0], color=COLORS, width=0.4, edgecolor="#0f172a")
    axes[0, 0].set_title("Cold Startup Latency (Lower = Better)", fontweight="bold", fontsize=11)
    axes[0, 0].set_ylabel("Seconds (s)")
    axes[0, 0].set_ylim(0, 50)
    axes[0, 0].grid(axis="y")
    for bar in b1:
        h = bar.get_height()
        lbl = f"{h:.1f} s" if h >= 1 else f"{h:.1f} s"
        axes[0, 0].annotate(lbl, (bar.get_x() + bar.get_width()/2, h), xytext=(0, 3), textcoords="offset points", ha="center", fontweight="bold")

    # Subplot 2: Memory Footprint (Log scale)
    b2 = axes[0, 1].bar(ARCH_LABELS, [24.5, 2048.0, 2048.0], color=COLORS, width=0.4, edgecolor="#0f172a")
    axes[0, 1].set_title("Baseline Memory Footprint (Lower = Better)", fontweight="bold", fontsize=11)
    axes[0, 1].set_ylabel("RAM (MB - Log Scale)")
    axes[0, 1].set_yscale("log")
    axes[0, 1].set_ylim(1, 6000)
    axes[0, 1].grid(axis="y", which="both")
    for bar in b2:
        h = bar.get_height()
        lbl = f"{h:.1f} MB" if h < 100 else f"{int(h)} MB"
        axes[0, 1].annotate(lbl, (bar.get_x() + bar.get_width()/2, h), xytext=(0, 3), textcoords="offset points", ha="center", fontweight="bold")

    # Subplot 3: Disk Footprint (Log scale)
    b3 = axes[1, 0].bar(ARCH_LABELS, [145.0, 20480.0, 20480.0], color=COLORS, width=0.4, edgecolor="#0f172a")
    axes[1, 0].set_title("Storage Footprint (Lower = Better)", fontweight="bold", fontsize=11)
    axes[1, 0].set_ylabel("Disk Size (MB - Log Scale)")
    axes[1, 0].set_yscale("log")
    axes[1, 0].set_ylim(10, 60000)
    axes[1, 0].grid(axis="y", which="both")
    for bar in b3:
        h = bar.get_height()
        lbl = f"{int(h)} MB" if h < 1000 else f"{int(h/1024)} GB"
        axes[1, 0].annotate(lbl, (bar.get_x() + bar.get_width()/2, h), xytext=(0, 3), textcoords="offset points", ha="center", fontweight="bold")

    # Subplot 4: CPU Virtualization Overhead %
    overheads = [0.5, 5.2, 14.8]
    b4 = axes[1, 1].bar(ARCH_LABELS, overheads, color=COLORS, width=0.4, edgecolor="#0f172a")
    axes[1, 1].set_title("CPU Virtualization Overhead (Lower = Better)", fontweight="bold", fontsize=11)
    axes[1, 1].set_ylabel("CPU Overhead Ratio (%)")
    axes[1, 1].set_ylim(0, 18)
    axes[1, 1].grid(axis="y")
    for bar in b4:
        axes[1, 1].annotate(f"{bar.get_height():.1f}%", (bar.get_x() + bar.get_width()/2, bar.get_height()), xytext=(0, 3), textcoords="offset points", ha="center", fontweight="bold")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(OUTPUT_DIR, "containerization_performance_dashboard.png"))
    plt.close()


def main() -> None:
    print("[*] Generating containerization performance visualization plots...")
    plot_startup_time()
    plot_memory_footprint()
    plot_disk_overhead()
    plot_dashboard()
    print("[OK] All figures successfully generated in images/ directory.")


if __name__ == "__main__":
    main()
