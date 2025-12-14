import serial
import time
import os
import keyboard

ARDUINO_PORT = 'COM9'
BAUD_RATE = 115200

borg = 1
last_pressed_time = 0

def increase_borg(event):
    global borg, last_pressed_time
    now = time.time()
    if now - last_pressed_time > 0.2:
        borg += 1
        last_pressed_time = now

keyboard.on_press_key('+', increase_borg)

def get_next_index(directory, prefix="sEMG_data_", extension=".csv"):
    files = os.listdir(directory)
    numbers = []

    for f in files:
        if f.startswith(prefix) and f.endswith(extension):
            num_part = f[len(prefix):-len(extension)]
            if num_part.isdigit():
                numbers.append(int(num_part))

    if not numbers:
        return 0
    return max(numbers) + 1

script_dir = os.path.dirname(os.path.abspath(__file__))
num = get_next_index(script_dir)
file_path = os.path.join(script_dir, f"sEMG_data_{num}.csv")

ser = None
borg = 1

keyboard.on_release_key('+', increase_borg)

try:
    ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
    print(f"{ARDUINO_PORT} connected")

    time.sleep(2)
    ser.reset_input_buffer()

    input("start")

    ser.write(b's')

    header_written = False

    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        while True:
            try:
                line = ser.readline()
                if not line:
                    continue

                try:
                    data_str = line.decode('utf-8').strip()
                except UnicodeDecodeError:
                    continue
                
                if data_str:
                    parts = data_str.split(',')
                    
                    if len(parts) == 4 and all(p.isdigit() for p in parts):
                        
                        if not header_written:
                            f.write("Ch1,Ch2,Ch3,Ch4,label\n")
                            header_written = True
                        
                        data = f"{data_str},{borg}"
                        f.write(data + "\n")
                        print(f"{data}")
                    
            except KeyboardInterrupt:
                raise KeyboardInterrupt

except KeyboardInterrupt:
    print("\nstopped")

except Exception as e:
    print(f"Error: {e}")

finally:
    if ser and ser.is_open:
        ser.write(b'e')
        ser.close()
        print("disconnected")