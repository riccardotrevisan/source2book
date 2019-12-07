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
        self.htmlcode = ''

    def remove_header(self, nrows):
        self.content = ''.join(self.content.splitlines(keepends=True)[nrows:])

    def add_html_chapter(self):
        self.htmlcode += '<h2>\n' + self.filename + '\n</h2>\n'

    def add_html_body(self):
        self.htmlcode += '<pre>\n' + \
                         self.content.replace('&', '&amp;').\
                             replace('>', '&gt;').\
                             replace('<', '&lt;') + '</pre>\n'

    def compose_html(self):
        self.add_html_chapter()
        self.add_html_body()
        pass

    @staticmethod
    def add_html_header_footer(title, html_body):
        header = "<!DOCTYPE html>\n" \
                 "<html>\n" \
                 "<head><title>" + \
                 title + \
                 "</title></head>" \
                 "<body>\n"
        footer = "\n</body>\n" \
                 "</html>\n"
        return header + html_body + footer


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
    html_page_body = ''
    for subfolder in subfolders:
        sourcefilelist = [SourceFile(entry.path)
                          for entry in os.scandir(os.path.join(sourcepath, subfolder))
                          if os.path.splitext(entry.name)[1][1:] in extensions]
        sourcefilelist.sort()
        # Remove header
        html_page_body += '<h1>Chapter ' + subfolder + '</h1>\n'
        headingrows = int(options['headingrows'])
        for sourcefile in sourcefilelist:
            sourcefile.remove_header(headingrows)
            sourcefile.compose_html()
            html_page_body += sourcefile.htmlcode
            print('Processed file: ' + sourcefile)
    html_page_content = SourceFile.add_html_header_footer(options['title'], html_page_body)
    with open('output.html', 'w') as f:
        f.write(html_page_content)


if __name__ == '__main__':
    main()
