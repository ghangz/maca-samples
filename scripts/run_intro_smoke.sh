#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="${LOG_DIR:-${ROOT_DIR}/smoke-logs/$(date +%Y%m%d-%H%M%S)}"

SAMPLES=(
  "0_Introduction/vectorAdd"
  "0_Introduction/asyncMemcpy"
  "0_Introduction/pinnedMemory"
  "0_Introduction/sharedMemory"
)

mkdir -p "${LOG_DIR}"
printf 'MACA intro smoke logs: %s\n' "${LOG_DIR}"

for sample in "${SAMPLES[@]}"; do
  sample_dir="${ROOT_DIR}/${sample}"
  sample_log_dir="${LOG_DIR}/${sample//\//_}"
  mkdir -p "${sample_log_dir}"
  printf '[RUN] %s\n' "${sample}"
  (
    cd "${sample_dir}"
    make clean
    make
    make run
  ) >"${sample_log_dir}/stdout.log" 2>"${sample_log_dir}/stderr.log" || {
    printf '[FAIL] %s, see %s\n' "${sample}" "${sample_log_dir}" >&2
    exit 1
  }
  printf '[OK] %s\n' "${sample}"
done

printf 'All selected intro samples passed.\n'
