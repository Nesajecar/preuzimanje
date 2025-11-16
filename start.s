; Start funkcija koja poziva kernel_main
global start
extern kernel_main

start:
    call kernel_main
    hlt

