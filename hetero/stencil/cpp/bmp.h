#pragma once
#include <cstring>
#include <fstream>
#include <iostream>
#include <vector>

class BMPImage {
public:
  using WORD = uint16_t;
  using DWORD = uint32_t;
  using LONG = int32_t;
  struct BMPFileHeader {
    std::vector<uint8_t> buffer;

    WORD asWord(const DWORD offset) {
      return (static_cast<DWORD>(buffer[offset]) & 0x000000FF) +
             ((static_cast<DWORD>(buffer[offset + 1]) & 0x000000FF) << 8);
    }
    DWORD asDWord(const DWORD offset) const {
      return (static_cast<DWORD>(buffer[offset]) & 0x000000FF) +
             ((static_cast<DWORD>(buffer[offset + 1]) & 0x000000FF) << 8) +
             ((static_cast<DWORD>(buffer[offset + 2]) & 0x000000FF) << 16) +
             ((static_cast<DWORD>(buffer[offset + 3]) & 0x000000FF) << 24);
    }
    DWORD getWidth() const { return asDWord(0x012); }
    DWORD getHeight() const { return asDWord(0x016); }
    void fromStream(std::ifstream &stream) {

      buffer.resize(14);
      stream.seekg(0, std::ios::beg);
      stream.read(reinterpret_cast<char *>(buffer.data()), 14);
      DWORD bmp_offset = getOffset();
      DWORD bmp_size = getSize();
      std::cout << buffer[0] << buffer[1] << std::endl;
      buffer.resize(bmp_offset);

      stream.seekg(0, std::ios::beg);
      stream.read(reinterpret_cast<char *>(buffer.data()), bmp_offset);
    }
    DWORD getOffset() const { return asDWord(0x0A); }
    DWORD getPixelBytes() const { return asDWord(0x01C) / 8; }
    DWORD getSize() const { return asDWord(0x02); }
  };

  BMPFileHeader header;
  struct Pixel {
    uint8_t b, g, r, alpha;
  };
  std::vector<Pixel> pixels;
  uint32_t padding;
  BMPImage() { padding = 0; }
  BMPImage(const BMPImage &img) { copy(img); }

  void copy(const BMPImage &img) {
    this->header.buffer.resize(img.header.buffer.size());
    std::memcpy(this->header.buffer.data(), img.header.buffer.data(),
                img.header.buffer.size());
    this->pixels.resize(img.pixels.size());
    std::memcpy(this->pixels.data(), img.pixels.data(), img.pixels.size());
    std::cout << "Copy assigned BMPImage " << this->header.buffer.size() << " "
              << this->pixels.size() << std::endl;
    this->padding = img.padding;
  }
  BMPImage &operator=(const BMPImage &img) {
    copy(img);
    return *this;
  }
};

class BMPParser {
private:
  enum class State : int { Blue, Green, Red, Alpha };

public:
  BMPParser(){};
  bool parse(const std::string &file_name, BMPImage &img) {

    std::ifstream bmp_stream;
    try {

      bmp_stream.open(file_name, std::ios::binary);

      img.header.fromStream(bmp_stream);

      uint32_t pos = img.header.getOffset();
      bmp_stream.seekg(pos, std::ios::beg);

      uint32_t x = 0, y = 0, index = 0, padding = 0;
      uint32_t bmp_size = img.header.getSize();
      uint32_t w = img.header.getWidth(), h = img.header.getHeight();

      img.pixels.resize(w * h);

      uint32_t byte_per_pixel = img.header.getPixelBytes();

      State stream_state = State::Blue;

      if ((w * byte_per_pixel % 4 != 0)) {
        int fl = (w * byte_per_pixel) / 4;
        int cl = fl + 1;
        padding = cl * 4 - w * byte_per_pixel;
      }
      img.padding = padding;
      // std::cout << "padding " << padding << std::endl;
      // std::cout << "offset " << pos << std::endl;
      while (y < h) {
        uint8_t v;
        index = y * w + x;
        // std::cout << "index = " << index;
        switch (stream_state) {
        case State::Blue:
          v = bmp_stream.get();
          // std::cout << "v = " << (int)v << std::endl;
          img.pixels[index].b = v;
          stream_state = State::Green;
          break;
        case State::Green:
          v = bmp_stream.get();
          // std::cout << "v = " << (int)v << std::endl;
          img.pixels[index].g = v;
          stream_state = State::Red;
          break;
        case State::Red:
          v = bmp_stream.get();
          // std::cout << "v = " << (int)v << std::endl;
          img.pixels[index].r = v;
          if (byte_per_pixel == 3) {
            if (x == w - 1) {
              x = 0;
              y = y + 1;
              for (int _l = 0; _l < padding; _l++) {
                char tmp = bmp_stream.get();
              }
            } else {
              x++;
            }
            stream_state = State::Blue;
          } else {
            stream_state = State::Alpha;
          }
          break;
        case State::Alpha:
          v = bmp_stream.get();
          // std::cout << "v = " << (int)v << std::endl;
          img.pixels[index].alpha = v;

          if (x == w - 1) {
            x = 0;
            y = y + 1;
            for (int _l = 0; _l < padding; _l++) {
              bmp_stream.get();
            }
          } else {
            x++;
          }
          stream_state = State::Blue;
          break;
        }
      }

      return true;
    } catch (const std::ios_base::failure &fail) {
      std::cerr << "Could not open file " << fail.what() << std::endl;
      return false;
    }
  }

  bool dump(const std::string &file_name, const BMPImage &img) {
    try {
      std::ofstream bmp_out(file_name, std::ios::binary);

      std::cout << "Writing file header " << img.header.getOffset();
      bmp_out.write(reinterpret_cast<const char *>(img.header.buffer.data()),
                    img.header.getOffset());

      uint32_t x = 0, y = 0, w = img.header.getWidth(),
               h = img.header.getHeight();

      uint32_t bytes_per_pixel = img.header.getPixelBytes();

      std::cout << "Writing image " << w << " x " << h << std::endl;
      uint32_t image_size = h * (w * (bytes_per_pixel) + img.padding);
      // std::vector<uint8_t> raw_buffer(image_size);
      // std::cout << "Creating raw buffer " << std::endl;
      uint32_t ix = 0;
      while (y < h) {
        uint32_t index = y * w + x;
        // std::cout << "(" << x << ", " << y << ")" << std::endl;
        bmp_out.put(img.pixels[index].b);
        bmp_out.put(img.pixels[index].g);
        bmp_out.put(img.pixels[index].r);

        // std::cout << "( " << (int)img.pixels[index].b << ", "
        //           << (int)img.pixels[index].g << ", "
        //           << (int)img.pixels[index].r << ")" << std::endl;
        if (bytes_per_pixel == 4) {
          bmp_out.put(img.pixels[index].alpha);
        }

        if (x == w - 1) {
          x = 0;
          y = y + 1;
          for (int _i = 0; _i < img.padding; _i++) {
            bmp_out.put(0x00);
          }
        } else {
          x++;
        }
      }
      // std::cout << "Writing raw buffer " << std::endl;
      // bmp_out.write(reinterpret_cast<char *>(raw_buffer.data()),
      //               raw_buffer.size());

      return true;
    } catch (std::ios_base::failure &fail) {
      std::cerr << "Could not dump to file " << fail.what() << std::endl;
      return false;
    }
  }
};