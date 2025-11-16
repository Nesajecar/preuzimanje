# Makefile za mali OS

ASM = nasm
CC = gcc
LD = ld

ASMFLAGS = -f elf32
CFLAGS = -m32 -ffreestanding -O2 -Wall -Wextra -fno-pic -fno-stack-protector
LDFLAGS = -m elf_i386 -T linker.ld

# Fajlovi
BOOTLOADER = boot.bin
KERNEL_OBJ = start.o kernel.o terminal.o keyboard.o
KERNEL_BIN = kernel.bin
OS_IMAGE = os.img

# Pravila
all: $(OS_IMAGE)

$(OS_IMAGE): $(BOOTLOADER) $(KERNEL_BIN)
	dd if=/dev/zero of=$(OS_IMAGE) bs=1024 count=1440
	dd if=$(BOOTLOADER) of=$(OS_IMAGE) conv=notrunc
	dd if=$(KERNEL_BIN) of=$(OS_IMAGE) seek=1 conv=notrunc

$(BOOTLOADER): boot.asm
	$(ASM) -f bin boot.asm -o $(BOOTLOADER)

$(KERNEL_BIN): $(KERNEL_OBJ)
	$(LD) $(LDFLAGS) -o $(KERNEL_BIN) $(KERNEL_OBJ)

start.o: start.s
	$(ASM) $(ASMFLAGS) start.s -o start.o

kernel.o: kernel.c terminal.h keyboard.h io.h
	$(CC) $(CFLAGS) -c kernel.c -o kernel.o

terminal.o: terminal.c terminal.h io.h
	$(CC) $(CFLAGS) -c terminal.c -o terminal.o

keyboard.o: keyboard.c keyboard.h io.h
	$(CC) $(CFLAGS) -c keyboard.c -o keyboard.o

clean:
	rm -f *.o *.bin *.img

run: $(OS_IMAGE)
	qemu-system-i386 -drive file=$(OS_IMAGE),format=raw,index=0,if=floppy

.PHONY: all clean run

