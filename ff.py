#!/usr/bin/env python3

from argparse import ArgumentParser
import logging
import bitcoin
import json

import codecs
import urllib3

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

http = urllib3.PoolManager()

def get_hash_by_height(height):
    url = 'https://blockchain.info/block-height/'+str(height)+'?format=json'
    logger.info('url %s' % url)
    r = http.request('GET', url)
    text = json.loads(r.data)
    return text['blocks'][0]['hash']

def serialize_header(height):
    url = 'https://blockchain.info/block-height/'+str(height)+'?format=json'
    logger.info('url %s' % url)
    r = http.request('GET', url)
    text = json.loads(r.data)
    inp = text['blocks'][0]

    return inp

def blockHashHex(number):
    hexHead = hex(number)[2:-1]  # snip off the 0x and trailing L
    hexHead = '0' * (64 - len(hexHead)) + hexHead
    return hexHead

def main():
    parser = ArgumentParser()
    parser.add_argument('--startBlock', required=True, default=625332, type=int, help='block number to start fetching from')
    args = parser.parse_args()

    logger.info('startBlock: %s' % args.startBlock)
    height = args.startBlock

    realHead = get_hash_by_height(height)
    bhStr = serialize_header(height)
    logger.info("@@@ {0}: {1}".format(height, bhStr))
    logger.info("Block header: %s" % bhStr)

if __name__ == '__main__':
    main()
