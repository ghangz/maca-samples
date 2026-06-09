# deviceInfo - MACA Device Query

## Description

This sample queries MACA Runtime device information and prints a compact summary for every visible GPU. It is useful as the first smoke test after starting a MACA container because it verifies that the runtime can enumerate devices before running heavier samples.

## Key Concepts

MACA Runtime API, device enumeration, environment smoke test

## MACA APIs involved

mcGetDeviceCount, mcGetDeviceProperties

## Prerequisites

Download the MACA driver and SDK, then set the toolkit path if it is not installed under `/opt/maca`.

```bash
$ export MACA_PATH=/opt/maca
$ export PATH=${MACA_PATH}/mxgpu_llvm/bin:${MACA_PATH}/bin:$PATH
$ export LD_LIBRARY_PATH=${MACA_PATH}/lib:$LD_LIBRARY_PATH
```

## Build and Run

```bash
$ cd 0_Introduction/deviceInfo
$ make
$ make run
$ make clean
```
