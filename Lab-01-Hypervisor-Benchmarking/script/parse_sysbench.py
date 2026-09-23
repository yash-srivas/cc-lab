#!/usr/bin/env python3
"""
Performance Telemetry Parser & Comparative Analysis Engine
Evaluates CPU execution efficiency between Type-1 (Proxmox VE / KVM) 
and Type-2 (VMware Workstation) hypervisor benchmarks.
"""

from __future__ import annotations
import sys
import re
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class SysbenchTelemetry:
    hypervisor_name: str
    architecture_type: str
    events_per_sec: float
    total_time: float
    total_events: int
    min_latency: float
    avg_latency: float
    p95_latency: float
    max_latency: float


# Default empirical dataset collected during laboratory execution
EMPIRICAL_RUNS: Dict[str, SysbenchTelemetry] = {
    "type1": SysbenchTelemetry(
        hypervisor_name="Proxmox VE (KVM)",
        architecture_type="Type-1 Bare-Metal",
        events_per_sec=1716.69,
        total_time=10.0004,
        total_events=17169,
        min_latency=0.57,
        avg_latency=0.58,
        p95_latency=0.65,
        max_latency=2.78,
    ),
    "type2": SysbenchTelemetry(
        hypervisor_name="VMware Workstation",
        architecture_type="Type-2 Hosted",
        events_per_sec=1364.78,
        total_time=10.0007,
        total_events=13650,
        min_latency=0.67,
        avg_latency=0.73,
        p95_latency=0.89,
        max_latency=4.06,
    ),
}


def parse_log_content(text: str, name: str, arch_type: str) -> SysbenchTelemetry:
    """Extracts benchmark metrics from raw sysbench command output."""
    def extract_float(pattern: str, default: float = 0.0) -> float:
        match = re.search(pattern, text)
        return float(match.group(1)) if match else default

    def extract_int(pattern: str, default: int = 0) -> int:
        match = re.search(pattern, text)
        return int(match.group(1)) if match else default

    eps = extract_float(r"events per second:\s+([0-9.]+)")
    total_time = extract_float(r"total time:\s+([0-9.]+)s?")
    total_events = extract_int(r"total number of events:\s+([0-9]+)")
    min_lat = extract_float(r"min:\s+([0-9.]+)")
    avg_lat = extract_float(r"avg:\s+([0-9.]+)")
    max_lat = extract_float(r"max:\s+([0-9.]+)")
    p95_lat = extract_float(r"95th percentile:\s+([0-9.]+)")

    return SysbenchTelemetry(
        hypervisor_name=name,
        architecture_type=arch_type,
        events_per_sec=eps,
        total_time=total_time,
        total_events=total_events,
        min_latency=min_lat,
        avg_latency=avg_lat,
        p95_latency=p95_lat,
        max_latency=max_lat,
    )


def compute_performance_matrix(type1: SysbenchTelemetry, type2: SysbenchTelemetry) -> None:
    """Computes statistical differentials and displays a formatted comparative matrix."""
    throughput_gain = ((type1.events_per_sec - type2.events_per_sec) / type2.events_per_sec) * 100
    events_delta = type1.total_events - type2.total_events
    avg_latency_reduction = ((type2.avg_latency - type1.avg_latency) / type2.avg_latency) * 100
    p95_latency_reduction = ((type2.p95_latency - type1.p95_latency) / type2.p95_latency) * 100
    max_latency_delta = type2.max_latency - type1.max_latency

    header_border = "=" * 90
    sub_border = "-" * 90

    print(header_border)
    print("      VIRTUALIZATION ARCHITECTURAL PERFORMANCE BENCHMARK MATRIX")
    print("      Type-1 Bare-Metal (KVM) vs. Type-2 Hosted (VMware Workstation)")
    print(header_border)
    print(f"{'Performance Metric':<30} {'Type-1 (Proxmox)':<20} {'Type-2 (VMware)':<20} {'Observed Delta / Advantage'}")
    print(sub_border)

    rows = [
        ("Throughput (Events/sec)", f"{type1.events_per_sec:,.2f} EPS", f"{type2.events_per_sec:,.2f} EPS", f"+{throughput_gain:.2f}% (Type-1 speedup)"),
        ("Total Completed Events", f"{type1.total_events:,}", f"{type2.total_events:,}", f"+{events_delta:,} events (+{throughput_gain:.2f}%)"),
        ("Total Evaluation Time", f"{type1.total_time:.4f} s", f"{type2.total_time:.4f} s", f"{type1.total_time - type2.total_time:+.4f} s"),
        ("Minimum Latency", f"{type1.min_latency:.2f} ms", f"{type2.min_latency:.2f} ms", f"-{type2.min_latency - type1.min_latency:.2f} ms ({((type2.min_latency - type1.min_latency)/type2.min_latency)*100:.2f}% faster)"),
        ("Average (Mean) Latency", f"{type1.avg_latency:.2f} ms", f"{type2.avg_latency:.2f} ms", f"-{type2.avg_latency - type1.avg_latency:.2f} ms ({avg_latency_reduction:.2f}% lower)"),
        ("95th Percentile Latency", f"{type1.p95_latency:.2f} ms", f"{type2.p95_latency:.2f} ms", f"-{type2.p95_latency - type1.p95_latency:.2f} ms ({p95_latency_reduction:.2f}% lower)"),
        ("Maximum Latency (Jitter)", f"{type1.max_latency:.2f} ms", f"{type2.max_latency:.2f} ms", f"-{max_latency_delta:.2f} ms ({((type2.max_latency - type1.max_latency)/type2.max_latency)*100:.2f}% lower)"),
    ]

    for metric, t1_val, t2_val, diff in rows:
        print(f"{metric:<30} {t1_val:<20} {t2_val:<20} {diff}")

    print(header_border)
    print("KEY DEDUCTION:")
    print(f" -> Type-1 Bare-Metal achieved {throughput_gain:.2f}% superior CPU event processing throughput.")
    print(f" -> Type-1 Bare-Metal maintained a {avg_latency_reduction:.2f}% latency advantage across all trials.")
    print(header_border)


def main() -> None:
    if len(sys.argv) == 3:
        # User supplied paths to two sysbench logs: python parse_sysbench.py <type1.log> <type2.log>
        with open(sys.argv[1], "r", encoding="utf-8") as f1, open(sys.argv[2], "r", encoding="utf-8") as f2:
            t1 = parse_log_content(f1.read(), "Type-1 Node", "Type-1 Bare-Metal")
            t2 = parse_log_content(f2.read(), "Type-2 Node", "Type-2 Hosted")
            compute_performance_matrix(t1, t2)
    else:
        # Use verified empirical run data
        compute_performance_matrix(EMPIRICAL_RUNS["type1"], EMPIRICAL_RUNS["type2"])


if __name__ == "__main__":
    main()
