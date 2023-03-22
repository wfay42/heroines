import subprocess
import os

class Converter():
    def __init__(self, convert_all = False):
        self.convert_all = convert_all

    def should_convert(self, img_path, out_img_path):
        if self.convert_all:
            return True

        # if the output file doesn't exist, we should make it
        if not os.path.exists(out_img_path):
            return True

        input_modify_time = os.path.getmtime(img_path)
        output_modify_time = os.path.getmtime(out_img_path)

        # if the input is newer than the output,
        # then the output is stale and we should update it
        return input_modify_time > output_modify_time

    def convert_image(self, img_path):
        filename = os.path.basename(img_path)
        dirname = os.path.dirname(img_path)

        out_img_name = "_c-%s" % filename
        out_img_path = os.path.join(dirname, out_img_name)

        if not self.should_convert(img_path, out_img_path):
            print("Skipping converting %s to %s" % (img_path, out_img_path))
            return

        success = subprocess.call(["magick", "convert",
            "-crop", "+700+0+1000x1440",
            "-crop", "-860+0+1000x1440",
            img_path, out_img_path])
        print("Succeeded? %s - Converting %s to %s" % (success, img_path, out_img_path))


def main():
    converter = Converter()
    converter.convert_image(".\\raw_img\hazel-01.png")

if __name__ == '__main__':
    main()