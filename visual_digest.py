#!/usr/bin/python3

from PIL import Image
import argparse
import base64
import binascii
import random
import subprocess
import sys


SIZE = 100
RATE = 4 / 5


def byte_to_yuri(i, size=SIZE):
    return Image.open('yuribyte/twdne-60000/{}.jpg'.format(i)).resize((size, size), Image.BOX)


def visual_digest(data, size=SIZE, rate=RATE):
    if rate < 1:
        data = reedsolo(data, rate=rate)
    images = [byte_to_yuri(i, size=size) for i in data]
    deterministic_shuffle(images)
    return compose(images, size)


def deterministic_shuffle(l):
    r = random.Random(x='anime;brain?reset!') # fixed seed
    r.shuffle(l)


def reedsolo(data, rate=RATE):
    k = len(data)
    m = max(1, round(k / rate - k))
    p = subprocess.run(['./reedsolo', str(k), str(m)],
                       input=bytes(data), stdout=subprocess.PIPE, check=True)
    return p.stdout


def compose(images, size):
    nhor = int(len(images) ** 0.5)
    nver = len(images) // nhor + bool(len(images) % nhor)

    new_im = Image.new('RGB', (nhor * size, nver * size))
    for i, im in enumerate(images):
        x = i % nhor
        y = i // nhor
        new_im.paste(im, (x * size, y * size))
    return new_im


def main():
    p = argparse.ArgumentParser(description='Produce a visual fingerprint.')
    p.add_argument('-s', '--size', type=int, default=SIZE,
                   help='Desired size of subimages in pixels')
    p.add_argument('-r', '--rate', type=float, default=RATE,
                   help='Rate of error-correcting code')
    p.add_argument('-t', '--type', default='raw',
                   help='Input data type {raw, hex, base64}')
    p.add_argument('outfile', help='Destination file for image')
    args = p.parse_args()

    if args.type == 'raw':
        data = sys.stdin.buffer.read()
    elif args.type == 'hex':
        data = binascii.unhexlify(sys.stdin.read().strip())
    elif args.type == 'base64':
        data = base64.b64decode(sys.stdin.read())
    else:
        raise ValueError('bad type {}'.format(args.type))

    visual_digest(data, rate=args.rate, size=args.size).save(args.outfile)


if __name__ == '__main__':
    main()
