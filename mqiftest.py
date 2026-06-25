from ppmgen import ppm_from_list, ppm_to_list, pgm_from_list
from mqiftool import decode, encode

filename = "cover"

inpt = open(f"{filename}.ppm", "rb").read()
bitmap = ppm_to_list(inpt)
output = encode(bitmap)
open(f"{filename}.mqif", "wb").write(output)

inputf = open(f"{filename}.mqif", "rb").read()
bmp = decode(inputf)
ppm = ppm_from_list(bmp)
open(f"{filename}_decoded.ppm", "wb").write(ppm)

#pgm = ["P2\n8 8\n255\n"]
#for v in out:
#    pgm.append(str(v))
#pgm = " ".join(pgm)+"\n"

#kqi = generator_is_my_name(1920, 1080)
#open("randomly-generated-1920x1080.kqi", "wb").write(kqi)

#inputfile = open("rtx0.ppm", "rb").read()
#listed = ppm_to_list(inputfile)
#gh = bitmap_to_chunkmap(listed)
#hg = chunkmap_to_bitmap(gh, len(listed[0]), len(listed))
#ppmed = ppm_from_list(hg)
#open("ieatsand.ppm", "wb").write(ppmed)
