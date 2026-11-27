// Box.asm
// Khushi, K = 77
// start row = 77, 20 rows tall
// width = 16 * ((77 mod 4) + 1) = 32 pixels = 2 words
// start address = SCREEN + 32*77 = 16384 + 2464 = 18848

(LOOP)
    @KBD
    D=M
    @PRESSED
    D;JNE           // key pressed -> go black

    @color
    M=0             // no key -> white (erases the box)
    @DRAW
    0;JMP

(PRESSED)
    @color
    M=-1            // black

(DRAW)
    @18848
    D=A
    @addr
    M=D             // addr = first word of the box
    @20
    D=A
    @rows
    M=D             // rows left = 20

(ROWLOOP)
    @color
    D=M
    @addr
    A=M
    M=D             // first word of this row
    A=A+1
    M=D             // second word of this row

    @32
    D=A
    @addr
    M=D+M           // next row (+32 words)

    @rows
    M=M-1
    D=M
    @ROWLOOP
    D;JGT

    @LOOP
    0;JMP
