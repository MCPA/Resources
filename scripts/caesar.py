import sys,string,socket,time,logging,argparse

symbols = 'abcdefghijklmnopqrstuvwxyz'
port = 12345
host = '192.168.239.128'

def rot(*symbols):
    def _rot(n):
        encoded = ''.join(sy[n:] + sy[:n] for sy in symbols)
        lookup = string.maketrans(''.join(symbols), encoded)
        return lambda s: s.translate(lookup)
    return _rot

def encrypt(k,plaintext):
    cipher = ''
    caesar_encode = rot(symbols)(k)
    cipher = caesar_encode(plaintext)

    logging.info('Your encrypted message is: ' + str(cipher))

def decrypt(k,cipher):
    caesar_decode = rot(symbols)(26-k)
    return caesar_decode(cipher)

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

def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
                '-H', '--host',type=str, help='IP Address', required = True)
        parser.add_argument(
                '-p', '--port',type=int, help='TCP Port', required = True)
        sp = parser.add_subparsers(dest='subparser_name')

        # create the parser for the "d" command
        parser_d = sp.add_parser('d', help = 'd help')
        parser_d.add_argument('decrypt', help='Decrypt', action='store_true')
        parser_d.set_defaults(func=decrypt)

        # create the parser for the "e" command
        parser_e = sp.add_parser('e', help = 'e help')
        parser_e.add_argument('encrypt', help='Encrypt', action='store_true')
        parser_d.set_defaults(func=encrypt)

        args = parser.parse_args()
    except argparse.ArgumentError as err:
        print str(err)
        sys.exit(2)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip = socket.gethostbyname(host)
        sock.connect((ip, int(port)))
        
    except socket.error, msg:
        logging.info('Error trying to connect.')
        sys.exit()

    response = read(sock)
    cipher = response[198:237]
    print(response)

    plaintext = ''
    for i in range(1,26):
        plaintext = decrypt(int(i),cipher)
        if ("the" in plaintext):
            print plaintext
            sock.sendall(plaintext)
            print read(sock)

if __name__ == "__main__":
    main()
