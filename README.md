# Hash Brown

A convenient interface for hashlib and zlib.

## Install

```
pip install hb
```

## Usage

```
>>> from hb import hb

>>> hb.algorithms_guaranteed
['adler32', 'blake2b', 'blake2s', 'crc32', 'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512', 'sha512', 'shake_128', 'shake_256']

>>> hb.compute('sha1', 'hello.txt')
'fab3fff31b58f5c50ce0213407eb3e047cf2a8dc sha1 hello.txt'

>>> hb.scan('hexdigests.txt')
OK crc32 hello.txt
OK md5 world.txt
OK sha1 image.jpg
OK sha256 video.mp4
```

From the command line

```
$ python -m hb -c sha1 hello.txt
fab3fff31b58f5c50ce0213407eb3e047cf2a8dc sha1 hello.txt

$ cat hexdigests.txt
71d4f5e9 crc32 hello.txt
039c6a18baa8d77474b61fac86aeb7c7 md5 world.txt
ff0023686cd30938c2eade9b08e1507747d7fbf6 sha1 image.jpg
006e7bcdbdc2b77636b6ca695b7b68227b30c10130106b990f20d3ccace1cb9b sha256 video.mp4

$ python -m hb -s hexdigests.txt
OK crc32 hello.txt
OK md5 world.txt
OK sha1 image.jpg
OK sha256 video.mp4
```
