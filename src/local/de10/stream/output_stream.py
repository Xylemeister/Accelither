"C:/intelFPGA_lite/18.1/nios2eds/Nios II Command Shell.bat"

import multiprocessing.shared_memory as shm
from time import sleep

OUTPUT_BYTE_COUNT = 7
SHARED_MEMORY_NAME = "acc_out"

FREQUENCY = 100

# Create if doesn't exist
try:
    shared_mem = shm.SharedMemory(name = SHARED_MEMORY_NAME, size = OUTPUT_BYTE_COUNT, create = True)
except:
    shared_mem = shm.SharedMemory(name = SHARED_MEMORY_NAME, size = OUTPUT_BYTE_COUNT)

while True:
    # Hex values
    out = 0
    for i in range(6):
        out += shared_mem.buf[i] & 0x7f
        out <<= 7
    
    out <<= 3
    out += (shared_mem.buf[5] & 0x80) << 2
    out += (shared_mem.buf[4] & 0x80) << 1
    out += shared_mem.buf[6]

    print("/", end = "")
    for i in range(48, -1, -4):
        print(hex((out >> i) & 0xf)[2], end = "")
    print("", flush = True)
    
    sleep(1 / FREQUENCY)