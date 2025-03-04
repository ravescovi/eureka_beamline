#!/usr/bin/env python3
import math
import time
from caproto.server import pvproperty, PVGroup, run

class SimulatedPVGroup(PVGroup):
    # A simple counter that increments every second.
    counter = pvproperty(value=0)
    # A sine wave that updates every 0.1 seconds.
    sine = pvproperty(value=0.0)

    @counter.scan(period=1.0)
    async def counter(self, instance, async_lib):
        instance.value += 1

    @sine.scan(period=0.1)
    async def sine(self, instance, async_lib):
        instance.value = math.sin(time.time())

if __name__ == '__main__':
    # Pass a prefix to the PVGroup instance (e.g., "sim:")
    run(SimulatedPVGroup(prefix='sim:'))
