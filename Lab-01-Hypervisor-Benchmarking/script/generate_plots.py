#!/usr/bin/env python3
"""
Visualization Generator for Virtualization Benchmarks
Creates publication-quality performance comparison plots between
Type-1 (Proxmox VE / KVM) and Type-2 (VMware Workstation) hypervisors.
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

# Styling and theme definitions
PALETTE = {
    "type1": "#3730a3",      # Deep Indigo / Navy
    "type2": "#ea580c",      # Vivid Orange / Amber
    "type1_light": "#e0e7ff",# Light Indigo
    "type2_light": "#ffedd5",# Light Amber
    "text": "#1e293b",       # Slate Dark
    "grid": "#e2e8f0",       # Light Grey
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
LABELS = ["Proxmox VE\n(Type-1 Bare-Metal)", "VMware Workstation\n(Type-2 Hosted)"]


def plot_throughput() -> None:
    """Generates Figure 1: Events Per Second Comparison."""
    eps_data = [1716.69, 1364.78]
    fig, ax = plt.subplots(figsize=(7.5, 5.5), dpi=DPI)

    bars = ax.bar(LABELS, eps_data, color=[PALETTE["type1"], PALETTE["type2"]], width=0.42, edgecolor="#0f172a", linewidth=1.1)
    ax.set_ylabel("Throughput (Events / Second)", fontsize=11, fontweight="bold", color=PALETTE["text"])
    ax.set_title("CPU Computational Throughput (Sysbench 20,000 Primes)", fontsize=13, fontweight="bold", pad=15)
    ax.set_ylim(0, 2150)
    ax.grid(axis="y")

    for bar in bars:
        h = bar.get_height()
        ax.annotate(
            f"{h:,.2f} EPS",
            xy=(bar.get_x() + bar.get_width() / 2, h),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontweight="bold",
            fontsize=10.5,
        )

    delta_pct = ((1716.69 - 1364.78) / 1364.78) * 100
    ax.text(
        0.5, 0.86,
        f"Bare-Metal Type-1 Speedup: +{delta_pct:.2f}%\n(+351.91 Events/sec)",
        transform=ax.transAxes,
        ha="center",
        fontsize=10.5,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.6", facecolor=PALETTE["type1_light"], edgecolor=PALETTE["type1"], alpha=0.9),
    )

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "events_per_second_comparison.png"))
    plt.close()


def plot_latency_metrics() -> None:
    """Generates Figure 2: Detailed Latency Profiles."""
    categories = ["Minimum Latency", "Average Latency", "95th Percentile", "Maximum Latency"]
    t1_lat = [0.57, 0.58, 0.65, 2.78]
    t2_lat = [0.67, 0.73, 0.89, 4.06]

    x = np.arange(len(categories))
    bar_width = 0.35

    fig, ax = plt.subplots(figsize=(9.5, 5.5), dpi=DPI)
    b1 = ax.bar(x - bar_width/2, t1_lat, bar_width, label="Proxmox VE (Type-1)", color=PALETTE["type1"], edgecolor="#0f172a")
    b2 = ax.bar(x + bar_width/2, t2_lat, bar_width, label="VMware Workstation (Type-2)", color=PALETTE["type2"], edgecolor="#0f172a")

    ax.set_ylabel("Execution Latency (Milliseconds - Lower is Better)", fontsize=11, fontweight="bold", color=PALETTE["text"])
    ax.set_title("Sysbench CPU Latency Metrics by Percentile", fontsize=13, fontweight="bold", pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=10.5, fontweight="bold")
    ax.set_ylim(0, 4.8)
    ax.legend(frameon=True, facecolor="white", edgecolor="#cbd5e1", fontsize=10)
    ax.grid(axis="y")

    for bar in b1:
        h = bar.get_height()
        ax.annotate(f"{h:.2f} ms", (bar.get_x() + bar.get_width()/2, h), xytext=(0, 4), textcoords="offset points", ha="center", fontsize=9, fontweight="bold", color=PALETTE["type1"])

    for bar in b2:
        h = bar.get_height()
        ax.annotate(f"{h:.2f} ms", (bar.get_x() + bar.get_width()/2, h), xytext=(0, 4), textcoords="offset points", ha="center", fontsize=9, fontweight="bold", color=PALETTE["type2"])

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "latency_comparison.png"))
    plt.close()


def plot_total_events() -> None:
    """Generates Figure 3: Total Completed Events."""
    events = [17169, 13650]
    fig, ax = plt.subplots(figsize=(7.5, 5.5), dpi=DPI)

    bars = ax.bar(LABELS, events, color=[PALETTE["type1"], PALETTE["type2"]], width=0.42, edgecolor="#0f172a", linewidth=1.1)
    ax.set_ylabel("Completed Event Volume (10-Second Window)", fontsize=11, fontweight="bold", color=PALETTE["text"])
    ax.set_title("Total Completed Computation Events", fontsize=13, fontweight="bold", pad=15)
    ax.set_ylim(0, 21500)
    ax.grid(axis="y")

    for bar in bars:
        h = bar.get_height()
        ax.annotate(
            f"{int(h):,} Events",
            xy=(bar.get_x() + bar.get_width() / 2, h),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontweight="bold",
            fontsize=10.5,
        )

    delta_events = 17169 - 13650
    ax.text(
        0.5, 0.86,
        f"+{delta_events:,} Additional Events Processed\n(+25.78% Greater Work Done)",
        transform=ax.transAxes,
        ha="center",
        fontsize=10.5,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.6", facecolor=PALETTE["type1_light"], edgecolor=PALETTE["type1"], alpha=0.9),
    )

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "total_events_comparison.png"))
    plt.close()


def plot_dashboard() -> None:
    """Generates Figure 4: Comprehensive Multi-Quadrant Dashboard."""
    fig, axes = plt.subplots(2, 2, figsize=(13, 9), dpi=DPI)
    fig.suptitle("Performance Telemetry Dashboard: Type-1 (Proxmox VE) vs Type-2 (VMware Workstation)", fontsize=15, fontweight="bold", y=0.98)

    # Subplot 1: Throughput
    b1 = axes[0, 0].bar(LABELS, [1716.69, 1364.78], color=[PALETTE["type1"], PALETTE["type2"]], width=0.4, edgecolor="#0f172a")
    axes[0, 0].set_title("Throughput: Events / Sec (Higher = Better)", fontweight="bold", fontsize=11)
    axes[0, 0].set_ylabel("Events / Sec")
    axes[0, 0].grid(axis="y")
    for bar in b1:
        axes[0, 0].annotate(f"{bar.get_height():,.2f}", (bar.get_x() + bar.get_width()/2, bar.get_height()), xytext=(0, 3), textcoords="offset points", ha="center", fontweight="bold")

    # Subplot 2: Total Events
    b2 = axes[0, 1].bar(LABELS, [17169, 13650], color=[PALETTE["type1"], PALETTE["type2"]], width=0.4, edgecolor="#0f172a")
    axes[0, 1].set_title("Total Event Count in 10s (Higher = Better)", fontweight="bold", fontsize=11)
    axes[0, 1].set_ylabel("Total Events")
    axes[0, 1].grid(axis="y")
    for bar in b2:
        axes[0, 1].annotate(f"{int(bar.get_height()):,}", (bar.get_x() + bar.get_width()/2, bar.get_height()), xytext=(0, 3), textcoords="offset points", ha="center", fontweight="bold")

    # Subplot 3: Mean Latency
    b3 = axes[1, 0].bar(LABELS, [0.58, 0.73], color=[PALETTE["type1"], PALETTE["type2"]], width=0.4, edgecolor="#0f172a")
    axes[1, 0].set_title("Mean Latency (Lower = Better)", fontweight="bold", fontsize=11)
    axes[1, 0].set_ylabel("Latency (ms)")
    axes[1, 0].set_ylim(0, 1.0)
    axes[1, 0].grid(axis="y")
    for bar in b3:
        axes[1, 0].annotate(f"{bar.get_height():.2f} ms", (bar.get_x() + bar.get_width()/2, bar.get_height()), xytext=(0, 3), textcoords="offset points", ha="center", fontweight="bold")

    # Subplot 4: 95th Percentile Latency
    b4 = axes[1, 1].bar(LABELS, [0.65, 0.89], color=[PALETTE["type1"], PALETTE["type2"]], width=0.4, edgecolor="#0f172a")
    axes[1, 1].set_title("95th Percentile Latency (Lower = Better)", fontweight="bold", fontsize=11)
    axes[1, 1].set_ylabel("Latency (ms)")
    axes[1, 1].set_ylim(0, 1.2)
    axes[1, 1].grid(axis="y")
    for bar in b4:
        axes[1, 1].annotate(f"{bar.get_height():.2f} ms", (bar.get_x() + bar.get_width()/2, bar.get_height()), xytext=(0, 3), textcoords="offset points", ha="center", fontweight="bold")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(OUTPUT_DIR, "overall_performance_dashboard.png"))
    plt.close()


def main() -> None:
    print("[*] Generating updated performance visualization plots...")
    plot_throughput()
    plot_latency_metrics()
    plot_total_events()
    plot_dashboard()
    print("[✔] Visualizations successfully generated in images/ directory.")


if __name__ == "__main__":
    main()
