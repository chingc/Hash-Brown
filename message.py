"""Various messages."""


def help():
    """Usage: hb -h | -v
       hb -c FILE(S)
       hb ALGORITHM -d FILE FILE [FILE FILE] [...]
       hb ALGORITHM -e FILE(S)
       hb ALGORITHM -i FILE DIGEST [FILE DIGEST] [...]
       hb ALGORITHM -s "hello, world!"
       hb ALGORITHM FILE(S)

Algorithms:
    md5, sha1, sha224, sha256, sha384, sha512
    adler32, crc32

Options:
    -h    this help screen
    -v    version information
    -c    checklist: verify the files given in a checklist
    -d    dupe: determine whether two files are identical
    -e    embedded: verify a file using the digest or checksum in its filename
    -i    inline: verify a file with a digest or checksum
    -s    string: hash a string of text

Notes:
    A checklist is an ordinary text file with lines like this:
    CRC32 (document.txt) = ad0c2001

    Checklists are allowed to have mixed types.  Example:
    CRC32 ("hello, world!") = 58988d13
    MD5 (audio.flac) = 69afdf17b98ed394964f15ab497e12d2
    SHA1 (video.mkv) = 1f09d30c707d53f3d16c530dd73d70a6ce7596a9

    Text can appear anywhere within the checklist.  Example:
    Top secret!  CRC32 (document.txt) = ad0c2001
    CRC32 ("hello, world!") = 58988d13  Strings are quoted!

    A blank line went by!
    MD5 (audio.mp3) = 69afdf17b98ed394964f15ab497e12d2
    SHA1 (video.mkv) = 1f09d30c707d53f3d16c530dd73d70a6ce7596a9
    That's all the files I want to check for now.

Contact:
    https://github.com/smwst/hb
    smwst10@x.y | x = gmail, y = com

    """
    print(help.__doc__)


def version():
    """3.01"""
    print(version.__doc__)
