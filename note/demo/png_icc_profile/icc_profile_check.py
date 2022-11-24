import os

from PIL import Image

from kivy.core.image.img_sdl2 import ImageLoaderSDL2
# i = "./plu_merch/20221117a55942f3-0028-4e86-9902-ff43357738e9imageView1w250h250.png"
# i2 = "./plu_merch/20221117a55942f3-0028-4e86-9902-ff43357738e9imageView1w250h250-2.png"
#
# img = ImageLoaderSDL2(i)
#
# i = Image.open(i)
# i.info.pop("icc_profile")
# i.save(i2)
#
# img2 = ImageLoaderSDL2(i2)


old_dir = "./TCC"
# old_dir = "./plu_merch_old"
new_dir = old_dir + "_new"

if not os.path.isdir(new_dir):
    os.makedirs(new_dir)


only_icc_profile_log = False


for top, dirs, files in os.walk(old_dir):
    for file in files:
        try:
            img_file = f"{old_dir}/{file}"
            not only_icc_profile_log and print(f"ImageLoaderSDL2:{img_file}")
            ImageLoaderSDL2(img_file)
            i = Image.open(img_file)
            if "icc_profile" in i.info:
                print(f"delete icc profile: {img_file}")
                i.info.pop("icc_profile")
            new_file = f"{new_dir}/{file}"
            i.save(new_file)
            not only_icc_profile_log and print(f"ImageLoaderSDL2 after check:{new_file}")
            ImageLoaderSDL2(new_file)
            not only_icc_profile_log and print("\n")
        except Exception as err:
            print(err)
