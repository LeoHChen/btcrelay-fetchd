#!/usr/bin/env python3

from argparse import ArgumentParser
import logging
import bitcoin
import urllib3

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def get_hash_by_height(height):
    url = 'https://blockchain.info/block-height/'+str(height)+'?format=json'
    r = http.request('GET', url)
    text = json.loads(r.data.decode('utf-8'))
    return text['blocks'][0]['hash']

def serialize_header(height):
    url = 'https://blockchain.info/block-height/'+str(height)+'?format=json'
    r = http.request('GET', url)
    text = json.loads(r.data.decode('utf-8'))
    inp = text['blocks'][0]

    o = encode(inp['ver'], 256, 4)[::-1] + \
        inp['prev_block'].decode('hex')[::-1] + \
        inp['mrkl_root'].decode('hex')[::-1] + \
        encode(inp['time'], 256, 4)[::-1] + \
        encode(inp['bits'], 256, 4)[::-1] + \
        encode(inp['nonce'], 256, 4)[::-1]
    h = bin_sha256(bin_sha256(o))[::-1].encode('hex')
    assert h == inp['hash'], (sha256(o), inp['hash'])
    return o.encode('hex')

def blockHashHex(number):
    hexHead = hex(number)[2:-1]  # snip off the 0x and trailing L
    hexHead = '0' * (64 - len(hexHead)) + hexHead
    return hexHead

def main():
    logger.info("fetchd using PyEPM %s" % __version__)
    parser = ArgumentParser()
    parser.add_argument('--startBlock', default=625332, type=int, help='block number to start fetching from')
    args = parser.parse_args()

    logger.info('startBlock: %s' % args.startBlock)
    height = args.startBlock

    realHead = get_hash_by_height(height)
    bhStr = serialize_header(height)
    logger.info("@@@ {0}: {1}".format(height, bhStr))
    logger.info("Block header: %s" % repr(bhStr.decode('hex')))

if __name__ == '__main__':
    main()
