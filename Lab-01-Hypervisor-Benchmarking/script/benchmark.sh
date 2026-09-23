#!/usr/bin/env bash
# ==============================================================================
# Script Name   : benchmark.sh
# Description   : Automated CPU Virtualization Benchmark & System Audit
# Target System : Ubuntu / Debian Linux Guests
# Dependencies  : sysbench, util-linux, coreutils
# ==============================================================================

set -euo pipefail

# Visual formatting constants
BOLD="\033[1m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
YELLOW="\033[1;33m"
RESET="\033[0m"

# Configuration variables
TIMESTAMP="$(date +'%Y%m%d_%H%M%S')"
HOSTNAME_ID="$(hostname -s 2>/dev/null || hostname)"
LOG_DIR="benchmark_logs"
REPORT_FILE="${LOG_DIR}/sysbench_cpu_${HOSTNAME_ID}_${TIMESTAMP}.log"
PRIME_LIMIT=20000
THREADS=1

mkdir -p "${LOG_DIR}"

log_header() {
    echo -e "${BLUE}${BOLD}====================================================================${RESET}"
    echo -e "${BLUE}${BOLD}   VIRTUALIZATION BENCHMARK & SYSTEM AUDIT UTILITY                  ${RESET}"
    echo -e "${BLUE}${BOLD}====================================================================${RESET}"
    echo -e "Timestamp       : $(date -u +'%Y-%m-%d %H:%M:%S UTC')"
    echo -e "Host Identifier : ${HOSTNAME_ID}"
    echo -e "Kernel Release  : $(uname -r)"
    echo -e "Architecture    : $(uname -m)"
    echo -e "--------------------------------------------------------------------"
}

audit_hardware() {
    echo -e "\n${YELLOW}${BOLD}[1/3] Auditing System & Virtual Hardware Topology...${RESET}"
    echo -e "--- CPU Architecture & Configuration ---"
    lscpu | grep -E "Model name|CPU\(s\)|Thread\(s\) per core|Core\(s\) per socket|Socket\(s\)|Vendor ID|Virtualization" || true

    echo -e "\n--- Memory Allocation & Utilization ---"
    free -h

    echo -e "\n--- Storage Footprint ---"
    df -h /
}

prepare_environment() {
    echo -e "\n${YELLOW}${BOLD}[2/3] Verifying Benchmark Dependencies...${RESET}"
    if ! command -v sysbench &>/dev/null; then
        echo -e "${YELLOW}sysbench binary not detected. Attempting installation via APT...${RESET}"
        sudo apt-get update -qq && sudo apt-get install -y -qq sysbench
    fi
    echo -e "${GREEN}Sysbench version: $(sysbench --version)${RESET}"
}

run_cpu_benchmark() {
    echo -e "\n${YELLOW}${BOLD}[3/3] Executing Prime Sieve Benchmark (Max Prime: ${PRIME_LIMIT}, Threads: ${THREADS})...${RESET}"
    echo "Benchmark started at: $(date)"
    
    # Run benchmark and stream output to both console and log
    sysbench cpu \
        --cpu-max-prime="${PRIME_LIMIT}" \
        --threads="${THREADS}" \
        run | tee -a "${REPORT_FILE}"

    echo "Benchmark completed at: $(date)"
}

# Execution Pipeline
{
    log_header
    audit_hardware
    prepare_environment
    run_cpu_benchmark
} 2>&1 | tee "${REPORT_FILE}"

echo -e "\n${GREEN}${BOLD}✔ Benchmark execution complete.${RESET}"
echo -e "Detailed telemetry saved to: ${BOLD}${REPORT_FILE}${RESET}\n"
