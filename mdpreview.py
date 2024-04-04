import argparse
import os
import markdown
import json
from pygments.formatters import HtmlFormatter

def main():
    parser = argparse.ArgumentParser(description='Markdown Preview Tool')
    parser.add_argument('file', type=str, help='Path to the Markdown file')
    parser.add_argument('--config', type=str, default=None, help='Path to the configuration file')
    parser.add_argument('--theme', type=str, default='default', help='Syntax highlighting theme')
    parser.add_argument('--toc', action='store_true', help='Generate table of contents')
    parser.add_argument('--no-highlight', action='store_true', help='Disable syntax highlighting')
    parser.add_argument('--no-pager', action='store_true', help='Disable pager')
    parser.add_argument('--output', type=str, default=None, help='Output file path')
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(f"Error: File '{args.file}' does not exist.")
        return

    # 設定の読み込み
    config = {}
    if args.config:
        try:
            with open(args.config, 'r') as f:
                config = json.load(f)
        except IOError as e:
            print(f"Error: Could not read the configuration file '{args.config}'. {str(e)}")
            return

    # 設定の適用
    theme = config.get('theme', args.theme)
    toc = config.get('toc', args.toc)
    highlight = config.get('highlight', not args.no_highlight)

    # mdの読み込み
    try:
        with open(args.file, 'r') as f:
            md_content = f.read()
    except IOError as e:
        print(f"Error: Could not read the file '{args.file}'. {str(e)}")
        return

    # HTMLに変換
    try:
        extensions = ['extra', 'smarty']
        if toc:
            extensions.append('toc')
        if highlight:
            extensions.append('codehilite')

        html = markdown.markdown(md_content, extensions=extensions)

        # スタイル追加
        if highlight:
            style = HtmlFormatter(style=theme).get_style_defs('.codehilite')
            html = f'<style>{style}</style>\n{html}'
    except Exception as e:
        print(f"Error: Could not convert Markdown to HTML. {str(e)}")
        return
    
    #ファイル出力
    output_path = args.output
    if output_path:
        try:
            with open(output_path, 'w') as f:
                f.write(html)
            print(f"Output saved to {output_path}")
        except IOError as e:
            print(f"Error: Could not write to the output file '{output_path}'. {str(e)}")
    else:
        print(html)

if __name__ == '__main__':
    main()