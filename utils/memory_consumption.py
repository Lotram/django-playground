from threading import Thread
from time import sleep

import psutil


def measure_ram_consumption(function_to_audit):
    """Output the RAM consumption of the function passed as parameter"""
    initial_available_memory = psutil.virtual_memory().available
    min_available_memory = initial_available_memory
    is_running = True
    mem_data = []

    class RamUsageThread(Thread):
        def run(self) -> None:
            nonlocal min_available_memory
            while is_running:
                available_memory = psutil.virtual_memory().available
                mem_data.append(available_memory)
                min_available_memory = min(available_memory, min_available_memory)
                sleep(0.1)
            return min_available_memory

    ram_thread = RamUsageThread()
    ram_thread.start()
    function_to_audit()
    is_running = False

    print(
        "RAM consumption:",
        (initial_available_memory - min_available_memory) / 2**20,
        "MB",
    )
    return mem_data
