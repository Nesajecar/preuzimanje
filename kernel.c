#include "terminal.h"
#include "keyboard.h"

// Buffer za unos
#define INPUT_BUFFER_SIZE 256
static char input_buffer[INPUT_BUFFER_SIZE];
static size_t input_index = 0;

// Deklaracija start funkcije
void kernel_main(void) {
    // Inicijalizuj terminal
    terminal_initialize();
    terminal_writestring("Mali OS - Unesite tekst i pritisnite Enter\n");
    terminal_writestring("> ");
    
    // Inicijalizuj tastaturu
    keyboard_init();
    
    // Glavna petlja
    while (1) {
        char c = keyboard_getchar();
        
        if (c != 0) {
            if (c == '\n' || c == '\r') {
                // Enter pritisnut - ispiši unos
                if (input_index > 0) {
                    input_buffer[input_index] = '\0';
                    terminal_newline();
                    terminal_writestring("Ispis: ");
                    terminal_writestring(input_buffer);
                    terminal_newline();
                    terminal_newline();
                    
                    // Resetuj buffer
                    input_index = 0;
                    terminal_writestring("> ");
                } else {
                    terminal_newline();
                    terminal_writestring("> ");
                }
            } else if (c == '\b') {
                // Backspace
                if (input_index > 0) {
                    input_index--;
                    terminal_backspace();
                }
            } else {
                // Dodaj karakter u buffer i prikaži ga
                if (input_index < INPUT_BUFFER_SIZE - 1) {
                    input_buffer[input_index++] = c;
                    terminal_putchar(c);
                }
            }
        }
    }
}

