import os

'''
Standalone function that renames files placed in the dump folder
'''

def rename():
    os.getcwd()
    os.chdir("static")
    os.chdir("images")
    os.chdir("dump")
    Directory = os.getcwd() + "/"
    for count, filename in enumerate(os.listdir(Directory)):
        final = "pic" + str(count) + ".jpg"
        source = Directory + filename
        final = Directory + final

        os.rename(source, final)

if __name__ == '__main__':
    rename()