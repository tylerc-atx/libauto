import sys


outbuf = sys.stdout.detach()


while True:

    text = sys.stdin.readline()
    if text == '':
        break

    chunk = text.encode('utf-8')

    chunk_type = 1
    outbuf.write(chunk_type.to_bytes(1, byteorder='big'))

    chunk_len = len(chunk)
    outbuf.write(chunk_len.to_bytes(4, byteorder='big'))

    outbuf.write(chunk)

    outbuf.flush()

