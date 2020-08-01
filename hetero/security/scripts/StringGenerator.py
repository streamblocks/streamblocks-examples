
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
def stringGenerator(min_size, max_size, num_pe, str_per_pe):


  with open("strings.txt", "w") as stringsStream:

    with open("ref_hash.txt", "w") as hashStream:

      letters = string.ascii_lowercase + string.ascii_uppercase
      for string_ix in range(0, num_pe * str_per_pe):
        string_size = random.randint(min_size, max_size)
        for byte in toBytes(string_size):
          stringsStream.write(str(byte) + "\n")
        text = ""
        for ix in range(0, string_size):
          character = random.choice(letters)
          line = str(ord(character)) + "\n"
          stringsStream.write(line)
          text += character
        
        hash = hashlib.sha1(text.encode('utf-8'))
        # print("Text: %s Hash:%s"%(text, hash.hexdigest()))

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
  parser.add_argument('--num-pes', type=int, help="number of SHA1 processing elements", required=True)
  parser.add_argument('--min-size', type=int, help="Minimum string size", required=True)
  parser.add_argument('--max-size', type=int, help='maximum string size', required=True)
  parser.add_argument('--strings-per-pe', type=int, help='number of strings per pe', required=True)
  args = parser.parse_args()
  stringGenerator(args.min_size, args.max_size, args.num_pes, args.strings_per_pe)
        
    
