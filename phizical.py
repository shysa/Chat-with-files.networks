# !/usr/bin/python


#import serial.tools.list_ports
import datetime
import threading
import time
import serial
import channel
# import ft_serial_1
#from serial.tools import list_ports

# initialization and open the port

# possible timeout values:
#    1. None: wait forever, block call
#    2. 0: non-blocking mode, return immediately
#    3. x, x is bigger than 0, float allowed, timeout block call


ser_1 = serial.Serial()
# ser.port = "/dev/ttyUSB0"
ser_1.port = "COM6"
# ser.port = "/dev/ttyS2"
ser_1.baudrate = 115200
ser_1.bytesize = serial.EIGHTBITS  # number of bits per bytes
ser_1.parity = serial.PARITY_NONE  # set parity check: no parity
ser_1.stopbits = serial.STOPBITS_ONE  # number of stop bits
# ser.timeout = None  #block read
ser_1.timeout = 1  # non-block read
# ser.timeout = 2  #timeout block read
# ser_1.xonxoff = False  # disable software flow control
# ser_1.rtscts = False  # disable hardware (RTS/CTS) flow control
# ser_1.dsrdtr = False  # disable hardware (DSR/DTR) flow control
ser_1.writeTimeout = None  # timeout for write

ser_2 = serial.Serial()
# ser.port = "/dev/ttyUSB0"
ser_2.port = "COM7"
# ser.port = "/dev/ttyS2"
ser_2.baudrate = 115200
ser_2.bytesize = serial.EIGHTBITS  # number of bits per bytes
ser_2.parity = serial.PARITY_NONE  # set parity check: no parity
ser_2.stopbits = serial.STOPBITS_ONE  # number of stop bits
# ser.timeout = None          #block read
ser_2.timeout = 1  # non-block read
# ser.timeout = 2              #timeout block read
# ser_2.xonxoff = False  # disable software flow control
# ser_2.rtscts = False  # disable hardware (RTS/CTS) flow control
# ser_2.dsrdtr = False  # disable hardware (DSR/DTR) flow control
ser_2.writeTimeout = 20  # timeout for write

priem = 0

frames = []

def ser_open():
    try:
        ser_1.open()
        ser_2.open()
    except Exception as e:
        print("error open serial port: " + str(e))
        exit()


def ser_write(binary_message):
    ser_1.flushInput()  # flush input buffer, discarding all its contents
    ser_2.flushInput()  # flush input buffer, discarding all its contents
    ser_1.flushOutput()  # flush output buffer, aborting current output
    ser_2.flushOutput()  # flush output buffer, aborting current output
    if ser_1.isOpen() and ser_2.isOpen():
        i = 0
        for frame in binary_message:
            try:
                # and discard all that is in buffer

                # write data
                ser_1.write(frame)
                #print('WRITE', i, datetime.datetime.now())
                ser_1.flush()
                # print("write data: Hello")
                #time.sleep(0.0005)  # give the serial port sometime to receive the data
                i = i +1
            except Exception as e1:
                print("error communicating write...: " + str(e1))
    else:
        print("cannot open serial port ")


def ser_read():
    global priem
    global frames
    if ser_1.isOpen() and ser_2.isOpen():
        number_lines = 0
        #while True:
            #if ser_2.in_waiting:
        #try:
        if ser_2.in_waiting == 0 and priem == 1:
            priem = 0
            channel.receive(frames)
            frames = []
        while ser_2.in_waiting > 0:
            if priem == 0:
                priem = 1
            #print('in_waiting', ser_2.in_waiting)
            while ser_2.in_waiting >= 238:
                response = ser_2.read(238)
                #time.sleep(0.4)
                #print('READ', ser_2.in_waiting, datetime.datetime.now())
                frames.append(response)
            #frames.append(ser_2.read(238))
            #ser_2.flushInput()
            #ser_2.flushOutput()
            #print("read data: " + response)
            # print(sys.stdout.write(response.decode()))
            """if response:
                # ser_1.close()
                # ser_2.close()
                return response"""
            number_lines = number_lines + 1
            """if number_lines == 3:
                break"""

        #if len(frames) == 0:
            #print('empty buffer')
        #except Exception as e2:
            #print("error communicating read...: " + str(e2))
    else:
        print("cannot open serial port ")
    threading.Timer(0.0001, ser_read).start()
    #TODO спячка



# ser_open()
#ser_write("Hello")
#message = ser_read()
#print(message)
# print([comport.device for comport in serial.tools.list_ports.comports()])
# list_ports.comports()  # Outputs list of available serial ports
# print(list(serial.tools.list_ports.comports()))
# list = serial.tools.list_ports.comports()
# connected = []
# for element in list:
#    connected.append(element.device)
#    print("Connected COM ports: " + str(connected))
# def exec_every_n_seconds(n, f):
#    first_called = datetime.now()
#   f()
#   num_calls = 1
#   drift = timedelta()
#   time_period = timedelta(seconds=n)
#   while 1:
#       time.sleep(n - drift.microseconds / 1000000.0)
#      current_time = datetime.now()
#       f()
#       num_calls += 1
#       difference = current_time - first_called
#       drift = difference - time_period * num_calls
#       print("drift=", drift)


#ser_open()
#ser_read()
#ser_write(channel.send("хуй"))


def foo():
    if not (ser_1.isOpen() and ser_2.isOpen()):
        print('Выхожу')
        # ser_open()
    print(datetime.datetime.now())
    threading.Timer(3, foo).start()



