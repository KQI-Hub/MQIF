# MQIF - Mari's QOI-Like Interchange Format

MQIF is a simple format based on GIF and QOI, made mostly as an experiment to see how viable scQOI is for general images.

Currently the implementation lacks support for multiple images per file / animation and transparency. I'll release a proper spec later.

MQIF File structure:
```
---- Head ----
"QIF26a" - Magic
uint16 - Width
uint16 - Height
uint8 - Color Table Size
uint8 - Transparency Toggle (Sets Index 0 transparent)
---- Color Table ----
(uint8, uint8, uint8) - Color Tuplet
(uint8, uint8, uint8) - Color Tuplet
etc...
---- Frame ----
uint8 - Disposal Mode, 0 is replace, 1 is overlay/combine.
uint16 - Frame Delta, in Miliseconds. 0 means no delay.
uint32 - Frame scQOI Payload Size
scQOI-compressed stream of color indexes
---- EOF ----
00 00 00 00 00 00 00 3B hex literal
```

Note: MQIF was previously called QIF, until I found out about the Quicken Interchange Format.
