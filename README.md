# Mali OS za QEMU

Jednostavan operativni sistem sa podrškom za tastaturu i ispis teksta.

## Funkcionalnosti

- Bootloader koji učitava kernel
- Terminal sa tekstualnim ispisom
- Podrška za tastaturu
- Kada se pritisne Enter, ispisuje se samo uneseni tekst

## Zahtevi

- NASM (Netwide Assembler)
- GCC sa 32-bit podrškom
- QEMU emulator
- Make

### Instalacija na Ubuntu/Debian:
```bash
sudo apt-get install nasm gcc-multilib qemu-system-x86 make
```

### Instalacija na Windows:
- NASM: https://www.nasm.us/
- MinGW-w64 sa 32-bit podrškom
- QEMU: https://www.qemu.org/download/

## Build

```bash
make
```

Ovo će kreirati `os.img` fajl koji se može pokrenuti u QEMU.

## Pokretanje u QEMU

```bash
make run
```

Ili ručno:
```bash
qemu-system-i386 -drive file=os.img,format=raw,index=0,if=floppy
```

## Korišćenje

1. Pokrenite OS u QEMU
2. Unesite tekst koristeći tastaturu
3. Pritisnite Enter da ispišete uneseni tekst
4. Koristite Backspace za brisanje karaktera

## Struktura projekta

- `boot.asm` - Bootloader koji učitava kernel
- `kernel.c` - Glavni kernel kod
- `terminal.c/h` - Terminal i VGA funkcije
- `keyboard.c/h` - Tastatura input handling
- `io.h` - I/O port funkcije
- `linker.ld` - Linker skript
- `Makefile` - Build skript

## Napomene

- OS radi u 32-bit zaštićenom modu
- Koristi VGA tekstualni mod (80x25)
- Tastatura podrška je osnovna (QWERTY layout)
- Nema podršku za Shift, Caps Lock, itd.

