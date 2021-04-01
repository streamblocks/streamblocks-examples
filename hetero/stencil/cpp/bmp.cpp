#include "bmp.h"

void blurKernel(const BMPImage &source, BMPImage &out) {

  auto w = source.header.getWidth();
  auto h = source.header.getHeight();
  std::cout << "Blur " << w << " x " << h << std::endl;
  for (int y = 1; y < h - 1; y++) {
    for (int x = 1; x < w - 1; x++) {
      // std::cout << "(" << x << ", " << y << ")" << std::endl;
      int ix = y * w + x;
      uint8_t t1 = (source.pixels[ix + 1].r);
      uint8_t t2 = (source.pixels[ix - 1].r);
      uint8_t t3 = (source.pixels[ix - w].r);
      uint8_t t4 = (source.pixels[ix + w].r);
      out.pixels[ix].r = (t1 + t2 + t3 + t4) / 4;

      t1 = (source.pixels[ix + 1].b);
      t2 = (source.pixels[ix - 1].b);
      t3 = (source.pixels[ix - w].b);
      t4 = (source.pixels[ix + w].b);
      out.pixels[ix].b = (t1 + t2 + t3 + t4) / 4;

      t1 = (source.pixels[ix + 1].g);
      t2 = (source.pixels[ix - 1].g);
      t3 = (source.pixels[ix - w].g);
      t4 = (source.pixels[ix + w].g);
      out.pixels[ix].g = (t1 + t2 + t3 + t4) / 4;
    }
  }
}

BMPImage blurKernel(const BMPImage &source) {
  auto w = source.header.getWidth();
  auto h = source.header.getHeight();
  BMPImage out(source);
  std::cout << "Blur " << w << " x " << h << std::endl;
  for (int y = 1; y < h - 1; y++) {
    for (int x = 1; x < w - 1; x++) {
      // std::cout << "(" << x << ", " << y << ")" << std::endl;
      int ix = y * w + x;
      uint8_t t1 = (source.pixels[ix + 1].r);
      uint8_t t2 = (source.pixels[ix - 1].r);
      uint8_t t3 = (source.pixels[ix - w].r);
      uint8_t t4 = (source.pixels[ix + w].r);
      out.pixels[ix].r = (t1 + t2 + t3 + t4) / 4;

      t1 = (source.pixels[ix + 1].b);
      t2 = (source.pixels[ix - 1].b);
      t3 = (source.pixels[ix - w].b);
      t4 = (source.pixels[ix + w].b);
      out.pixels[ix].b = (t1 + t2 + t3 + t4) / 4;

      t1 = (source.pixels[ix + 1].g);
      t2 = (source.pixels[ix - 1].g);
      t3 = (source.pixels[ix - w].g);
      t4 = (source.pixels[ix + w].g);
      out.pixels[ix].g = (t1 + t2 + t3 + t4) / 4;
    }
  }
  return out;
}

BMPImage blurKernel(const BMPImage &source, const int n) {

  if (n == 1) {
    return blurKernel(source);
  } else {
    return blurKernel(blurKernel(source), n - 1);
  }
}
int main() {

  BMPParser parser;
  BMPImage img;
  bool success = parser.parse("../images/concentric.bmp", img);
  if (success) {
    std::cout << "Image parsed " << img.header.getHeight() << " x "
              << img.header.getWidth() << std::endl;

    std::cout << "Applying blur" << std::endl;

    BMPImage out_img = blurKernel(img, 200);

    
    std::cout << "Saving output " << std::endl;
    parser.dump("test.bmp", out_img);
  } else {
    std::cout << "Parsing failed" << std::endl;
  }
}