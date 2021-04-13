import os
from collections import Counter

def main():
    path = os.getcwd()+'/photo'
    print(path)
    print("There is 2 mods. Info and main.\nIn info mode, i will show stats about photos to be proced."
          "\nIn main mode script will apply this changes. \nInfo/Main?")
    arg = input()

    if arg == 'Info':
        print("Good decision!\n")
        draw_counter = 0
        sig_count = 0
        photo_tag_count = 0
        other_count = 0
        files_count = 0

        folder_list = os.listdir(path)
        print("There is " + str(len(folder_list)) + " folders.")
        extensions = list()
        for folder in folder_list:

            photo_list = os.listdir(path + "/" + folder)
            files_count += len(photo_list)
            for photo in photo_list:
                ext = photo.split(".")[-1]
                extensions.append(photo.split(".")[-1])
                if photo.find("photo") !=-1:
                    photo_tag_count += 1
                elif photo.find("draw") !=-1:
                    draw_counter += 1
                elif photo.find("insig") !=-1:
                    sig_count += 1
                else:
                    other_count += 1

        print(Counter(extensions).keys(), Counter(extensions).values())
        print("Photos at all: {0}.\nTag photo: {1}.\nDrawing count: {2}.\nSig count: {3}.\nOther photos: {4}".
              format(files_count, photo_tag_count, draw_counter, sig_count, other_count))
        return 0

    if arg == "Main":
        print("Ok, let's do it!")
        folder_list = os.listdir(path)
        print("There is " + str(len(folder_list)) + " folders.")
        for folder in folder_list:
            print(folder)
            photo_list = os.listdir(path + "/" + folder)
            for photo in photo_list:
                photo_path = path + "/" + folder + "/" + photo
                # if photo.find("photo") != -1:
                # elif photo.find("draw") != -1:
                # elif photo.find("insig") != -1:
                # else:
                #     other_count += 1
            return 0

        return 0

    print("Oh, senpai! :(")

if __name__ == "__main__":
    main()