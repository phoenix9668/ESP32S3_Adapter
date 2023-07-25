from machine import UART, Pin
from time import sleep_ms

class E34_2G4H20D_Class:
    """ E34-2G4H20D class, incloud configure function"""

    def __init__(self, addh=0xf0, addl=0x00, alise="E34-2G4H20D"):
        # Initialization command
        self.uart2_dev = UART(2, baudrate=9600, tx=43, rx=44)
        self.m0 = Pin(38, Pin.OUT)
        self.m1 = Pin(39, Pin.OUT)
        self.aux = Pin(40, Pin.IN)
        self.dev_head = 0xc0
        self.dev_addh = addh
        self.dev_addl = addl
        self.dev_sped = 0x18
        
        # | 3,2,1,0 通信信道（00H~0BH,共计12个信道）
        # | 定频模式（模式0）
        # | 0~5信道对应频率  | 2400M + CHAN * 2M     |
        # | 6~11信道对应频率 | 2508M + (CHAN-6) * 2M |
        # | 跳频模式（模式1）
        # | 0~11信道对应频率 | 2412M + CHAN * 2M     |
        self.dev_chan = 0x00
        self.dev_option = 0x00
        self.dev_speed = {'baudrate_9600': 0x18, 'baudrate_57600': 0x30, 'baudrate_115200': 0x38}
        self.dev_model = ['Fixed_Frequency_Mode','Frequency_Hopping_Mode','Reserve_Mode','Sleep_Mode']
#         config_reg(addh=addh, addl=addl, chan=self.dev_chan, mode='Fixed_Frequency_Mode')
        pass
    
    def model_sel(self, mode='Fixed_Frequency_Mode'):
        if (mode == self.dev_model[0]):
            self.m0.value(0)
            self.m1.value(0)
        elif (mode == self.dev_model[1]):
            self.m0.value(1)
            self.m1.value(0)
        elif (mode == self.dev_model[2]):
            self.m0.value(0)
            self.m1.value(1)
        elif (mode == self.dev_model[3]):
            self.m0.value(1)
            self.m1.value(1)

    def config_reg(self, baudrate=9600, addh=0xf0, addl=0x00, chan=0x00, mode='Fixed_Frequency_Mode'):
        self.uart2_dev.init(baudrate = 9600)
        self.read_reg()
        
        self.dev_addh = addh
        self.dev_addl = addl
        if (baudrate == 9600):
            self.dev_sped = self.dev_speed['baudrate_9600']
        elif (baudrate == 57600):
            self.dev_sped = self.dev_speed['baudrate_57600']
        elif (baudrate == 115200):
            self.dev_sped = self.dev_speed['baudrate_115200']
        self.dev_chan = chan
        w_bytes_list = bytearray([self.dev_head,self.dev_addh,self.dev_addl,self.dev_sped,self.dev_chan,self.dev_option])
        print("w_bytes_list: ",end="")
        print(w_bytes_list)
        self.uart2_dev.write(w_bytes_list)
        sleep_ms(100)
        r_bytes_list = self.uart2_dev.read()
        print("r_bytes_list: ",end="")
        print(r_bytes_list)
        if (w_bytes_list == r_bytes_list):
            print('#--config register success--#')
        
        self.uart2_dev.init(baudrate = baudrate)
        self.model_sel(mode)
        sleep_ms(2)

    def read_reg(self):
        while (self.aux.value() == 0):
            sleep_ms(2)
        self.model_sel('Sleep_Mode')
        sleep_ms(2)
        print(bytearray([0xc1,0xc1,0xc1]))
        self.uart2_dev.write(bytearray([0xc1,0xc1,0xc1]))
        sleep_ms(100)
        print(self.uart2_dev.read())
        
    def read_version(self):
        while (self.aux.value() == 0):
            sleep_ms(2)
        self.model_sel('Sleep_Mode')
        sleep_ms(2)
        print(bytearray([0xc3,0xc3,0xc3]))
        self.uart2_dev.write(bytearray([0xc3,0xc3,0xc3]))
        sleep_ms(100)
        print(self.uart2_dev.read())
        
    def reset_dev(self):
        while (self.aux.value() == 0):
            sleep_ms(2)
        self.model_sel('Sleep_Mode')
        sleep_ms(2)
        print('#--reset e34-2g4h20d--#')
        self.uart2_dev.write(bytearray([0xc4,0xc4,0xc4]))
        
        
