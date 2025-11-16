ENTRY(start)

SECTIONS
{
    . = 0x1000;
    
    .text : ALIGN(4) {
        *(.text)
    }
    
    .rodata : {
        *(.rodata)
    }
    
    .data : {
        *(.data)
    }
    
    .bss : {
        *(.bss)
    }
}

