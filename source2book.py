"""
Script to convert a folder of source code examples into an eBook-ready html page
"""

from yaml import load, BaseLoader
import os


class SourceFile(str):
    """
    Class that define a source file to be processed
    """
    def __init__(self, filename):
        str.__init__(filename)
        self.extension = os.path.splitext(filename)[1][1:]


def main():
    """
    Main program
    """
    with open('config.yaml') as f:
        options = load(f, Loader=BaseLoader)
    sourcepath = options['sourcefolder']
    subfolders = options['subfolders']
    extensions = options['filter']
    for subfolder in subfolders:
        print('Chapter ' + subfolder)
        sourcefilelist = [SourceFile(entry.name)
                          for entry in os.scandir(os.path.join(sourcepath, subfolder))
                          if os.path.splitext(entry.name)[1][1:] in extensions]
        sourcefilelist.sort()
        print(sourcefilelist)


if __name__ == '__main__':
    main()
