################################################################################
# Copyright 2026 MetaX Integrated Circuits (Shanghai) Co.,Ltd.
#
# SPDX-License-Identifier: BSD-3-Clause
################################################################################

MACA_PATH ?= /opt/maca
MXCC      := $(MACA_PATH)/mxgpu_llvm/bin/mxcc
MXCCFLAGS := -x maca

.PHONY: all run clean

all: deviceInfo

deviceInfo: deviceInfo.cpp
	$(MXCC) $(MXCCFLAGS) $< -o $@ --maca-path=$(MACA_PATH)

run: deviceInfo
	./deviceInfo

clean:
	rm -rf deviceInfo deviceInfo.o
