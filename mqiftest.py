from ppmgen import ppm_from_list, ppm_to_list, pgm_from_list, pam_from_list
from mqiftool import decode, encode

filename = "flif"

#inpt = open(f"{filename}.ppm", "rb").read()
#bitmap = ppm_to_list(inpt)
#output = encode(bitmap, (255,0,255))
#open(f"{filename}.mqif", "wb").write(output)

inputf = open(f"{filename}.mqif", "rb").read()
bmp, _ = decode(inputf)
pam = pam_from_list(bmp)
open(f"{filename}_decoded.pam", "wb").write(pam)
