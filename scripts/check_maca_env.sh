#!/usr/bin/env bash
set -euo pipefail

MACA_PATH="${MACA_PATH:-/opt/maca}"
MXCC="${MXCC:-${MACA_PATH}/mxgpu_llvm/bin/mxcc}"

failures=0

check_path() {
  local label="$1"
  local path="$2"
  if [[ -e "${path}" ]]; then
    printf '[OK] %s: %s\n' "${label}" "${path}"
  else
    printf '[FAIL] %s not found: %s\n' "${label}" "${path}" >&2
    failures=$((failures + 1))
  fi
}

printf 'MACA_PATH=%s\n' "${MACA_PATH}"
printf 'MXCC=%s\n' "${MXCC}"

check_path "MACA root" "${MACA_PATH}"
check_path "mxcc compiler" "${MXCC}"
check_path "runtime header" "${MACA_PATH}/include/mc_runtime.h"
check_path "runtime library directory" "${MACA_PATH}/lib"

if [[ -x "${MXCC}" ]]; then
  "${MXCC}" --version || true
fi

if [[ "${failures}" -ne 0 ]]; then
  printf 'MACA sample environment check failed with %d missing item(s).\n' "${failures}" >&2
  exit 1
fi

printf 'MACA sample environment check passed.\n'
