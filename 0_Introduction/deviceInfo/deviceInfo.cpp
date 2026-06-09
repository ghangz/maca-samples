/* Copyright 2026 MetaX Integrated Circuits (Shanghai) Co.,Ltd.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

#include <mc_runtime.h>

#include <cstdio>

int main()
{
    int device_count = 0;
    mcError_t status = mcGetDeviceCount(&device_count);
    if (status != mcSuccess)
    {
        std::printf("mcGetDeviceCount failed: %s\n", mcGetErrorString(status));
        return 1;
    }

    std::printf("MACA device count: %d\n", device_count);
    if (device_count == 0)
    {
        return 1;
    }

    for (int device = 0; device < device_count; ++device)
    {
        mcDeviceProp_t prop;
        status = mcGetDeviceProperties(&prop, device);
        if (status != mcSuccess)
        {
            std::printf("mcGetDeviceProperties(%d) failed: %s\n", device, mcGetErrorString(status));
            return 1;
        }
        std::printf("device=%d name=%s multiprocessors=%d unifiedAddressing=%d\n",
                    device,
                    prop.name,
                    prop.multiProcessorCount,
                    prop.unifiedAddressing);
    }

    return 0;
}
