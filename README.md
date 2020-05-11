# CHIP-8 Disassembler written in Python.
**This dis-assembler is based on CHIP-8 instructions listed at Cowgod's Technical Reference.**
http://devernay.free.fr/hacks/chip8/C8TECH10.HTM 

Works on Python 2.7/3

----

## Usage:
```
USAGE: disassembler.py ROM_PATH <MODE>
```

----

## Script can dis-assemble the binary in the below three modes.
### Normal Mode(Default mode 0)
All the instructions are dis-assembled normally.

### Example
```
ROM given: roms/TEST
-I- Number of bytes: 478

JP 0x24E
SKNP VA
LD I, 0xAEA
RND VE, 0xAA
LD I, 0xAAE
SKNP V0
LD I, 0x0E0
RND V0, 0x40
SNE V0, 0xE0
SKNP V0
RND V0, 0xE0
SKNP V0
CALL 0x0E0
LD I, 0x0E0
CALL 0x020
LD V0, 0x40
CALL 0x040
........
........
```
### Dis-assemble with bytes offset(1)
Byte offset at which each opcode is present is also printed with decoded instructions.

### Example
```
ROM given: roms/TEST, Mode: disassemble_binary_with_byte_offset
-I- Number of bytes: 0x1DE(478)

0x00	JP 0x24E
0x02	SKNP VA
0x04	LD I, 0xAEA
0x06	RND VE, 0xAA
0x08	LD I, 0xAAE
0x0A	SKNP V0
0x0C	LD I, 0x0E0
0x0E	RND V0, 0x40
0x10	SNE V0, 0xE0
0x12	SKNP V0
0x14	RND V0, 0xE0
0x16	SKNP V0
0x18	CALL 0x0E0
0x1A	LD I, 0x0E0
0x1C	CALL 0x020
.................
.................
```

### Dis-assemble with address offset(2)
Address at which the opcode will be stored is also printed with decoded instructions.
Program is stored on CHIP-8 memory starting at address 512(0x200). Refer this excellent [guide](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM) for more info.

### Example
```
ROM given: roms/TEST, Mode: disassemble_binary_with_address_offset
-I- Number of bytes: 0x1DE(478)

0x200	JP 0x24E
0x202	SKNP VA
0x204	LD I, 0xAEA
0x206	RND VE, 0xAA
0x208	LD I, 0xAAE
0x20A	SKNP V0
0x20C	LD I, 0x0E0
0x20E	RND V0, 0x40
0x210	SNE V0, 0xE0
0x212	SKNP V0
0x214	RND V0, 0xE0
0x216	SKNP V0
0x218	CALL 0x0E0
0x21A	LD I, 0x0E0
0x21C	CALL 0x020
0x21E	LD V0, 0x40
0x220	CALL 0x040

```

## Note:
I have not included any ROMS in the repository. But, a simple google search might help you to get the roms.

## License
MIT License

