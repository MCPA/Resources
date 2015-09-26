#!/bin/python

def decipher(msg):
    for j in range(2, len(msg)):

        dec_msg = ['0'] * len(msg)
        idec_msg, shift = 0, 0

        for i in range(len(msg)):
            dec_msg[idec_msg] = msg[i]
            idec_msg += j

            if idec_msg > len(msg) - 1:
                shift += 1
                idec_msg = shift
        dec_msg = "".join(dec_msg)

        if "you" not in dec_msg: continue
        return dec_msg

def decipher2(ciphertext):
    length = len(ciphertext)
    width_list = []
    # width values that divide evenly into
    # the length of the ciphertext
    for i in range(1,length/4):
        # if there is no remainder from division
        width_list.append(i)
    for width in width_list:
        plaintext = [''] * width
        for column in range(width):
            pointer = column
            while pointer < length:
                plaintext[column] += ciphertext[pointer]
                pointer += width
#        print "Width: {0}, Plaintext: {1}".format(width,plaintext)
        plaintext = ''.join(plaintext)
        if "problem" not in plaintext: continue
        return plaintext



#cipher = open('string.txt','r').readline().rstrip()
#print decipher2(cipher)
