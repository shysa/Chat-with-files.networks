import random


def send(text, file=False, file_name=None):
# ------------ splitting on frames
    if not file:
        text = text.encode('utf-8')
    frame_amount = len(text) // 128
    last_frame_len = len(text) % 128 - 1
    data_len = 127
    if frame_amount == 0:
        data_len = last_frame_len
    if last_frame_len < 0:
        frame_amount = frame_amount - 1
        last_frame_len = 127
    message_id = random.randint(1, 63)
    #print(hex(message_id+192))
    if file:
        frame_amount = frame_amount + 1
        data_len = 255
        file_name = bytes(file_name, encoding='utf-8')
        prim_frame = bytes([message_id + 192, frame_amount // 65536, frame_amount % 65536 // 256, frame_amount % 256, data_len]) + file_name
        prim_frame = prim_frame + bytes([ord(')') for i in range(128-len(file_name))])
        data_len = 127
        text = bytes([0 for i in range(128)]) + text
    else:
        prim_frame = bytes([message_id + 192, frame_amount // 65536, frame_amount % 65536 // 256, frame_amount % 256, data_len]) + text[:128]


    frames = []
    frames.append(prim_frame)
    for i in range(frame_amount):
        text = text[128:]
        if i == frame_amount-1:
            data_len = last_frame_len
        frames.append(bytes([message_id, i // 65536, i % 65536 // 256, i % 256, data_len]) + text[:128])
    frames[len(frames)-1] = frames[len(frames)-1] + bytes([ord(')') for i in range(133-len(frames[len(frames)-1]))])

# ------------ encoding [4,7]
    frames_encoded = []
    for frame in frames:
        encoding1 = frame
        #print('encoding1', encoding1, len(encoding1))
        frame_encoded = bytes([])                           # encoding1 - hole frame    [1 и 2 в названия х переменных - уровни фрагментации]
        while len(encoding1) > 0:
            if len(encoding1) > 3:
                encoding2 = int.from_bytes(encoding1[len(encoding1)-4:], byteorder='big')   # encoding2 - 4 bytes
                encoding1 = encoding1[:len(encoding1)-4]
            else:
                encoding2 = int.from_bytes(encoding1, byteorder='big')  # encoding2 - 4 bytes
                encoding1 = ''
            mask = 15
            #print('encoding1', encoding1, len(encoding1))
            encoded2 = 0
            for i in range(8):                                              # encoding each 4 bits of 4 bytes
                input_vect = ((encoding2 & mask) >> (i * 4)) << 3
                encoded_vect = input_vect
                generating_vect = 11
                tail = 8
                while input_vect >= 8:
                    while tail << 1 < input_vect:
                        tail = tail << 1
                        generating_vect = generating_vect << 1
                    input_vect = input_vect ^ generating_vect
                    tail = 8
                    generating_vect = 11
                encoded2 = encoded2 + ((encoded_vect + input_vect) << (i * 7))       # 4 bits encoded to 7 bits
                mask = mask << 4
            frame_encoded = bytes(encoded2.to_bytes(7,  byteorder='big')) + frame_encoded
        frames_encoded.append(frame_encoded)
    i = 0
    """for frame in frames_encoded:
        i = i + len(frame)
    print('total send', i, ', frames:', len(frames_encoded))
    print('send', frames_encoded[0])"""
    return frames_encoded


def receive(frames_encoded):
    check_table = {
        1: 0,
        2: 1,
        3: 3,
        4: 2,
        5: 6,
        6: 4,
        7: 5
    }
    frames = []

    #print('rec',len(frames_encoded))

    if not isinstance(frames_encoded, list):
        return
    #leng = 0
    for frame_encoded in frames_encoded:
        #leng = len(frame_encoded) + leng

        decoding1 = frame_encoded
        frame = bytes([])                                                                   # decoding1 - hole frame
        while len(decoding1) > 0:
            decoding2 = int.from_bytes(decoding1[len(decoding1) - 7:], byteorder='big')     # decoding2 - 7 bytes
            decoding1 = decoding1[:len(decoding1) - 7]
            mask = 127
            decoded2 = 0
            for i in range(8):                                      # encoding each 4 bits of 4 bytes
                input_vect = (decoding2 & mask) >> (i * 7)
                decoded_vect = input_vect
                generating_vect = 11
                tail = 8
                while input_vect >= 8:
                    while tail << 1 < input_vect:
                        tail = tail << 1
                        generating_vect = generating_vect << 1
                    input_vect = input_vect ^ generating_vect
                    tail = 8
                    generating_vect = 11
                if input_vect != 0:
                    decoded_vect = decoded_vect ^ (1 << check_table[input_vect])
                mask = mask << 7
                decoded2 = decoded2 + ((decoded_vect >> 3) << (i * 4))
            frame = bytes(decoded2.to_bytes(4, byteorder='big')) + frame
        #print(frame)
        while frame[0] == 0:
            frame = frame[1:]
        frames.append(frame)
    #print(len(frames[0]))
    #print('total length', leng, 'bytes', ', frames:', len(frames_encoded))
    """for frame in frames:
        print('rec', frame)"""
    #frames[0] = frames[0][3:]           # KOSTYL!!!!!!!!!!!!!!!!!!!111

    message_id = 0
    frame_amount = 0
    prim_frame = None
    isFile = False

    #print(frames[0])
    for frame in frames:            # finding primary frame
        if frame[0] > 63:
            message_id = frame[0] & 63
            frame_amount = frame[1] * 65536 + frame[2] * 256 + frame[3]
            prim_frame = frames.index(frame)
            if frames[prim_frame][4] > 127:
                isFile = True
            break
    if isFile:
        file_name = frames[prim_frame][5:frames[prim_frame][4]+6].decode()
        text = bytes([])
    else:
        text = frames[prim_frame][5:frames[prim_frame][4]+6]
    for i in range(frame_amount):
        text = text + frames[i + 1][5:frames[i + 1][4]+6]
    if not isFile:
        text = text.decode()
        print(text)
    if isFile:
        receive_file(text, file_name)
    #threading.Timer(0.1, receive(phizical.ser_read())).start()
    return text


def send_file(file):
    f = open(file, 'rb')
    data = f.read()
    f.close()
    file_name = file[file.rfind("\\")+1:]
    #print(file_name)
    return send(data, True, file_name)


def receive_file(data, file_name):
    file_name = file_name[:file_name.find(')')]
    print('received file:', file_name)
    f = open('downloads\\' + file_name, 'wb')
    f.write(data)
    f.close()
    return file_name


def send_nudes(nudes):
    pass


#receive(send_file(r'C:\Users\Ilya\Downloads\VID_20200428_120510.mp4'))
#receive(send('Белоусов-Попов_ф3.jpg'))

#thread1 = threading.Thread(target=receive(phizical.ser_read()))
#thread2 = threading.Thread(target=phizical.ser_write(send_file(r"C:\Users\Ilya\Documents\!University\networks\kursach\Chat-with-files.networks-master\client.py")))
#thread2.start()
#thread1.start()
#thread2.join()
#thread1.join()
