import serial
import matplotlib.pyplot as plt
import time
import numpy as np
import pandas as pd
import datetime

### --  factor obtenido de la celda -- ###
factor = 1

plt.ion()
fig, ax = plt.subplots()
line, = ax.plot([])
ax.set_ylim(-22000, 1023)
ax.set_xlim(0, 100)
ax.set_title('ME5120 - Celda de carga')
ax.set_xlabel('Tiempo (s)')
ax.set_ylabel('Carga [N]')
ax.grid()
# create button to stop the program
button = plt.Button(plt.axes([0.8, 0.05, 0.15, 0.075]), 'Save data')

x_data = np.array([])
y_data = np.array([])

def open_serial():
    global ser
    try:
        #Select port
        ser = serial.Serial("/dev/cu.wchusbserial14230", 115200, timeout=1, write_timeout=0.1)
        print("The port is available")
        time.sleep(2)
    except serial.serialutil.SerialException:
        print("The port is at use")
        ser.close()
        ser.open()

def read_serial():
    global ser
    global time_s
    value = 0
    time_s = 0
    message = ser.readline()
    #print(message)
    if b'VAL' in message:
        value = int(message.split(b',')[1].strip())
        time_s = float(message.split(b',')[2].strip())/1000

    return value, time_s

def send_command(cmd='GO'):
    global ser
    msg = cmd + '\n'
    # Execute the function
    ser.write(msg.encode())

def save_data(event):
    # example data
    datos_tiempo = x_data
    datos_carga = y_data

    # create a pandas DataFrame from the data
    df = pd.DataFrame({'Tiempo': datos_tiempo, 'Carga': datos_carga})
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    # save the DataFrame to a CSV file
    df.to_csv('datos_celda_{}.csv'.format(timestamp), index=False)
    print('Data saved')


button.on_clicked(save_data)

open_serial()
send_command()
start_time = time.time()
while True:
    try:
        value_celda,time_s = read_serial()
        value_norm = value_celda*factor
        x_data = np.append(x_data, time_s)
        y_data = np.append(y_data, value_norm)
        line.set_data(x_data, y_data)
        ax.set_xlim(max(0, x_data[-1] - 100), x_data[-1])
        fig.canvas.draw()
        fig.canvas.flush_events()
    except KeyboardInterrupt:
        break

