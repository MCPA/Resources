import sys,string,socket,pexpect,time,logging

symbols = 'abcdefghijklmnopqrstuvwxyz'

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
    plaintext = ''
    caesar_decode = rot(symbols)(26-k)
    plaintext = caesar_decode(cipher)

    logging.info('Key: '+str(k)+'Message: ' + plaintext)

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

def main(argv):
    logging.basicConfig(filename='caesar.log', level=logging.INFO)
    port = 12345
    host = '192.168.239.128'
    if (len(sys.argv) != 3):
        sys.exit('Usage: caesar.py <k> <mode>')

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip = socket.gethostbyname(host)
        sock.connect((ip, int(port)))
        
    except socket.error, msg:
        logging.info('Error trying to connect.')
        sys.exit()

    cipher = read(sock)[198:]
    logging.info('Cipher = ' + cipher)

    if sys.argv[2] == 'e':
        encrypt(int(sys.argv[1]))
    elif sys.argv[2] == 'd':
        plaintext = raw_input('Enter plain text message: ')
        decrypt(int(sys.argv[1]),plaintext)
    elif sys.argv[2] == 'da':
        for i in range(1,26):
            decrypt(int(i),cipher)
    else:
        sys.exit('Error in mode type')

if __name__ == "__main__":
    main(sys.argv[1:])
