import tkinter as tk
import serial
import xbee
import MySQLdb
import time
import threading
import serial.tools.list_ports
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

i = 1
j = 0
var = {}
db = MySQLdb.connect(host = 'localhost',user = 'root',passwd = 'sahith123',db = 'xbee')
table1 = []
table2 = []
ports = []
data_10 = []

##GUI##
sensing_sys = tk.Tk()
sensing_sys.title("Sensing System")
#sensing_sys.geometry('700x300')
sensing_sys.resizable(0,0)

###FRAMES###

settings = tk.Frame(sensing_sys,bg="white")
settings.pack(side = tk.LEFT)

sensor_readings = tk.Frame(sensing_sys,bg="skyblue")
sensor_readings.pack(side = tk.LEFT)

digital_outputs = tk.Frame(sensing_sys,bg="lightgreen")
digital_outputs.pack(side = tk.LEFT)

###Settings###

tk.Label(settings, text="SETTINGS").grid(column=0, row=0,padx=3)
##PORT##
p = serial.tools.list_ports.comports()
for i in range(len(p)):
    ports.append(p[i][0])
port = tk.StringVar(sensing_sys)
port_choices = ports
port_list = tk.OptionMenu(settings, port, *port_choices)
tk.Label(settings, text="Port").grid(column=0, row=1,padx=3,pady=5)
port_list.grid(row = 1, column =1,pady=5)
def change_port(*args):
    global ports
    ports = port.get()
port.trace('w', change_port)



##Baud Rate##
baud = tk.StringVar(sensing_sys)
baud_choices = { '1200','2400','4800','9600','19200','38400','57600','115200','230400'}
baud.set('9600') # set the default option
baud_list = tk.OptionMenu(settings, baud, *baud_choices)
tk.Label(settings, text="Baud Rate").grid(column=0, row=2,padx = 3,pady=5)
baud_list.grid(row = 2, column =1,pady=5)
def change_baud(*args):
    global brate
    brate = baud.get()
baud.trace('w', change_baud)


##Data Bits##
data = tk.StringVar(sensing_sys)
data_choices = { '4','5','6','7','8'}
data.set('8') # set the default option
data_list = tk.OptionMenu(settings, data, *data_choices)
tk.Label(settings, text="Data Bits").grid(column=0, row=3,padx = 3,pady=5)
data_list.grid(row = 3, column =1,pady=5)
def change_data(*args):
    data.get()
data.trace('w', change_data)


##Open Port##
def OpenPort():
    try:
        global db
        global cur
        cur = db.cursor()
        global serial_port
        serial_port = serial.Serial(ports, brate)
        global conn
        conn = xbee.ZigBee(serial_port)
    except Exception as e:
        print(e)
B = tk.Button(settings, text ="Open Port", command = OpenPort)
B.grid(row = 4, column = 0,pady=5)

    

###Sensor Readings###

def Readings():
    try:
        global i
        global j
        global table1
        global table2
        while(reading_state):
            while(i!=20):
                while(serial_port.read() != b'\x7E'):
                    print('.',end = "")
                l1 = int.from_bytes(serial_port.read(),"big")
                l2 = int.from_bytes(serial_port.read(),"big")
                l = l2 - l1
                global d
                d = serial_port.read(l + 1)
                temp_entry.delete(0, 'end')
                pot_entry.delete(0, 'end')
                global temp
                if(len(d) == 23):
                    temp = 3.3*int.from_bytes(d[18:20],"big")/1023
                    temp = (temp*1000 - 500)/100
                    temp_entry.insert(10,temp)
                    pot_entry.insert(10,int.from_bytes(d[20:22],"big"))

                v = str(time.ctime())
                frame = (v,d)
                i = i+1
                if(j == 0):
                    table1.append(frame)
                else:
                    table2.append(frame)

            i=0
            if(j==0):
                print(table1)
                v = str(time.time())
                var[v] = threading.Thread(target=Commit, args = (table1,))
                var[v].start()
                j=1
                del table1[:]
            else:
                print(table2)
                v = str(time.time())
                var[v] = threading.Thread(target=Commit, args = (table2,))
                var[v].start()
                j=0
                del table2[:]
            
    except Exception as e:
        print(e)
        

def Commit(data):
    try:
        sql_insert_query = "INSERT into frames(time,frame)VALUES(%s,%s)"
        global db
        cur1 = db.cursor()
        n = cur1.executemany(sql_insert_query , data)
        db.commit()
        print(n)
    except (2006, 'MySQL server has gone away'):
        db = MySQLdb.connect(host = 'localhost',user = 'root',passwd = 'sahith123',db = 'xbee')
    except Exception as e:
        print(e)
        
 
tk.Label(sensor_readings, text="SENSOR READINGS").grid(column=0, row=0,padx=3)
##Temperature##
temp = tk.Label(sensor_readings, text="Temperature")
temp.grid(column=0, row=1,padx = 5,pady =5)
temp_entry = tk.Entry(sensor_readings, bd =5)
temp_entry.grid(column=1, row=1,padx = 5,pady =5)

##Potentiometer Readings##
pot = tk.Label(sensor_readings, text="Potentiometer Readings")
pot.grid(column=0, row=2,padx = 5,pady =5)
pot_entry = tk.Entry(sensor_readings, bd =5)
pot_entry.grid(column=1, row=2,padx = 5,pady =5)

def Start():
    try:
        global reading_state
        reading_state = True
        t1 = threading.Thread(target=Readings )
        t1.start()
    except Exception as e:
        print(e)
    

B1 = tk.Button(sensor_readings, text ="Start", command = Start)
B1.grid(row = 3, column = 0,pady=5)

def Stop():
    try:
        global reading_state
        reading_state = False
    except Exception as e:
        print(e)

stop_button = tk.Button(sensor_readings, text ="Stop", command = Stop)
stop_button.grid(row = 3, column = 1,pady=5)


##Graph##
def DataPlot():
    try:
        n = 0
        
        #plt.rcParams['animation.html'] = 'jshtml'
        fig = plt.figure()
        ax = fig.add_subplot(111)
        fig.show()
        i = 0
        x,y = [],[]
        while(data_state and reading_state):
            global d
            global temp
            temp1 = 0
            while(n < 10):
                temp1 = temp1 + temp
                n = n + 1
            n = 0
            temp1 = temp1/10
            i = time.time()
            x.append(i)
            y.append(temp1)
            ax.plot(x,y,color = 'b')
            fig.canvas.draw()
            ax.set_xlim(left=max(0,i-2), right = i+2)
            time.sleep(0.01)
            
    except Exception as e:
        print(e)

        
def StartPlot():
    try:
        global data_state
        data_state = True
        t1 = threading.Thread(target=DataPlot )
        t1.start()
        
    except Exception as e:
        print(e)
    
def StopPlot():
    try:
        global data_state
        data_state = False
        
    except Exception as e:
        print(e)

        
graph_b = tk.Button(sensor_readings, text ="Start_plot", command = StartPlot)
graph_b.grid(row = 4, column = 0,pady=5)


graph_b = tk.Button(sensor_readings, text ="Stop_plot", command = StopPlot)
graph_b.grid(row = 4, column = 1,pady=5)




###Digital Outputs###
tk.Label(digital_outputs, text="DIGITAL OUTPUTS").grid(column=0, row=0,padx=3)

def Send_command():
    try:
        a1 = address_entry.get()
        a0 = bytearray(b'\x00\x13\xA2\x00')
        a2 = bytearray.fromhex(a1)
        a = a0 + a2

        if(s == "ON"):
            p = b'\x05'
        else:
            p = b'\x04'
        conn.remote_at(dest_addr_long= a ,dest_addr=b'\xFF\xFE',command='D2',parameter = p)
        print("Command Sent")
        
    except Exception as e:
        print(e)
##address##
address = tk.Label(digital_outputs, text="Address")
address.grid(column=0, row=1,padx = 5,pady =5)


address_entry = tk.Entry(digital_outputs, bd =2)
address_entry.grid(column=1, row=1,padx = 5,pady =3)




##ON/OFF##
state = tk.StringVar(digital_outputs)
state_choices = { 'ON','OFF'}
state.set('ON') # set the default option
state_list = tk.OptionMenu(digital_outputs, state, *state_choices)
tk.Label(digital_outputs, text="ON/OFF").grid(column=0, row=2,padx = 3)
state_list.grid(row = 2, column =1)
def change_state(*args):
    global s
    s = state.get()
state.trace('w', change_state)



B2 = tk.Button(digital_outputs, text ="Send", command = Send_command)
B2.grid(row = 4,pady=5)

def close_window():
    data_state = False
    db.close()
    sensing_sys.destroy()
B3 = tk.Button(digital_outputs, text ="EXIT", command =close_window)
B3.grid(row = 4,column = 1,pady=5)


sensing_sys.mainloop()


