__author__ = 'jaya'

# External Imports
import sys

MODE = {
    0: 'disassemble_binary',
    1: 'disassemble_binary_with_byte_offset',
    2: 'disassemble_binary_with_address_offset'
}

def disassemble_binary(binary):
    """
    Disassemble binary based on below instructions.
    Standard Chip-8 Instructions
    Taken from: http://devernay.free.fr/hacks/chip8/C8TECH10.HTM
    00E0 - CLS
    00EE - RET
    0nnn - SYS addr
    1nnn - JP addr
    2nnn - CALL addr
    3xkk - SE Vx, byte
    4xkk - SNE Vx, byte
    5xy0 - SE Vx, Vy
    6xkk - LD Vx, byte
    7xkk - ADD Vx, byte
    8xy0 - LD Vx, Vy
    8xy1 - OR Vx, Vy
    8xy2 - AND Vx, Vy
    8xy3 - XOR Vx, Vy
    8xy4 - ADD Vx, Vy
    8xy5 - SUB Vx, Vy
    8xy6 - SHR Vx {, Vy}
    8xy7 - SUBN Vx, Vy
    8xyE - SHL Vx {, Vy}
    9xy0 - SNE Vx, Vy
    Annn - LD I, addr
    Bnnn - JP V0, addr
    Cxkk - RND Vx, byte
    Dxyn - DRW Vx, Vy, nibble
    Ex9E - SKP Vx
    ExA1 - SKNP Vx
    Fx07 - LD Vx, DT
    Fx0A - LD Vx, K
    Fx15 - LD DT, Vx
    Fx18 - LD ST, Vx
    Fx1E - ADD I, Vx
    Fx29 - LD F, Vx
    Fx33 - LD B, Vx
    Fx55 - LD [I], Vx
    Fx65 - LD Vx, [I]
    :param binary: binary file to be parsed
    :return: string containing parsed opcodes of given binary.
    """
    return_string = '\n'
    # Python string formatting help
    # https://docs.python.org/2/library/string.html#format-specification-mini-language
    with open(binary, 'rb') as fh:
        file_contents = bytearray(fh.read())
        print("-I- Number of bytes: {}".format(len(file_contents)))
        file_size = len(file_contents)
        if file_size % 2:
            print("-W- File size is odd number of bytes. Last byte will be skipped")
            file_size -= 1
        count = 0
        while count < file_size:
            opcode = (file_contents[count] << 8) | (file_contents[count+1])
            x = (opcode & 0x0f00) >> 8  # Register X - 4 bits
            y = (opcode & 0x00f0) >> 4  # Register Y - 4 bits
            kk = (opcode & 0x00ff)  # kk - byte - 8 bits - 1 byte
            nnn = (opcode & 0x0fff)  # nnn - address - 12 bits
            n = (opcode & 0x000f)  # n(nibble) - 4 bits
            if (opcode & 0xf000) >> 12 == 0:
                if opcode == 0x00e0:
                    return_string += "CLS \n"
                elif opcode == 0x00ee:
                    return_string += "RET \n"
                else:
                    return_string += "SYS 0x{:03X}\n".format(nnn)
            elif (opcode & 0xf000) >> 12 == 1:
                return_string += 'JP 0x{:03X}\n'.format(nnn)
            elif (opcode & 0xf000) >> 12 == 2:
                return_string += 'CALL 0x{:03X}\n'.format(nnn)
            elif (opcode & 0xf000) >> 12 == 3:
                return_string += 'SE V{:01X}, 0x{:02X}\n'.format(x, kk)
            elif (opcode & 0xf000) >> 12 == 4:
                return_string+= 'SNE V{:01X}, 0x{:02X}\n'.format(x, kk)
            elif(opcode & 0xf000) >> 12 == 5:
                return_string += 'SE V{:01X}, V{:01X}\n'.format(x, y)
            elif(opcode & 0xf000) >> 12 == 6:
                return_string += 'LD V{:01X}, 0x{:02X}\n'.format(x, kk)
            elif(opcode & 0xf000) >> 12 == 7:
                return_string += 'ADD V{:01X}, 0x{:02X}\n'.format(x, kk)
            elif(opcode & 0xf000) >> 12 == 8:
                if n == 0:
                    return_string += 'LD V{:01X}, V{:01X}\n'.format(x, y)
                elif n == 1:
                    return_string += 'OR V{:01X}, V{:01X}\n'.format(x, y)
                elif n == 2:
                    return_string += 'AND V{:01X}, V{:01X}\n'.format(x, y)
                elif n == 3:
                    return_string += 'XOR V{:01X}, V{:01X}\n'.format(x, y)
                elif n == 4:
                    return_string += 'ADD V{:01X}, V{:01X}\n'.format(x, y)
                elif n == 5:
                    return_string += 'SUB V{:01X}, V{:01X}\n'.format(x, y)
                elif n == 6:
                    return_string += 'SHR V{:01X}\n'.format(x)
                elif n == 7:
                    return_string += 'SUBN V{:01X}, V{:01X}\n'.format(x, y)
                elif n == 0xe:
                    return_string += 'SHL V{:01X}\n'.format(x)
            elif(opcode & 0xf000) >> 12 == 9:
                return_string += 'SNE V{:01X}, V{:01X}\n'.format(x, y)
            elif(opcode & 0xf000) >> 12 == 0xA:
                return_string += 'LD I, 0x{:03X}\n'.format(nnn)
            elif(opcode & 0xf000) >> 12 == 0xB:
                return_string += 'JP V0, 0x{:03X}\n'.format(nnn)
            elif(opcode & 0xf000) >> 12 == 0xC:
                return_string += 'RND V{:01X}, 0x{:02X}\n'.format(x, kk)
            elif(opcode & 0xf000) >> 12 == 0xD:
                return_string += 'DRW V{:01X}, V{:01X}, 0x{:01X}\n'.format(x, y, n)
            elif(opcode & 0xf000) >> 12 == 0xE:
                x = (opcode & 0x0f00) >> 8
                if (opcode & 0x00ff) == 0x9e:
                    return_string += 'SKP V{:01X}\n'.format(x)
                else:
                    return_string += 'SKNP V{:01X}\n'.format(x)
            elif(opcode & 0xf000) >> 12 == 0xF:
                if kk == 0x07:
                    return_string += 'LD V{:01X}, DT\n'.format(x)
                elif kk == 0x0A:
                    return_string += 'LD V{:01X}, K\n'.format(x)
                elif kk == 0x15:
                    return_string += 'LD DT, V{:01X}\n'.format(x)
                elif kk == 0x18:
                    return_string += 'LD ST, V{:01X}\n'.format(x)
                elif kk == 0x1E:
                    return_string += 'ADD I, V{:01X}\n'.format(x)
                elif kk == 0x29:
                    return_string += 'LD F, V{:01X}\n'.format(x)
                elif kk == 0x33:
                    return_string += 'LD B, V{:01X}\n'.format(x)
                elif kk == 0x55:
                    return_string += 'LD [I], V{:01X}\n'.format(x)
                elif kk == 0x65:
                    return_string += 'LD V{:01X}, [I]\n'.format(x)
            else:
                return_string += 'Invalid Opcode 0x{:4X}'.format(opcode)
            count += 2
    return return_string

def disassemble_binary_with_byte_offset(binary):
    """
    Disassemble binary with byte offset of each instructions.
    Standard Chip-8 Instructions
    From: http://devernay.free.fr/hacks/chip8/C8TECH10.HTM
    :param binary: binary file to be parsed
    :return: string containing parsed opcodes of given binary.
    """
    return_string = '\n'
    # Python string formatting help
    # https://docs.python.org/2/library/string.html#format-specification-mini-language
    with open(binary, 'rb') as fh:
        file_contents = bytearray(fh.read())
        print("-I- Number of bytes: 0x{:02X}({})".format(len(file_contents), len(file_contents)))
        count = 0
        address_offset = 0x0000
        while count < len(file_contents):
            opcode = (file_contents[count] << 8) | (file_contents[count+1])
            return_string = return_string + "0x{:02X}\t".format(address_offset)
            x = (opcode & 0x0f00) >> 8  # Register X - 4 bits
            y = (opcode & 0x00f0) >> 4  # Register Y - 4 bits
            kk = (opcode & 0x00ff)  # kk - byte - 8 bits - 1 byte
            nnn = (opcode & 0x0fff)  # nnn - address - 12 bits
            n = (opcode & 0x000f)  # n(nibble) - 4 bits
            if (opcode & 0xf000) >> 12 == 0:
                if opcode == 0x00e0:
                    return_string += "CLS \n"
                elif opcode == 0x00ee:
                    return_string += "RET \n"
                else:
                    return_string += "SYS 0x{:03X}\n".format(nnn)
            elif (opcode & 0xf000) >> 12 == 1:
                return_string += 'JP 0x{:03X}\n'.format(nnn)
            elif (opcode & 0xf000) >> 12 == 2:
                return_string += 'CALL 0x{:03X}\n'.format(nnn)
            elif (opcode & 0xf000) >> 12 == 3:
                return_string += 'SE V{:01X}, 0x{:02X}\n'.format(x, kk)
            elif (opcode & 0xf000) >> 12 == 4:
                return_string+= 'SNE V{:01X}, 0x{:02X}\n'.format(x, kk)
            elif(opcode & 0xf000) >> 12 == 5:
                return_string += 'SE V{:01X}, V{:01X}\n'.format(x, y)
            elif(opcode & 0xf000) >> 12 == 6:
                return_string += 'LD V{:01X}, 0x{:02X}\n'.format(x, kk)
            elif(opcode & 0xf000) >> 12 == 7:
                return_string += 'ADD V{:01X}, 0x{:02X}\n'.format(x, kk)
            elif(opcode & 0xf000) >> 12 == 8:
                if n == 0:
                    return_string += 'LD V{:01X}, V{:01X}\n'.format(x, y)
                elif n == 1:
                    return_string += 'OR V{:01X}, V{:01X}\n'.format(x, y)
                elif n == 2:
                    return_string += 'AND V{:01X}, V{:01X}\n'.format(x, y)
                elif n == 3:
                    return_string += 'XOR V{:01X}, V{:01X}\n'.format(x, y)
                elif n == 4:
                    return_string += 'ADD V{:01X}, V{:01X}\n'.format(x, y)
                elif n == 5:
                    return_string += 'SUB V{:01X}, V{:01X}\n'.format(x, y)
                elif n == 6:
                    return_string += 'SHR V{:01X}\n'.format(x)
                elif n == 7:
                    return_string += 'SUBN V{:01X}, V{:01X}\n'.format(x, y)
                elif n == 0xe:
                    return_string += 'SHL V{:01X}\n'.format(x)
            elif(opcode & 0xf000) >> 12 == 9:
                return_string += 'SNE V{:01X}, V{:01X}\n'.format(x, y)
            elif(opcode & 0xf000) >> 12 == 0xA:
                return_string += 'LD I, 0x{:03X}\n'.format(nnn)
            elif(opcode & 0xf000) >> 12 == 0xB:
                return_string += 'JP V0, 0x{:03X}\n'.format(nnn)
            elif(opcode & 0xf000) >> 12 == 0xC:
                return_string += 'RND V{:01X}, 0x{:02X}\n'.format(x, kk)
            elif(opcode & 0xf000) >> 12 == 0xD:
                return_string += 'DRW V{:01X}, V{:01X}, 0x{:01X}\n'.format(x, y, n)
            elif(opcode & 0xf000) >> 12 == 0xE:
                x = (opcode & 0x0f00) >> 8
                if (opcode & 0x00ff) == 0x9e:
                    return_string += 'SKP V{:01X}\n'.format(x)
                else:
                    return_string += 'SKNP V{:01X}\n'.format(x)
            elif(opcode & 0xf000) >> 12 == 0xF:
                if kk == 0x07:
                    return_string += 'LD V{:01X}, DT\n'.format(x)
                elif kk == 0x0A:
                    return_string += 'LD V{:01X}, K\n'.format(x)
                elif kk == 0x15:
                    return_string += 'LD DT, V{:01X}\n'.format(x)
                elif kk == 0x18:
                    return_string += 'LD ST, V{:01X}\n'.format(x)
                elif kk == 0x1E:
                    return_string += 'ADD I, V{:01X}\n'.format(x)
                elif kk == 0x29:
                    return_string += 'LD F, V{:01X}\n'.format(x)
                elif kk == 0x33:
                    return_string += 'LD B, V{:01X}\n'.format(x)
                elif kk == 0x55:
                    return_string += 'LD [I], V{:01X}\n'.format(x)
                elif kk == 0x65:
                    return_string += 'LD V{:01X}, [I]\n'.format(x)
            address_offset = address_offset + 2
            count += 2
    return return_string

def disassemble_binary_with_address_offset(binary):
    """
    Disassemble with address on which the opcodes will be stored.
    Program is stored on memory starting from address 512(0x200).
    Refer below link for more details.
    Standard Chip-8 Instructions
    From: http://devernay.free.fr/hacks/chip8/C8TECH10.HTM
    :param binary: binary file to be parsed
    :return: string containing parsed opcodes of given binary.
    """
    return_string = '\n'
    # Python string formatting help
    # https://docs.python.org/2/library/string.html#format-specification-mini-language
    with open(binary, 'rb') as fh:
        file_contents = bytearray(fh.read())
        print("-I- Number of bytes: 0x{:02X}({})".format(len(file_contents), len(file_contents)))
        count = 0
        address_offset = 0x200
        while count < len(file_contents):
            opcode = (file_contents[count] << 8) | (file_contents[count+1])
            return_string = return_string + "0x{:03X}\t".format(address_offset)
            x = (opcode & 0x0f00) >> 8  # Register X - 4 bits
            y = (opcode & 0x00f0) >> 4  # Register Y - 4 bits
            kk = (opcode & 0x00ff)  # kk - byte - 8 bits - 1 byte
            nnn = (opcode & 0x0fff)  # nnn - address - 12 bits
            n = (opcode & 0x000f)  # n(nibble) - 4 bits
            if (opcode & 0xf000) >> 12 == 0:
                if opcode == 0x00e0:
                    return_string += "CLS \n"
                elif opcode == 0x00ee:
                    return_string += "RET \n"
                else:
                    return_string += "SYS 0x{:03X}\n".format(nnn)
            elif (opcode & 0xf000) >> 12 == 1:
                return_string += 'JP 0x{:03X}\n'.format(nnn)
            elif (opcode & 0xf000) >> 12 == 2:
                return_string += 'CALL 0x{:03X}\n'.format(nnn)
            elif (opcode & 0xf000) >> 12 == 3:
                return_string += 'SE V{:01X}, 0x{:02X}\n'.format(x, kk)
            elif (opcode & 0xf000) >> 12 == 4:
                return_string+= 'SNE V{:01X}, 0x{:02X}\n'.format(x, kk)
            elif(opcode & 0xf000) >> 12 == 5:
                return_string += 'SE V{:01X}, V{:01X}\n'.format(x, y)
            elif(opcode & 0xf000) >> 12 == 6:
                return_string += 'LD V{:01X}, 0x{:02X}\n'.format(x, kk)
            elif(opcode & 0xf000) >> 12 == 7:
                return_string += 'ADD V{:01X}, 0x{:02X}\n'.format(x, kk)
            elif(opcode & 0xf000) >> 12 == 8:
                if n == 0:
                    return_string += 'LD V{:01X}, V{:01X}\n'.format(x, y)
                elif n == 1:
                    return_string += 'OR V{:01X}, V{:01X}\n'.format(x, y)
                elif n == 2:
                    return_string += 'AND V{:01X}, V{:01X}\n'.format(x, y)
                elif n == 3:
                    return_string += 'XOR V{:01X}, V{:01X}\n'.format(x, y)
                elif n == 4:
                    return_string += 'ADD V{:01X}, V{:01X}\n'.format(x, y)
                elif n == 5:
                    return_string += 'SUB V{:01X}, V{:01X}\n'.format(x, y)
                elif n == 6:
                    return_string += 'SHR V{:01X}\n'.format(x)
                elif n == 7:
                    return_string += 'SUBN V{:01X}, V{:01X}\n'.format(x, y)
                elif n == 0xe:
                    return_string += 'SHL V{:01X}\n'.format(x)
            elif(opcode & 0xf000) >> 12 == 9:
                return_string += 'SNE V{:01X}, V{:01X}\n'.format(x, y)
            elif(opcode & 0xf000) >> 12 == 0xA:
                return_string += 'LD I, 0x{:03X}\n'.format(nnn)
            elif(opcode & 0xf000) >> 12 == 0xB:
                return_string += 'JP V0, 0x{:03X}\n'.format(nnn)
            elif(opcode & 0xf000) >> 12 == 0xC:
                return_string += 'RND V{:01X}, 0x{:02X}\n'.format(x, kk)
            elif(opcode & 0xf000) >> 12 == 0xD:
                return_string += 'DRW V{:01X}, V{:01X}, 0x{:01X}\n'.format(x, y, n)
            elif(opcode & 0xf000) >> 12 == 0xE:
                x = (opcode & 0x0f00) >> 8
                if (opcode & 0x00ff) == 0x9e:
                    return_string += 'SKP V{:01X}\n'.format(x)
                else:
                    return_string += 'SKNP V{:01X}\n'.format(x)
            elif(opcode & 0xf000) >> 12 == 0xF:
                if kk == 0x07:
                    return_string += 'LD V{:01X}, DT\n'.format(x)
                elif kk == 0x0A:
                    return_string += 'LD V{:01X}, K\n'.format(x)
                elif kk == 0x15:
                    return_string += 'LD DT, V{:01X}\n'.format(x)
                elif kk == 0x18:
                    return_string += 'LD ST, V{:01X}\n'.format(x)
                elif kk == 0x1E:
                    return_string += 'ADD I, V{:01X}\n'.format(x)
                elif kk == 0x29:
                    return_string += 'LD F, V{:01X}\n'.format(x)
                elif kk == 0x33:
                    return_string += 'LD B, V{:01X}\n'.format(x)
                elif kk == 0x55:
                    return_string += 'LD [I], V{:01X}\n'.format(x)
                elif kk == 0x65:
                    return_string += 'LD V{:01X}, [I]\n'.format(x)
            address_offset = address_offset + 2
            count += 2
    return return_string

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("USAGE: disassembler.py ROM_PATH <MODE>")
    elif len(sys.argv) == 2:
        print("ROM given: {}".format(sys.argv[1]))
        print(disassemble_binary(sys.argv[1]))
    elif len(sys.argv) == 3:
        mode = int(sys.argv[2])
        if mode > 2:
            print("Invalid mode: {}".format(sys.argv[2]))
            exit(1)
        print("ROM given: {}, Mode: {}".format(sys.argv[1], MODE[mode]))
        if mode == 0:
            print(disassemble_binary(sys.argv[1]))
        if mode == 1:
            print(disassemble_binary_with_byte_offset(sys.argv[1]))
        if mode == 2:
            print(disassemble_binary_with_address_offset(sys.argv[1]))
