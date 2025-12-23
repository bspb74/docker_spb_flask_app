import os


def iterate_over_images(directory):
    fnameList = []
    for fname in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, fname)):
            print(fname)
            fnameList.append(fname)
    return fnameList

if __name__ == "__main__":

    directory = "C:/Users/Carey/lightburn/bbb_business/board_images"
    fnames = iterate_over_images(directory)
    print(fnames)

