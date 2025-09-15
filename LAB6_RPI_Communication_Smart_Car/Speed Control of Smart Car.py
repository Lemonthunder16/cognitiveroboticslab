# AccelerateSpeed.py
#!/usr/bin/env python3
import serial, time

i=0
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM4', 9600, timeout=1)
    ser.reset_input_buffer()

    while True:
        line=str(i)
        line_encode=line.encode()
        ser.write(line_encode)
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(1)
        i=i+1
