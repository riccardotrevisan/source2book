"""
Script to convert a folder of source code examples into an eBook-ready html page
"""

from yaml import load, BaseLoader
import os


class SourceFile(str):
    """
    Class that defines a source file to be processed
    """
    def __init__(self, filepath):
        str.__init__(self)
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.extension = os.path.splitext(self.filename)[1][1:]
        with open(filepath, 'r') as f:
            self.content = f.read()

    def remove_header(self, nrows):
        self.content = ''.join(self.content.splitlines()[nrows:])


def main():
    """
    Main program
    """
    # Read globals
    with open('config.yaml') as f:
        options = load(f, Loader=BaseLoader)
    sourcepath = options['sourcefolder']
    subfolders = options['subfolders']
    extensions = options['filter']
    # Compose file list
    for subfolder in subfolders:
        # print('Chapter ' + subfolder)
        sourcefilelist = [SourceFile(entry.path)
                          for entry in os.scandir(os.path.join(sourcepath, subfolder))
                          if os.path.splitext(entry.name)[1][1:] in extensions]
        sourcefilelist.sort()
        # Remove header
        headingrows = int(options['headingrows'])
        for sourcefile in sourcefilelist:
            sourcefile.remove_header(headingrows)
            print('Processed file: ' + sourcefile)


if __name__ == '__main__':
    main()
