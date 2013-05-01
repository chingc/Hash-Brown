# Hash Brown

A convenient command-line file hashing utility.


## Download

Latest source code available [here][download].


## Usage

Obtain the SHA1 digest of a file:

`hb.py sha1 -i document.txt`

SHA1 is the default, so it can be omitted:

`hb.py -i document.txt`

Verify a file with MD5 quickly:

`hb.py md5 -m audio.flac 69afdf17b98ed394964f15ab497e12d2`

Verify a file with the checksum in the filename itself:

`hb.py crc32 -e video_[B7BFA115].mkv`


## Checklist

When using checklists, the argument specifying the hashing algorithm is ignored.  It will be determined by the checklist.

A checklist is a plain text file with lines like this:

    CRC32 (document.txt) = ad0c2001
    CRC32 (photo.png) = 1629491b

It can contain different algorithms.

    CRC32 (document.txt) = ad0c2001
    CRC32 (photo.png) = 1629491b
    MD5 (audio.flac) = 69afdf17b98ed394964f15ab497e12d2
    SHA1 (video.mkv) = 1f09d30c707d53f3d16c530dd73d70a6ce7596a9

Comments can be on a line by itself, at the beginning, or the end.

    I am a string.  CRC32 ("hello, world!") = 58988d13  Double quote me!


## Support

Hash Brown should run on any platform that has Python 3.3.1 installed without the need for any additional libraries.


## License

Hash Brown is distributed under the Simplified BSD license.  See [LICENSE][1] for more details.




[download]: https://github.com/smwst/Hash-Brown/raw/master/hb.zip "Hash Brown"
[license]: https://github.com/smwst/LICENSE#readme "License"
