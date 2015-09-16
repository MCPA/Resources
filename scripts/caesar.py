import sys,string,socket,time,argparse

# 'abcdefghijklmnopqrstuvwxyz'
symbols = string.ascii_lowercase

def rot(*symbols):
    def _rot(n):
        encoded = ''.join(sy[n:] + sy[:n] for sy in symbols)
        lookup = string.maketrans(''.join(symbols), encoded)
        return lambda s: s.translate(lookup)
    return _rot

def encrypt(k,plaintext):
    return rot(symbols)(k)(plaintext)

def decrypt(k,cipher):
    return rot(symbols)(26-k)(cipher)

def brute_force(cipher):
    plaintext = ''
    for i in range(1,26):
        plaintext = decrypt(int(i),cipher)
        if ("the" in plaintext):
            answer = plaintext.split()[6]
    return answer

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
        sp = parser.add_subparsers(dest='subparser_name')

        # create the parser for the "decrypt" command
        parser_d = sp.add_parser('d', help = 'd help')
        parser_d.add_argument('decrypt', help='Decrypt', action='store_true')
        parser_d.set_defaults(func=decrypt)

        # create the parser for the "encrypt" command
        parser_e = sp.add_parser('e', help = 'e help')
        parser_e.add_argument('encrypt', help='Encrypt', action='store_true')
        parser_e.set_defaults(func=encrypt)

        args = parser.parse_args()
    except argparse.ArgumentError as err:
        print str(err)
        sys.exit(2)

    sock = connect(args.host, args.port)

    # Stage 1
    # read socket data, split on newlines into a list, remove empty lines, and split on ":" character
    response = [line.strip().split(':') for line in read(sock).split('\n') if line.strip()]
    match = [c for c in response if "psifer text" in c]
    cipher = match[0][1].strip()
    answer = brute_force(cipher)
    sock.sendall(answer)
    response = read(sock)
    print(response)

    # Stage 2
    print read(sock)
    #response = [line.strip().split(':') for line in read(sock).split('\n') if line.strip()]
    #match = [c for c in response if "psifer text" in c]
    #print match
    #cipher = match[0][1].strip()


if __name__ == "__main__":
    main()
