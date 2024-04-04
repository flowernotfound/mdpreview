import argparse
import os
import markdown

def main():
    parser = argparse.ArgumentParser(description='Markdown Preview Tool')
    parser.add_argument('file', type=str, help='Path to the Markdown file')
    parser.add_argument('--config', type=str, default=None, help='Path to the configuration file')
    parser.add_argument('--theme', type=str, default='default', help='Syntax highlighting theme')
    parser.add_argument('--toc', action='store_true', help='Generate table of contents')
    parser.add_argument('--no-highlight', action='store_true', help='Disable syntax highlighting')
    parser.add_argument('--no-pager', action='store_true', help='Disable pager')
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(f"Error: File '{args.file}' does not exist.")
        return

    # 読み込み
    try:
        with open(args.file, 'r') as f:
            md_content = f.read()
    except IOError as e:
        print(f"Error: Could not read the file '{args.file}'. {str(e)}")
        return

    # htmlに変換
    try:
        extensions = ['extra', 'smarty']
        if args.toc:
            extensions.append('toc')
        if not args.no_highlight:
            extensions.append('codehilite')
        html = markdown.markdown(md_content, extensions=extensions)
    except Exception as e:
        print(f"Error: Could not convert Markdown to HTML. {str(e)}")
        return

    print(html)

if __name__ == '__main__':
    main()