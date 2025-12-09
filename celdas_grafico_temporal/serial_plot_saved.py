import serial
import time
import matplotlib.pyplot as plt
import csv
from datetime import datetime
import numpy as np
import json
import pandas as pd
# Serial port configuration
serial_port = '/dev/tty.usbmodem1412201'  # Replace with your Arduino's serial port (e.g., COM3 on Windows)
baud_rate = 115200
timeout = 5

# List to store all data for saving to CSV
all_data = []
plt.ion()
fig, ax = plt.subplots()
line_ax, = ax.plot([])
line_2_ax, = ax.plot([])
line_3_ax, = ax.plot([])
line_4_ax, = ax.plot([])
line_5_ax, = ax.plot([])
line_6_ax, = ax.plot([])
line_7_ax, = ax.plot([])
line_8_ax, = ax.plot([])
line_9_ax, = ax.plot([])
ax.legend(['Celda 1', 'Celda 2', 'Celda 3', 'Celda 4', 'Celda 5', 'Celda 6', 'Celda 7', 'Celda 8', 'Celda 9'], loc='upper left')
ax.set_xlim(0, 100)
ax.set_title('Celda de carga')
ax.set_xlabel('Tiempo (s)')
ax.set_ylabel('Carga')
ax.grid()
# create button to stop the program
button = plt.Button(plt.axes([0.8, 0.05, 0.15, 0.075]), 'Save data')

x_data = np.array([])
y1_data = np.array([])
y2_data = np.array([])
y3_data = np.array([])
y4_data = np.array([])
y5_data = np.array([])
y6_data = np.array([])
y7_data = np.array([])
y8_data = np.array([])
y9_data = np.array([])

def save_data(event):
    # example data
    datos_tiempo = x_data
    datos_celda_1 = y1_data
    datos_celda_2 = y2_data
    datos_celda_3 = y3_data
    datos_celda_4 = y4_data
    datos_celda_5 = y5_data
    datos_celda_6 = y6_data
    datos_celda_7 = y7_data
    datos_celda_8 = y8_data
    datos_celda_9 = y9_data

    # create a pandas DataFrame from the data
    df = pd.DataFrame({'Tiempo': datos_tiempo, 'Celda_1': datos_celda_1, 'Celda_2': datos_celda_2, 'Celda_3': datos_celda_3, 'Celda_4': datos_celda_4, 'Celda_5': datos_celda_5, 'Celda_6': datos_celda_6, 'Celda_7': datos_celda_7, 'Celda_8': datos_celda_8, 'Celda_9': datos_celda_9})
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    # save the DataFrame to a CSV file
    df.to_csv('datos_celdas_{}.csv'.format(timestamp), index=False)
    print('Data saved')
    exit()


button.on_clicked(save_data)

try:
    ser = serial.Serial(serial_port, baud_rate, timeout=timeout)
    time.sleep(2)  # Wait for the serial port to initialize
    ser.flush()
    start_time = time.time()
    while True:  
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if not line:
            continue
        elif line.startswith('{') and line.endswith('}'):
            try:
                # Parse the JSON data
                data_dict = json.loads(line)
                # Extract the values from the JSON data
                celda_1 = (float(data_dict["celda_1"])-234500)/823500
                celda_2 = (float(data_dict["celda_2"])-314500)/855500
                celda_3 = (float(data_dict["celda_3"])-184000)/832500
                celda_4 = float(data_dict["celda_4"])
                celda_5 = float(data_dict["celda_5"])
                celda_6 = float(data_dict["celda_6"])
                celda_7 = float(data_dict["celda_7"])
                celda_8 = (float(data_dict["celda_8"])- 97500)/859500
                celda_9 = float(data_dict["celda_9"])
                x_data = np.append(x_data, time.time() - start_time)
                y1_data = np.append(y1_data, celda_1)
                y2_data = np.append(y2_data, celda_2)
                y3_data = np.append(y3_data, celda_3)
                y4_data = np.append(y4_data, celda_4)
                y5_data = np.append(y5_data, celda_5)
                y6_data = np.append(y6_data, celda_6)
                y7_data = np.append(y7_data, celda_7)
                y8_data = np.append(y8_data, celda_8)
                y9_data = np.append(y9_data, celda_9)
                line_ax.set_data(x_data, y1_data)
                line_2_ax.set_data(x_data, y2_data)
                line_3_ax.set_data(x_data, y3_data)
                line_4_ax.set_data(x_data, y4_data)
                line_5_ax.set_data(x_data, y5_data)
                line_6_ax.set_data(x_data, y6_data)
                line_7_ax.set_data(x_data, y7_data)
                line_8_ax.set_data(x_data, y8_data)
                line_9_ax.set_data(x_data, y9_data)
                fig.canvas.draw()
                fig.canvas.flush_events()
                ax.set_xlim(max(0, x_data[-1] - 100), x_data[-1])
                ax.set_ylim(min(np.min(y1_data), np.min(y2_data), np.min(y3_data), np.min(y4_data), np.min(y5_data), np.min(y6_data), np.min(y7_data), np.min(y8_data), np.min(y9_data)) - 0.1,
                             max(np.max(y1_data), np.max(y2_data), np.max(y3_data), np.max(y4_data), np.max(y5_data), np.max(y6_data), np.max(y7_data), np.max(y8_data), np.max(y9_data)) + 0.1)
            except json.JSONDecodeError as e:
                print(e)
                continue  # Skip invalid JSON
            except KeyError as e:
                print(e)
                continue  # Skip if expected keys are missing
            
            
except serial.SerialException as e:
    print(f"Serial error: {e}")
    save_data(None)
except KeyboardInterrupt:
    print("Program terminated by user.")
    save_data(None)


finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")