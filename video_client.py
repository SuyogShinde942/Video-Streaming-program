import socket,cv2, pickle,struct

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #Creating a socke
host_ip = '192.168.0.106' # Video_server_IP
port = 9999               # Video_server_Port

#Connecting to server
client_socket.connect((host_ip,port)) 

#Sending an empty message
data = b""

#Return the size of struct (and hence of the bytes produced by pack corresponding to the format string format)
payload_size = struct.calcsize("Q")
while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4*1024) #Reading 4*1024
        if not packet: break
        data+=packet
    packed_msg_size = data[:payload_size] #limiting the payload
    data = data[payload_size:]
    msg_size = struct.unpack("Q",packed_msg_size)[0]
    
    while len(data) < msg_size:
        data += client_socket.recv(4*1024)
    frame_data = data[:msg_size]
    data  = data[msg_size:]
    frame = pickle.loads(frame_data)
    cv2.imshow("CLIENT",frame)
    key = cv2.waitKey(1) & 0xFF
    if key  == ord('q'): #Pressing "q" is quit the program
        break
client_socket.close()
