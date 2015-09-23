import sys,socket,time,argparse
import caesar,transposition

def read(s):
    s.setblocking(0)
    recv_buf = ''
    data = []
    timeout = 1
              
    begin=time.time()
    while 1:
        if data and time.time()-begin > timeout:
            break
        elif time.time()-begin > timeout*2:
            break
        try:
            recv_buf = s.recv(1024)
            if recv_buf:
                data.append(recv_buf)
                begin = time.time()
            else:
                time.sleep(0.25)
        except:
            pass
    return ''.join(data)  

def connect(host,port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip = socket.gethostbyname(host)
        sock.connect((ip, int(port)))
        return sock
        
    except socket.error, msg:
        print str('Error trying to connect.')

def main():
    try:
        parser = argparse.ArgumentParser()

        # Host and Port arguments required to connect to remote host
        parser.add_argument(
                '-H', '--host',type=str, help='IP Address', required = True)
        parser.add_argument(
                '-p', '--port',type=int, help='TCP Port', required = True)

        args = parser.parse_args()
    except argparse.ArgumentError as err:
        print str(err)
        sys.exit(2)

    sock = connect(args.host, args.port)

    # Stage 1
    # read socket data, split on newlines into a list, remove empty lines, and split on ":" character
    data = read(sock)
#    print data
    response = [line.strip().split(':') for line in data.split('\n') if line.strip()]
    match = [c for c in response if "psifer text" in c]
    cipher = match[0][1].strip()
    print("Stage 1::Cipher: %s" % cipher)
    answer = caesar.brute_force(cipher,1,26,["the"]).split(' ')
    print("Stage 1::Plaintext: %s" % answer)
    sock.sendall(answer[6] + '\n')

    # Stage 2
    data = read(sock)
    response = [line.strip().split(':') for line in data.split('\n') if line.strip()]
    match = [c for c in response if "psifer text" in c]
    cipher = match[0][1].strip()
    print("Stage 2::Cipher: %s" % cipher)
    plaintext = transposition.decipher(cipher)
    print("Stage 2::Plaintext: %s" % plaintext)
    answer = plaintext.split('"')[1::2][0]
    sock.sendall(answer + '\n')

    #Stage 3
    data = read(sock)
    print data



if __name__ == "__main__":
    main()
