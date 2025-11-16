#include "keyboard.h"
#include "io.h"

static bool key_pressed = false;
static uint8_t last_scancode = 0;

void keyboard_init(void) {
    // Reset keyboard
    outb(KEYBOARD_STATUS_PORT, 0xAE);
}

bool keyboard_is_key_pressed(void) {
    // Proveri da li postoji podatak za čitanje
    uint8_t status = inb(KEYBOARD_STATUS_PORT);
    return (status & 0x01) != 0;
}

char keyboard_getchar(void) {
    if (!keyboard_is_key_pressed()) {
        return 0;
    }
    
    uint8_t scancode = inb(KEYBOARD_DATA_PORT);
    
    // Ignoriši key release (scancode > 0x80)
    if (scancode > 0x80) {
        return 0;
    }
    
    // Konvertuj scancode u ASCII
    if (scancode < 128 && keyboard_map[scancode] != 0) {
        return keyboard_map[scancode];
    }
    
    return 0;
}

