# ForwardMovement.py
#!/usr/bin/env python3
import serial, time

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM4', 9600, timeout=1)
    ser.reset_input_buffer()

    while True:
        line='1'
        line_encode=line.encode()
        ser.write(line_encode)
        time.sleep(1)
