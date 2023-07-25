from machine import UART
from time import sleep_ms
import _thread
from e34_2g4h20d_driver import E34_2G4H20D_Class

uart1 = UART(1, baudrate=9600, tx=42, rx=41)
# uart2 = UART(2, baudrate=115200, tx=43, rx=44)


def uart1_read():
    sleep_ms(2000)
    print('#--begin reveive tmr data--#')
    global uart1
    while True:
        msg_len = uart1.any()
        if msg_len:
            print("uart1_msg_len: " + str(msg_len))
            msg = uart1.readline()
            msg = msg.decode().split()
            print("uart1_read msg: " + msg[0])
            e34_2g4h20d_dev.uart2_dev.write(msg[0])
        sleep_ms(10)

_thread.start_new_thread(uart1_read, ())

if __name__ == '__main__':
    sleep_ms(500)
    e34_2g4h20d_dev = E34_2G4H20D_Class()
    e34_2g4h20d_dev.config_reg(baudrate=9600,mode='Fixed_Frequency_Mode')         

#     sleep_ms(100)
#     e34_2g4h20d_dev.read_version()
#     e34_2g4h20d_dev.config_reg(baudrate=115200)
    sleep_ms(500)
    print('#--program runing--#')
    while True:
        if (e34_2g4h20d_dev.uart2_dev.any()):
            data2 = e34_2g4h20d_dev.uart2_dev.read()
#             print(data2)
#             print("uart2_read msg: " + data2.decode())
        sleep_ms(10)
        
        