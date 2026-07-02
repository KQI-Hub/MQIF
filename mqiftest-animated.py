from ppmgen import ppm_from_list, ppm_to_list, pgm_from_list, pam_from_list
from mqiftool import decode, encode

def ntps(n: int):
    if len(str(n)) == 1:
        return f"0{n}"
    else:
        return str(n)

#filename = "mqif-animation/remapped/"
#totalframes = 41
#frames = []
#disposals = []
#delays = []

#for i in range(1, totalframes+1):
#    inpt = open(f"{filename}{ntps(i)}.ppm", "rb").read()
#    frames.append(ppm_to_list(inpt))
#    disposals.append(True)
#    delays.append(40) if (i % 2) else delays.append(30)

#output = encode(frames, (255, 0, 255), True, disposals, delays)
#open(f"tenor.mqif", "wb").write(output)

inputf = open(f"tenor.mqif", "rb").read()
bmp, animated = decode(inputf)
if animated:
    for i in range(len(bmp)):
        ppm = ppm_from_list(bmp[i])
        open(f"output/frame_{ntps(i)}.ppm", "wb").write(ppm)
else:
    ppm = ppm_from_list(bmp)
    open(f"tenor_decoded.ppm", "wb").write(ppm)
