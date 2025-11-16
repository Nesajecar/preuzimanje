; Bootloader za mali OS
bits 16
org 0x7c00

start:
    ; Postavi segment registre
    cli
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7c00
    
    ; Postavi video mod na 80x25 tekstualni mod
    mov ax, 0x0003
    int 0x10
    
    ; Učitaj kernel sa diska
    mov si, msg_loading
    call print_string
    
    ; Učitaj kernel (pretpostavljamo da je na sektoru 2)
    mov ah, 0x02
    mov al, 4        ; Broj sektora
    mov ch, 0        ; Cilindar
    mov cl, 2        ; Sektor
    mov dh, 0        ; Glava
    mov dl, 0x00     ; Disk (floppy u QEMU)
    mov bx, 0x1000   ; Gde učitati
    int 0x13
    
    ; Proveri grešku
    jc error
    
    ; Prebaci u zaštićeni mod
    cli
    lgdt [gdt_descriptor]
    
    ; Omogući zaštićeni mod
    mov eax, cr0
    or eax, 1
    mov cr0, eax
    
    ; Skoči u 32-bitni kod
    jmp CODE_SEG:start_protected

print_string:
    pusha
    mov ah, 0x0e
.loop:
    lodsb
    cmp al, 0
    je .done
    int 0x10
    jmp .loop
.done:
    popa
    ret

error:
    mov si, msg_error
    call print_string
    hlt

msg_loading db 'Loading OS...', 13, 10, 0
msg_error db 'Error loading kernel!', 13, 10, 0

; GDT (Global Descriptor Table)
gdt_start:
    ; Null descriptor
    dd 0x0
    dd 0x0
    
    ; Code segment
gdt_code:
    dw 0xffff       ; Limit (bits 0-15)
    dw 0x0          ; Base (bits 0-15)
    db 0x0          ; Base (bits 16-23)
    db 10011010b    ; Access byte
    db 11001111b    ; Flags + Limit (bits 16-19)
    db 0x0          ; Base (bits 24-31)
    
    ; Data segment
gdt_data:
    dw 0xffff
    dw 0x0
    db 0x0
    db 10010010b
    db 11001111b
    db 0x0

gdt_end:

gdt_descriptor:
    dw gdt_end - gdt_start - 1
    dd gdt_start

CODE_SEG equ gdt_code - gdt_start
DATA_SEG equ gdt_data - gdt_start

; Padding do 510 bajtova
times 510-($-$$) db 0
dw 0xaa55

; 32-bitni zaštićeni mod
bits 32
start_protected:
    mov ax, DATA_SEG
    mov ds, ax
    mov ss, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    
    ; Postavi stack
    mov ebp, 0x90000
    mov esp, ebp
    
    ; Skoči na kernel
    jmp 0x1000

