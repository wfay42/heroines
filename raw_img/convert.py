import subprocess
import glob
import json
import os
import shutil
import sys

class CopyInstructions():
    def __init__(self, copy_instructions_json_file_path):
        with open(copy_instructions_json_file_path) as fp:
            obj = json.load(fp)

        # all of these are lists
        self.skip = obj['skip']
        self.enemies = obj['enemies']
        self.titles = obj['titles']

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

    def crop_images(self, img_path):
        filename = os.path.basename(img_path)
        dirname = os.path.dirname(img_path)

        out_img_name = "_c-%s" % filename
        out_img_path = os.path.join(dirname, out_img_name)

        if not self.should_convert(img_path, out_img_path):
            print("Skipping cropping %s to %s" % (img_path, out_img_path))
            return None

        # TODO: should probably return a struct with the input and output paths
        return subprocess.Popen(["magick", "convert",
            "-crop", "+700+0+1000x1440",
            "-crop", "-860+0+1000x1440",
            img_path, out_img_path])

    def crop_original_images(self, root_path):
        path_pattern = os.path.join(root_path, "*.png")
        path_list = glob.glob(path_pattern)

        conversion_popens = []
        for path in path_list:
            # ignore cropped or resized images created from the conversion process
            basename = os.path.basename(path)
            if basename.startswith('_c') or basename.startswith('_r') or basename.startswith('ending'):
                continue
            popen = self.crop_images(path)
            if popen is not None:
                conversion_popens.append(popen)

        # now that we kicked off all the conversions, check if they succeeded
        for popen in conversion_popens:
            success = popen.wait()
            print("Subprocess return code: %s" % success)

    def resize_image(self, img_path):
        filename = os.path.basename(img_path)
        dirname = os.path.dirname(img_path)

        out_img_name = "_r%s" % filename
        out_img_path = os.path.join(dirname, out_img_name)

        if not self.should_convert(img_path, out_img_path):
            print("Skipping resizing %s to %s" % (img_path, out_img_path))
            return None

        # enemy files need to be <640 pixels high
        dimensions = "500x720"
        if "enemy" in filename:
            dimensions = "386x500"
        # ending files we resize to the size of the game window
        elif "ending" in filename:
            dimensions = "1280x720"

        # TODO: should probably return a struct with the input and output paths
        return subprocess.Popen(["magick", "convert",
            "-resize", dimensions,
            img_path, out_img_path])


    def resize_cropped_images(self, root_path):
        path_pattern = os.path.join(root_path, "_c*.png")
        path_list = glob.glob(path_pattern)

        path_pattern = os.path.join(root_path, "ending*.png")
        path_list.extend(glob.glob(path_pattern))

        conversion_popens = []
        for path in path_list:

            popen = self.resize_image(path)
            if popen is not None:
                conversion_popens.append(popen)

        # now that we kicked off all the conversions, check if they succeeded
        for popen in conversion_popens:
            success = popen.wait()
            print("Subprocess return code: %s" % success)

    def copy_files(self, root_path, output_dir, copy_instructions):
        path_pattern = os.path.join(root_path, "_r*.png")
        path_list = glob.glob(path_pattern)
        print(path_list)

        for path in path_list:
            basename = os.path.basename(path)
            output_path = os.path.join(output_dir, basename)

            if basename in copy_instructions.skip:
                print("Skipping copying %s because it is in the skip list" % path)
                continue

            if not self.should_convert(path, output_path):
                print("Skipping copying %s to %s" % (path, output_path))
                continue

            print("Copying %s to %s" % (path, output_path))
            shutil.copy2(path, output_path)

def main():
    if len(sys.argv) < 4:
        print("Usage: convert.py input_directory copy_directory copy_instructions")
        return

    # eagerly initialize everything from arguments to find any issues
    root_path = sys.argv[1]
    copy_directory = sys.argv[2]
    copy_instructions_json_file_path = sys.argv[3]
    copy_instructions = CopyInstructions(copy_instructions_json_file_path)

    print("Converting files in directory %s" % root_path)
    converter = Converter()
    converter.crop_original_images(root_path)
    print("Cropping complete.  Starting resizing.")
    converter.resize_cropped_images(root_path)

    # copy the resized files somewhere
    converter.copy_files(root_path, copy_directory, copy_instructions)

if __name__ == '__main__':
    main()
