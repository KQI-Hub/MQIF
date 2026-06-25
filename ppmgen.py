def ppm_from_list(bitmap, desc = None):
    ppmhead = "P6\n" # raw format
    ppmbody = bytearray() # byte array

    if desc:
        ppmhead += "# {desc}\n"

    ppmhead += f"{len(bitmap[0])} {len(bitmap)}\n"
    ppmhead += "255\n"

    for row in bitmap:
        for pixel in row:
            ppmbody.append(pixel[0])
            ppmbody.append(pixel[1])
            ppmbody.append(pixel[2])

    return ppmhead.encode() + bytes(ppmbody)

def pgm_from_list(bitmap, desc = None):
    pgmhead = "P5\n" # raw format
    pgmbody = bytearray() # byte array

    if desc:
        pgmhead += "# {desc}\n"

    pgmhead += f"{len(bitmap[0])} {len(bitmap)}\n"
    pgmhead += "255\n"

    for row in bitmap:
        for pixel in row:
            pgmbody.append(pixel)

    return pgmhead.encode() + bytes(pgmbody)

def ppm_to_list(data: bytes):
    if not data.startswith(b'P6') and not data.startswith(b'P5'):
        raise Exception("Unsupported PPM!")
    gray = False
    if data.startswith(b"P5"):
        gray = True
    head = data.split(b"\n", 4)
    one = 1
    if head[1].decode('ascii').startswith("#"):
        one = 2
    res = head[one].decode('ascii').split(" ")
    width = int(res[0])
    height = int(res[1])
    tulmax = head[one+1].decode('ascii')
    if not tulmax == "255":
        raise Exception("Unsupported PPM!")
    if one == 1:
        bmpmap = data.split(b"\n", 3)[3]
    else:
        bmpmap = head[4]
    bitmap = []
    for h in range(height):
        bitmap.append([])
        for p in range(width):
            ligma = (h*width)+p
            if gray:
                bitmap[h].append(bmpmap[ligma])
            else:
                bitmap[h].append(( bmpmap[ligma*3] , bmpmap[(ligma*3)+1] , bmpmap[(ligma*3)+2] ))
    
    return bitmap
