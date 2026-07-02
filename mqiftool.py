import itertools, copy
from random import randint

from bittools import byte_to_boollist, boollist_to_int_var, mk_uintvar, generate_boollist
import scqoi

def generate_frame(bitmap: list, palette: list, delay: int, disposal: bool):
    indmap = bytearray()
    for row in bitmap:
        for pixel in row:
            #try:
            indmap.append(palette.index(pixel))
            #except Exception:
            #    indmap.append(0)
    compressed = scqoi.compress(bytes(indmap))
    payloadlength = len(compressed)
    frame = bytearray()
    frame.append(int(disposal))
    frame.extend(delay.to_bytes(2, 'little'))
    frame.extend(payloadlength.to_bytes(4, 'little'))
    frame.extend(compressed)
    return frame

def generateheader(width, height, palette, transmode):
    head = bytearray()
    head.extend(width.to_bytes(2, 'little'))
    head.extend(height.to_bytes(2, 'little'))
    palbytes = bytearray()
    for col in palette:
        palbytes.append(col[0])
        palbytes.append(col[1])
        palbytes.append(col[2])
    head.append(len(palette)-1)
    head.append(int(transmode))

    head.extend(palbytes)

    return head

def gen_palette(bitmap, reserved: tuple = None, animated: bool = False):
    pal = []
    seen = set()

    if animated:
        imagedata = bitmap
    else:
        imagedata = [bitmap]

    for bitmap in imagedata:
        for row in bitmap:
            for px in row:
                if px not in seen:
                    seen.add(px)
                    pal.append(px)
                    if len(pal) > 256:
                        raise Exception("failed to palettize image to 256 colors or less.")

    pal.sort(key=lambda c: (c[0], c[1], c[2]))
    if reserved in pal:
        pal.remove(reserved)
        pal.insert(0, reserved)
    return pal

def encode(bitmap: list, transcolor: tuple = None, animated: bool = False, disposalmodes: list = None, framedelays: list = None):
    qif = bytearray(b"QIF26a")
    if animated:
        wid = len(bitmap[0][0])
        hei = len(bitmap[0])

        if not type(bitmap[0][0][0]) is tuple:
            raise Exception("grayscale is unsupported as of now")
        if disposalmodes is None or len(bitmap) > len(disposalmodes):
            raise Exception("a list of disposal modes for all frames is required!")
        if framedelays is None or len(bitmap) > len(framedelays):
            raise Exception("a list of timings for all frames is required!")
    else:
        wid = len(bitmap[0])
        hei = len(bitmap)

        if not type(bitmap[0][0]) is tuple:
            raise Exception("grayscale is unsupported as of now")

    if animated:
        pal = gen_palette(bitmap, transcolor, True)
    else:
        pal = gen_palette(bitmap, transcolor, False)

    qif.extend(generateheader(wid, hei, pal, bool(transcolor)))
    if animated:
        for i in range(len(bitmap)):
            qif.extend(generate_frame(bitmap[i], pal, framedelays[i], disposalmodes[i]))
    else:
        qif.extend(generate_frame(bitmap, pal, 0, False))

    qif.extend(b"\x00\x00\x00\x00\x00\x00\x00;")
    return bytes(qif)

def parseheader(header: bytes):
    width = int.from_bytes(header[0:2], "little")
    height = int.from_bytes(header[2:4], "little")
    palettesize = int(header[4])+1
    transparency = int(header[5])
    palette = []
    for i in range(palettesize):
        palette.append((int(header[(i*3)+6]), int(header[(i*3)+7]), int(header[(i*3)+8])))

    return width, height, palettesize, transparency, palette

def generate_canvas(width, height):
    frame = []
    blankline = []
    for _ in range(width):
        blankline.append(None)
    for _ in range(height):
        frame.append(blankline[:])
    return frame

def framebehead(data: bytes):
    disposal = int(data[0])
    delay = int.from_bytes(data[1:3], "little")
    payloadlength = int.from_bytes(data[3:8], "little")
    return disposal, delay, payloadlength

def decode_data(data, palette, transparency, width, height):
    frames = []
    bytten = 0

    while True:
        disposal, delay, payloadlength = framebehead(data[bytten:bytten+7])

        if disposal and not len(frames) == 0:
            frame = copy.deepcopy(frames[-1])
        else:
            frame = generate_canvas(width, height)

        bytten += 7
        if payloadlength == 0:
            return frames
        else:
            compressed = data[bytten:payloadlength+bytten]
            bytten += payloadlength
            ndata = scqoi.decompress(compressed)
            cx = 0
            cy = 0
            for index in ndata:
                if not (transparency and index == 0):
                    frame[cy][cx] = palette[index]
                cx += 1
                if cx == width:
                    cx = 0
                    cy += 1
                if cy == height:
                    break
            frames.append(frame)
    return frames

def decode(qifbytes: bytes):
    if not qifbytes.startswith(b'QIF26a'):
        raise Exception("Invalid QIF Image!")
    header = qifbytes[6:]
    width, height, palettesize, transparency, palette = parseheader(header)
    data = qifbytes[12+(palettesize*3):]
    if transparency:
        print(palette[0])
    frames = decode_data(data, palette, transparency, width, height)
    if len(frames) > 1:
        return frames, True
    else:
        return frames[0], False
