# Hash Brown

[![CircleCI](https://circleci.com/gh/chingc/Hash-Brown.svg?style=shield)](https://circleci.com/gh/chingc/workflows/Hash-Brown) [![codecov](https://codecov.io/gh/chingc/Hash-Brown/branch/master/graph/badge.svg)](https://codecov.io/gh/chingc/Hash-Brown) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

A simple command-line utility for calculating checksums.

## Install

Coming soon to a PyPI near you!

## Usage

Calculate the sha1 of a file:

```
$ hb -a sha1 hello.txt
sha1 (hello.txt) = 493a253abf93d705d67edeb463134a5c8752fc9d
```

Check to see if file matches a given checksum:

```
$ hb -a md5 hello.txt -g 77060c267470021a97392b815138733e
md5 (hello.txt) = 77060c267470021a97392b815138733e OK

$ hb -a md5 hello.txt -g 0123456789abcdef
md5 (hello.txt) = 0123456789abcdef ACTUAL: 77060c267470021a97392b815138733e
```

Checksums can be read from a file:

```
$ hb -c checksums.txt
sha512 (hello.txt) = 493a253abf93d705d67edeb463134a5c8752fc9d OK
sha512 (world.txt) = 683e4ee04e75e71a6dca42807001f00be1fcb2a3 OK
sha512 (image.jpg) = f3a53e6c2743645f08faedadd7a2c57cbc38632f OK
sha512 (video.mp4) = 03ba9191fc4cd74f218df58542643fbc07dca532 OK
```

Hash Brown outputs its results in BSD style.  The checksum files are also BSD style.

All files are read in binary mode.

Globbing and recursive globbing are supported via `*` and `**` respectively.

Dotfiles are not included when globbing and need to be specified explicitly.

## Options

```
-a, --algorithm [blake2b|blake2s|md5|sha1|sha224|sha256|sha384|sha512|adler32|crc32]
-c, --check                     Read checksums from a file.
-g, --given TEXT                See if the given checksum `TEXT` matches the
                                computed checksum. (use with -a)
--version                       Show the version and exit.
-h, --help                      Show this message and exit.
```
