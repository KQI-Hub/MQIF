import scqoi

fn = "blobby.txt"
thisfile = open(fn, 'rb').read()

open(f'{fn}.scq', "wb").write(scqoi.compress(thisfile))

newfile = open(f'{fn}.scq', """rb""").read()

open(f'decompressed_{fn}', "wb").write(scqoi.decompress(newfile))
