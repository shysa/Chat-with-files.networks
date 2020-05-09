# !/usr/bin/python


#import serial.tools.list_ports
import datetime
import threading
import time
import serial
import channel
# import ft_serial_1
import utils.parser
#from serial.tools import list_ports

# initialization and open the port

# possible timeout values:
#    1. None: wait forever, block call
#    2. 0: non-blocking mode, return immediately
#    3. x, x is bigger than 0, float allowed, timeout block call


"""ser_1 = serial.Serial()
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
ser_1.writeTimeout = None  # timeout for write"""

ser_1 = serial.Serial()


def portinit(com=utils.parser.get_port_parameters()):
    # ser.port = "/dev/ttyUSB0"
    # ser.port = "/dev/ttyS2"
    ser_1.baudrate = com[2]
    ser_1.bytesize = serial.EIGHTBITS  # number of bits per bytes
    ser_1.parity = serial.PARITY_NONE  # set parity check: no parity
    ser_1.stopbits = serial.STOPBITS_ONE  # number of stop bits
    # ser.timeout = None          #block read
    ser_1.timeout = 1  # non-block read
    # ser.timeout = 2              #timeout block read
    # ser_2.xonxoff = False  # disable software flow control
    # ser_2.rtscts = False  # disable hardware (RTS/CTS) flow control
    # ser_2.dsrdtr = False  # disable hardware (DSR/DTR) flow control
    ser_1.writeTimeout = 20  # timeout for write
    try:
        ser_1.port = com[0]
        ser_1.open()
        ser_1.close()
    except:
        ser_1.port = com[1]


priem = 0
read_delay = 0.5
frames = []


def ser_open():
    portinit()
    try:
        ser_1.open()
    except Exception as e:
        print("error open serial port: " + str(e))
        exit()


def ser_write(binary_message):
    ser_1.flushInput()  # flush input buffer, discarding all its contents
    ser_1.flushOutput()  # flush output buffer, aborting current output
    if ser_1.isOpen():
        i = 0
        for frame in binary_message:
            try:
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


def ser_read(ser=ser_1):
    global priem
    global frames
    global read_delay
    if ser.isOpen():
        if ser.in_waiting == 0 and priem == 1:
            priem = 0
            read_delay = 0.5
            channel.receive(frames)
            frames = []
        while ser.in_waiting > 0:
            if priem == 0:
                priem = 1
                read_delay = 0.0001
            #print('in_waiting', ser_2.in_waiting)
            while ser.in_waiting >= 238:
                response = ser.read(238)
                #print('READ', ser_2.in_waiting, datetime.datetime.now())
                frames.append(response)
    else:
        print("cannot open serial port ")
        return 1
    threading.Timer(read_delay, ser_read).start()


"""ser_open()
ser_read()
while True:
    ser_write(channel.send(input()))"""
#ser_write(channel.send_file(r"C:\Users\Ilya\Downloads\zheltogolovyj_amazon_popugaj_ptitsa_133941_3840x2400.jpg"))
