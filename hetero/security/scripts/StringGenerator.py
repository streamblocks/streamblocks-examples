
import random
import string
import hashlib
import argparse


def toBytes(n):
    return [
        (n >> 24) & 0xFF,
        (n >> 16) & 0xFF,
        (n >> 8) & 0xFF,
        n & 0xFF
    ]


def stringGenerator(min_size, max_size, num_pe, str_per_pe, binary=True):

    with open("strings." + ("bin" if binary else "txt"), "w" + ("b" if binary else "")) as stringsStream:

        with open("ref_hash." + ('bin' if binary else 'txt'), "w" + ("b" if binary else "")) as hashStream:

            letters = string.ascii_lowercase + string.ascii_uppercase
            for string_ix in range(0, num_pe * str_per_pe):
                string_size = random.randint(min_size, max_size)
                text = ""
                if binary:

                    stringsStream.write(bytes(toBytes(string_size)))
                    characters = [random.choice(letters)
                                  for i in range(0, string_size)]
                    text = text.join(characters).encode('ascii')
                    
                    stringsStream.write(bytes(text))
                    # text.join(characters)
                else:
                    for byte in toBytes(string_size):
                        line = str(byte) + "\n"
                        stringsStream.write(line)

                    for ix in range(0, string_size):
                        character = random.choice(letters)
                        print(character)
                        line = str(ord(character)) + "\n"
                        stringsStream.write(character)
                        text += character

                    text = text.encode('ascii')

                hash = hashlib.sha1(text)
                # print("Text: %s Hash:%s"%(text, hash.hexdigest()))
                if binary:
                  hashStream.write(bytes(hash.digest()))
                else:
                  byte_ix = 24
                  word = 0
                  for byte in bytearray(hash.digest()):
                      word += ((byte & 0xFF) << byte_ix)
                      if byte_ix == 8:
                          hashStream.write(str(word) + "\n")
                          word = 0
                          byte_ix = 24
                      else:
                          byte_ix -= 8


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate random strings")
    parser.add_argument('--num-pes', type=int,
                        help="number of SHA1 processing elements", required=True)
    parser.add_argument('--min-size', type=int,
                        help="Minimum string size", required=True)
    parser.add_argument('--max-size', type=int,
                        help='maximum string size', required=True)
    parser.add_argument('--strings-per-pe', type=int,
                        help='number of strings per pe', required=True)
    parser.add_argument('--ascii', action='store_true', default=False, help='save results in ascii txt files')
    args = parser.parse_args()

    stringGenerator(args.min_size, args.max_size,
                    args.num_pes, args.strings_per_pe, args.ascii == False)
