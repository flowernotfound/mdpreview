import argparse
import os
import markdown
import json
from pygments.formatters import HtmlFormatter

DEFAULT_THEME = 'default'
DEFAULT_TOC = False
DEFAULT_HIGHLIGHT = True
CONFIG_ERROR_MESSAGE = "Could not read the configuration file '{config_path}'. {error}"
FILE_READ_ERROR_MESSAGE = "Could not read the file '{file_path}'. {error}"
FILE_WRITE_ERROR_MESSAGE = "Could not write to the output file '{output_path}'. {error}"
FILE_NOT_FOUND_ERROR_MESSAGE = "File '{file_path}' does not exist."

class Config:
    def __init__(self, config_path=None, theme=DEFAULT_THEME, toc=DEFAULT_TOC, highlight=DEFAULT_HIGHLIGHT):
        self.theme = theme
        self.toc = toc
        self.highlight = highlight

        if config_path:
            self.load_from_file(config_path)

    def load_from_file(self, config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                self.theme = config.get('theme', self.theme)
                self.toc = config.get('toc', self.toc)
                self.highlight = config.get('highlight', self.highlight)
        except IOError as e:
            raise ConfigError(CONFIG_ERROR_MESSAGE.format(config_path=config_path, error=str(e)))

def parse_arguments():
    parser = argparse.ArgumentParser(description='Markdown Preview Tool')
    parser.add_argument('file', type=str, help='Path to the Markdown file')
    parser.add_argument('--config', type=str, default=None, help='Path to the configuration file')
    parser.add_argument('--theme', type=str, default=DEFAULT_THEME, help='Syntax highlighting theme')
    parser.add_argument('--toc', action='store_true', help='Generate table of contents')
    parser.add_argument('--no-highlight', action='store_true', help='Disable syntax highlighting')
    parser.add_argument('--no-pager', action='store_true', help='Disable pager')
    parser.add_argument('--output', type=str, default=None, help='Output file path')
    return parser.parse_args()

def read_markdown_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except IOError as e:
        raise FileReadError(FILE_READ_ERROR_MESSAGE.format(file_path=file_path, error=str(e)))

def convert_markdown_to_html(md_content, config):
    extensions = ['extra', 'smarty']
    if config.toc:
        extensions.append('toc')
    if config.highlight:
        extensions.append('codehilite')

    html = markdown.markdown(md_content, extensions=extensions)

    if config.highlight:
        style = HtmlFormatter(style=config.theme).get_style_defs('.codehilite')
        html = f'<style>{style}</style>\n{html}'

    return html

def save_html_to_file(html, output_path):
    try:
        with open(output_path, 'w') as f:
            f.write(html)
        print(f"Output saved to {output_path}")
    except IOError as e:
        raise FileWriteError(FILE_WRITE_ERROR_MESSAGE.format(output_path=output_path, error=str(e)))

class Error(Exception):
    pass

class ConfigError(Error):
    pass

class FileReadError(Error):
    pass

class FileWriteError(Error):
    pass

class FileNotFoundError(Error):
    pass

def main():
    args = parse_arguments()

    try:
        if not os.path.isfile(args.file):
            raise FileNotFoundError(FILE_NOT_FOUND_ERROR_MESSAGE.format(file_path=args.file))

        config = Config(args.config, args.theme, args.toc, not args.no_highlight)
        md_content = read_markdown_file(args.file)
        html = convert_markdown_to_html(md_content, config)

        if args.output:
            save_html_to_file(html, args.output)
        else:
            print(html)
    except Error as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()