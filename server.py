class Socket:
  def __init__(self, config):
    # create an incominn socket
    signal.signal(signal.SIGINT, self.shutdown)
    self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.serverSocket.bind((config['HOST_NAME'], config['BIND_PORT']))
    self.serverSocket.listen(10)
    self.__clients = {}
    
    # accepting clients and processes
    while True:
      (clientSocket, client_address) = self.serverSocket.accept() 
      d = threading.Thread(name=self._getClientName(client_address), 
      target = self.proxy_thread, args=(clientSocket, client_address))
      d.setDaemon(True)
      d.start()
      
    # redirect the traffic
    request = conn.recv(config['MAX_REQUEST_LEN']) 
    first_line = request.split('\n')[0]
    url = first_line.split(' ')[1]
    
    
  http_pos = url.find("://") # find pos of ://
  if (http_pos==-1):
      temp = url
  else:
      temp = url[(http_pos+3):] 
  port_pos = temp.find(":") 

  # find end of web server
  webserver_pos = temp.find("/")
  if webserver_pos == -1:
      webserver_pos = len(temp)

  webserver = ""
  port = -1
  if (port_pos==-1 or webserver_pos < port_pos): 
      port = 80 
      webserver = temp[:webserver_pos] 
  else: # specific port 
      port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
      webserver = temp[:port_pos] 
      
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
  s.settimeout(config['CONNECTION_TIMEOUT'])
  s.connect((webserver, port))
  s.sendall(request)
  
  while 1:
    # receive data from web server
    data = s.recv(config['MAX_REQUEST_LEN'])
    if (len(data) > 0):
        conn.send(data) # send to browser/client
    else:
        break
