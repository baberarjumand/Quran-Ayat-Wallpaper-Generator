# AYAT WALLPAPER GENERATOR
# This program generates wallpapers from the ayat (verses) of the Quran
# By default:
#   - one wallpaper is generated for one ayah
#   - wallpapers are of size 1920x1080
#   - the background is black
#   - the English translation used is Sahih International
# Custom resolutions can be created with custom fonts, but that will require the user to modify the relevant code themselves

# run to install required packages:
# pip install -r requirements.txt

import json
import textwrap
import urllib.request

from PIL import Image, ImageDraw, ImageFont

# install: pip install arabic-reshaper
from arabic_reshaper import arabic_reshaper

# install: pip install python-bidi
from bidi.algorithm import get_display


def create_background_image(MAX_W, MAX_H):
    im = Image.new('RGB', (MAX_W, MAX_H), (0, 0, 0, 0))
    im.save('background.jpg')


def write_text_on_image(t1, t2, img_width=1920, img_height=1080):
    im = Image.new('RGB', (img_width, img_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    # default text width is set to 120 characters
    para = textwrap.wrap(t1, width=120)
    # default font-size is 35
    font = ImageFont.truetype('fonts/Amiri-Regular.ttf', 35)

    # by default, text is written after leaving a space 15 percent of the total height of image on top
    current_h, pad = 0.15 * img_height, 10
    for line in para:
        w, h = draw.textsize(line, font=font)
        draw.text(((img_width - w) / 2, current_h), line, font=font)
        current_h += h + pad

    para2 = textwrap.wrap(t2, width=120)
    for line in para2:
        w, h = draw.textsize(line, font=font)
        draw.text(((img_width - w) / 2, current_h), line, font=font)
        current_h += h + pad

    im.save('test.jpg')


def get_json_object_from_url(url):
    try:
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        return data
    except urllib.request.HTTPError as err:
        if err.code == 404:
            print("HTTP ERROR 404 - Probably an invalid ayah reference provided")
        else:
            raise


def import_quran_arabic_into_json():
    jsonObject = get_json_object_from_url("http://api.alquran.cloud/v1/quran/quran-uthmani")
    with open('quran_data/quran-ar.json', 'w') as json_file:
        json.dump(jsonObject, json_file)
    print("quran_data/quran-ar.json successfully created")


def import_quran_english_into_json():
    jsonObject = get_json_object_from_url("http://api.alquran.cloud/v1/quran/en.sahih")
    with open('quran_data/quran-en.json', 'w') as json_file:
        json.dump(jsonObject, json_file)
    print("quran_data/quran-en.json successfully created")


def write_ayah_on_image(ayah_arabic_text, ayah_english_text, surah_number, ayah_number, img_width=1920, img_height=1080):
    im = Image.new('RGB', (img_width, img_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    para = textwrap.wrap(ayah_arabic_text, width=120)
    font = ImageFont.truetype('fonts/Amiri-Regular.ttf', 35)

    current_h, top_padding = 0.15 * img_height, 10
    for line in reversed(para):
        w, h = draw.textsize(line, font=font)
        draw.text(((img_width - w) / 2, current_h), line, font=font)
        current_h += h + top_padding

    para2 = textwrap.wrap(ayah_english_text, width=120)
    for line in para2:
        w, h = draw.textsize(line, font=font)
        draw.text(((img_width - w) / 2, current_h), line, font=font)
        current_h += h + top_padding

    im.save('generated_images/s' + surah_number.zfill(3) + 'a' + ayah_number.zfill(3) + '.jpg')


def generate_wallpapers_for_first_surah():
    try:
        with open('quran_data/quran-ar.json') as quran_ar_json_file:
            quran_ar_json = json.load(quran_ar_json_file)
    except FileNotFoundError:
        print("Local quran-ar.json file not found, downloading now...")
        print("Please wait...")
        import_quran_arabic_into_json()

    try:
        with open('quran_data/quran-en.json') as quran_en_json_file:
            quran_en_json = json.load(quran_en_json_file)
    except FileNotFoundError:
        print('Local quran-en.json file not found, downloading now...')
        print('Please wait...')
        import_quran_english_into_json()

    current_surah = 1
    for ayah_ar, ayah_en in zip(quran_ar_json["data"]["surahs"][current_surah-1]["ayahs"], quran_en_json["data"]["surahs"][current_surah-1]["ayahs"]):
        print(ayah_ar["text"])
        print(ayah_en["text"])
        print('Quran[' + str(current_surah) + ":" + str(ayah_en["numberInSurah"]) + ']')
        ayah_arabic_text = ayah_ar["text"]
        reshaped_arabic_text = arabic_reshaper.reshape(ayah_arabic_text)
        ayah_arabic_text = reshaped_arabic_text[::-1]
        ayah_english_text = ayah_en["text"]
        surah_number = str(current_surah)
        ayah_number = str(ayah_en["numberInSurah"])
        ayah_english_text += ' - Quran[' + str(current_surah) + ":" + str(ayah_en["numberInSurah"]) + ']'
        write_ayah_on_image(ayah_arabic_text, ayah_english_text, surah_number, ayah_number)


def generate_wallpapers_by_surah_number(surah_number):
    current_surah_index = surah_number - 1

    try:
        with open('quran_data/quran-ar.json') as quran_ar_json_file:
            quran_ar_json = json.load(quran_ar_json_file)
    except FileNotFoundError:
        print("Local quran-ar.json file not found, downloading now...")
        print("Please wait...")
        import_quran_arabic_into_json()

    try:
        with open('quran_data/quran-en.json') as quran_en_json_file:
            quran_en_json = json.load(quran_en_json_file)
    except FileNotFoundError:
        print('Local quran-en.json file not found, downloading now...')
        print('Please wait...')
        import_quran_english_into_json()

    for ayah_ar, ayah_en in zip(quran_ar_json["data"]["surahs"][current_surah_index]["ayahs"], quran_en_json["data"]["surahs"][current_surah_index]["ayahs"]):
        # print(ayah_ar["text"])
        # print(ayah_en["text"])
        # print('Quran[' + str(current_surah) + ":" + str(ayah_en["numberInSurah"]) + ']')
        ayah_arabic_text = ayah_ar["text"]
        reshaped_arabic_text = arabic_reshaper.reshape(ayah_arabic_text)
        ayah_arabic_text = get_display(reshaped_arabic_text)
        ayah_english_text = ayah_en["text"]
        surah_number = str(surah_number)
        ayah_number = str(ayah_en["numberInSurah"])
        ayah_english_text += ' - Quran[' + str(surah_number) + ":" + str(ayah_en["numberInSurah"]) + ']'
        write_ayah_on_image(ayah_arabic_text, ayah_english_text, surah_number, ayah_number)


if __name__ == '__main__':
    # MAX_W = 1920
    # MAX_H = 1080
    # TEXT1 = "Maecenas vel molestie ipsum, ac bibendum ex. Pellentesque porttitor, nisi id sodales lobortis, erat quam " \
    #         "ultrices neque, in sollicitudin elit dui in lacus. Phasellus ullamcorper dapibus arcu, ut eleifend turpis " \
    #         "imperdiet hendrerit. Nunc maximus nibh ut dictum gravida. Aenean vel turpis non lacus suscipit venenatis. " \
    #         "Morbi eu urna eleifend, finibus turpis in, ultricies justo. In pulvinar, leo eget lobortis gravida, " \
    #         "massa magna tempor nisi, blandit mollis lectus nisl ac mauris. Duis nec urna accumsan odio dapibus " \
    #         "gravida id eu nulla. Nam venenatis mi in erat euismod, ut aliquam quam lacinia. Proin dictum congue " \
    #         "condimentum. Phasellus aliquam efficitur orci, sit amet bibendum nibh pulvinar scelerisque. turpis " \
    #         "rhoncus feugiat. "
    # TEXT2 = "Vivamus sit amet fringilla metus, sit amet sodales quam. Sed porta justo risus, in convallis odio " \
    #         "fermentum non. Sed arcu purus, aliquet in pulvinar ut, feugiat id sapien. Pellentesque sit amet quam " \
    #         "consectetur turpis congue mattis eu ut nisi. Integer suscipit nisi at metus volutpat vulputate. Fusce " \
    #         "tempus tortor eu congue imperdiet. Nullam aliquam arcu ac ligula lacinia, eget blandit enim pharetra. " \
    #         "Mauris scelerisque tellus at turpis rhoncus feugiat. Integer quis vehicula velit. Curabitur mollis porta " \
    #         "gravida. Donec at faucibus nulla. Sed libero justo, egestas a eros quis, sodales varius mi. Aenean " \
    #         "semper blandit arcu, sed pellentesque justo blandit vitae. Maecenas elementum nulla tincidunt felis " \
    #         "efficitur rhoncus. Aliquam a pretium risus. Vestibulum et finibus ipsum. "
    # create_background_image(MAX_W, MAX_H)
    # write_text_on_image(TEXT1, TEXT2, MAX_W, MAX_H)
    # generate_wallpapers_for_first_surah()
    # generate_wallpapers_by_surah_number(2)
    for i in range(1, 115):
        print('Generating wallpapers for Surah ' + str(i) + ', please wait...')
        generate_wallpapers_by_surah_number(i)
        print("Successfully generated images for Surah " + str(i))
    pass
