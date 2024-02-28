"C:/intelFPGA_lite/18.1/nios2eds/Nios II Command Shell.bat"

import multiprocessing.shared_memory as shm

INPUT_BYTE_COUNT = 8
SHARED_MEMORY_NAME = "acc_in"

# Create if doesn't exist
try:
    shared_mem = shm.SharedMemory(name = SHARED_MEMORY_NAME, size = INPUT_BYTE_COUNT, create = True)
except:
    shared_mem = shm.SharedMemory(name = SHARED_MEMORY_NAME, size = INPUT_BYTE_COUNT)

while True:
    inp = input() + "0"
    for i in range(INPUT_BYTE_COUNT):
        try:
            shared_mem.buf[i] = int(inp[2*i]+inp[2*i+1], 16)
        except:
            pass # Non-int received e.g. upon connecting. Want to ignore
    
