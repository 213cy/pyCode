from configuration import config

steps = [3,4,5]
steps = [6]

# step 1.
# edit configuration.py

# step 2.
if 2 in steps:
    from makewordsfile import create_words_file
    create_words_file(config)
    exit()

# step 3.
if 3 in steps:
    from makebackground import create_background_image
    img_back = create_background_image(config)
    img_back.show()
    from makecover import create_cover_image
    img_cover = create_cover_image(config)
    img_cover.show()

# step 4.
if 4 in steps:
    from downloadspeech import download_speechs
    download_speechs(config)

# step 5.
if 5 in steps:
    from main import Project
    maker = Project(config)

    maker.make_page_video()
    maker.make_final_video()
    print("done !!!")

if 6 in steps:
    print(config.regexp)
    with open(config.words_file, 'r', encoding="utf-8-sig") as f:
        line_list = f.readlines()
    words = (line.split(' ')[0] for line in line_list if line != '\n')
    d=sorted(set(words))
    print(' '.join(d))