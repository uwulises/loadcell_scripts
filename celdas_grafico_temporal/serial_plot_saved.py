import serial
import time
import matplotlib.pyplot as plt
import csv
from datetime import datetime
import numpy as np
import json
import pandas as pd
# Serial port configuration
serial_port = '/dev/tty.usbmodem1422301'  # Replace with your Arduino's serial port (e.g., COM3 on Windows)
baud_rate = 57600
timeout = 5

# List to store all data for saving to CSV
all_data = []
plt.ion()
fig, ax = plt.subplots()
line_ax, = ax.plot([])
ax.set_xlim(0, 100)
ax.set_title('Celda de carga')
ax.set_xlabel('Tiempo (s)')
ax.set_ylabel('Carga')
ax.grid()
# create button to stop the program
button = plt.Button(plt.axes([0.8, 0.05, 0.15, 0.075]), 'Save data')

x_data = np.array([])
y_data = np.array([])


# Function to save the data to a CSV file
def save_to_csv(name='G'):
    if all_data:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_data_{now}.csv"
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['celda_1', 'celda_2', 'celda_3', 'celda_4', 'celda_5', 'celda_6', 'celda_7', 'celda_8', 'celda_9'])
            writer.writerows(all_data)
        print(f"\nData saved to '{filename}'")
    else:
        print("\nNo data to save.")
    return filename

def save_data(event):
    # example data
    datos_tiempo = x_data
    datos_carga = y_data

    # create a pandas DataFrame from the data
    df = pd.DataFrame({'Tiempo': datos_tiempo, 'Carga': datos_carga})
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    # save the DataFrame to a CSV file
    df.to_csv('datos_celda_{}.csv'.format(timestamp), index=False)
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
        elif line.startswith('{'):
            try:
                # Parse the JSON data
                data_dict = json.loads(line)
            except json.JSONDecodeError as e:
                print(e)
                continue  # Skip invalid JSON
        
            # Extract the values from the JSON data
            celda_1 = float(data_dict["celda_1"])
            celda_2 = float(data_dict["celda_2"])
            celda_3 = float(data_dict["celda_3"])
            celda_4 = float(data_dict["celda_4"])
            celda_5 = float(data_dict["celda_5"])
            celda_6 = float(data_dict["celda_6"])
            celda_7 = float(data_dict["celda_7"])
            celda_8 = float(data_dict["celda_8"])
            celda_9 = float(data_dict["celda_9"])

            # Add the data to the list for saving to CSV
            all_data.append([celda_1, celda_2, celda_3, celda_4, celda_5, celda_6, celda_7, celda_8, celda_9])
            #print(f"Celda 1: {celda_1}, Celda 2: {celda_2}, Celda 3: {celda_3}, Celda 4: {celda_4}, Celda 5: {celda_5}, Celda 6: {celda_6}, Celda 7: {celda_7}, Celda 8: {celda_8}, Celda 9: {celda_9}")

            x_data = np.append(x_data, time.time() - start_time)
            y_data = np.append(y_data, celda_1)
            line_ax.set_data(x_data, y_data)
            ax.set_xlim(max(0, x_data[-1] - 100), x_data[-1])
            ax.set_ylim(min(y_data)-100, max(y_data)+100)
            fig.canvas.draw()
            fig.canvas.flush_events()


except serial.SerialException as e:
    print(f"Error opening serial port {serial_port}: {e}")
except KeyboardInterrupt:
    print("Program terminated by user.")
    save_data(None)


finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")