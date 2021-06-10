import socket, cv2, pickle,struct

# Creating Socket
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
port = 9999      # Port assing to the connection
socket_address = ('192.168.0.106',port)         

#Binding the IP and PORT of the servers
server_socket.bind(socket_address)

# Socket Listening
server_socket.listen(5)
print("Listening at:---->>>",socket_address)

# Socket Accept
while True:
    client_socket,addr = server_socket.accept()
    if client_socket:
        vid = cv2.VideoCapture(0)
        while(vid.isOpened()):
            img,frame = vid.read() 
            a = pickle.dumps(frame)  #Serialize the frame in bytes
            message = struct.pack("Q",len(a))+a  #pack the message
            client_socket.sendall(message) #sending the message to client
            
            cv2.imshow('Sending Video',frame)  #Showing Video
            key = cv2.waitKey(1) & 0xFF  
            if key ==ord('q'): #Pressing "q" in the cliet side will end the call
                client_socket.close()