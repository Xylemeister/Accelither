import multiprocessing.shared_memory as shm

class RawNS():
    __INPUT_SHARED_MEMORY_NAME = "acc_in"
    __input_shared_memory = shm.SharedMemory(name = __INPUT_SHARED_MEMORY_NAME)

    __OUTPUT_SHARED_MEMORY_NAME = "acc_out"
    __output_shared_memory = shm.SharedMemory(name = __OUTPUT_SHARED_MEMORY_NAME)

    def __bytesToInt(self, byte1, byte2):
        """
        Converts 2 bytes of signed 16-bit number to int.
        """
        val = (byte1 << 8) + byte2
        if val > 0x8000: return val - 0x10000
        else: return val

    def getX(self):
        """
        Gets raw X reading from shared memory.
        """
        return self.__bytesToInt(self.__input_shared_memory.buf[0], self.__input_shared_memory.buf[1])
    
    def getY(self):
        """
        Gets raw Y reading from shared memory.
        """
        return self.__bytesToInt(self.__input_shared_memory.buf[2], self.__input_shared_memory.buf[3])
    
    def getZ(self):
        """
        Gets raw Z reading from shared memory.
        """
        return self.__bytesToInt(self.__input_shared_memory.buf[4], self.__input_shared_memory.buf[5])

    def getSwitches(self):
        """
        Gets switch readings from shared memory. Returns an array where bit N is SW[N].
        """
        return (self.__bytesToInt(self.__input_shared_memory.buf[6], self.__input_shared_memory.buf[7]) >> 4) & 0x3ff

    def getSwitch(self, switch_num):
        """
        Gets specific switch reading from shared memory.
        """
        return (self.getSwitches() & (1 << switch_num)) != 0

    def getButtons(self):
        """
        Gets button readings from shared memory. Returns an array where bit N is KEY[N].
        """
        return (self.__input_shared_memory.buf[6] >> 6) & 0x3
    
    def getButton(self, button_num):
        """
        Gets specific button reading from shared memory.
        """
        return (self.getButtons() & (1 << button_num)) != 0
    
    def set7Seg(self, seg_num, val):
        """
        Sets specific 7 segment value in shared memory.\n
        `val` = `tuple` or `list` with 7 `booleans`, or single `int`.\n
        Note: displays are numbered left-to-right, not using N in HEXN.
        """
        if type(val) == tuple or type(val) == list:
            tmp = 0
            for i in range(7):
                if val[i]: tmp += 1 << i
            val = tmp

        self.__output_shared_memory.buf[seg_num] = (self.__output_shared_memory.buf[seg_num] & 0x80) + val
        
    def setLED(self, led_num, val):
        """
        Sets specific LED, where:\n
        `led_num` = N in LED[N],\n
        `val` = boolean.
        """
        if led_num < 8:
            if val: self.__output_shared_memory.buf[6] |= 1 << led_num
            else: self.__output_shared_memory.buf[6] &= (0xff - (1 << led_num))
        
        elif led_num == 8:
            if val: self.__output_shared_memory.buf[4] |= 0x80
            else: self.__output_shared_memory.buf[4] &= 0x7f
        
        elif led_num == 9:
            if val: self.__output_shared_memory.buf[5] |= 0x80
            else: self.__output_shared_memory.buf[5] &= 0x7f


Raw = RawNS()
"""
Namespace for static functions which read raw input from shared memory.
"""

if __name__ == "__main__":
    if input("Enter 'Y' to perform accelerometer test\n>   ").upper() == "Y":
        while True:
            print(Raw.getX(), Raw.getY(), Raw.getZ())

    elif input("Enter 'Y' to perform switches test\n>   ").upper() == "Y":
        while True:
            print([Raw.getSwitch(i) for i in range(10)])

    elif input("Enter 'Y' to perform buttons test\n>   ").upper() == "Y":
        while True:
            print([Raw.getButton(i) for i in range(2)])

    elif input("Enter 'Y' to perform 7 segment test\n>   ").upper() == "Y":
        Raw.set7Seg(0, (True, False, False, True, True, True, True))
        Raw.set7Seg(1, [False, False, True, False, False, True, False])
        Raw.set7Seg(2, 48)
        Raw.set7Seg(3, 127)
        Raw.set7Seg(4, 0)
        Raw.set7Seg(5, 127)

    elif input("Enter 'Y' to perform LED test\n>   ").upper() == "Y":
        from time import sleep
        for i in range(10):
            Raw.setLED(i, True)
            sleep(0.2)
        for i in range(10):
            Raw.setLED(i, False)
            sleep(0.2)