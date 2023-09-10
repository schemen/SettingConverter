import os
import re
import pypandoc


def increment_header_levels(md_content):
    # Increment the level of each header by 2
    md_content = re.sub(r'^(#{1,6})', r'\1#', md_content, flags=re.MULTILINE)

    return md_content


def adjust_links(md_content, home_folder):
    # Replace relative links with absolute links for images, remove other links
    def repl(match):
        link_text = match.group(1)
        link_url = match.group(2)
        if link_url.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg')):
            link_url = os.path.normpath(os.path.join(home_folder, link_url))
            return f'[{link_text}]({link_url})'
        else:
            return link_text  # Remove link, keep link text

    md_content = re.sub(r'\[([^]]+)\]\(([^)]+)\)', repl, md_content)

    return md_content


def remove_toc(md_content):
    # Remove all lines containing [toc] or [TOC]
    md_content = re.sub(r'^.*\[(toc|TOC)\].*$', '', md_content, flags=re.MULTILINE)

    return md_content


def ensure_newline(md_content):
    # Replace single newline characters with two newline characters
    md_content = md_content.replace('\n', '\n\n')

    return md_content


def process_folder(folder_path):
    combined_md = ""
    used_headers = set()

    for root, dirs, files in os.walk(folder_path):
        title1 = os.path.basename(root)  # Use the folder name as level 1 title
        if title1 not in used_headers:
            combined_md += f"# {title1}\n\n"
            used_headers.add(title1)
        for file in files:
            if file.endswith('.md'):
                with open(os.path.join(root, file), 'r') as md_file:
                    md_content = md_file.read()
                    md_content = increment_header_levels(md_content)
                    md_content = adjust_links(md_content, root)
                    md_content = remove_toc(md_content)
                    md_content = ensure_newline(md_content)
                    title2 = os.path.splitext(file)[0]  # Use the file name as level 2 title
                    combined_md += f"## {title2}\n\n{md_content}\n\n"

    return combined_md


def process_folder_nobook(folder_path):
    combined_md = ""
    used_headers = set()

    for root, dirs, files in os.walk(folder_path):
        title1 = os.path.basename(root)  # Use the folder name as level 1 title
        if title1 not in used_headers:
            combined_md += f"# {title1}\n\n"
            used_headers.add(title1)
        for file in files:
            if file.endswith('.md'):
                with open(os.path.join(root, file), 'r') as md_file:
                    md_content = md_file.read()
                    md_content = increment_header_levels(md_content)
                    md_content = adjust_links(md_content, root)
                    md_content = remove_toc(md_content)
                    md_content = ensure_newline(md_content)
                    title2 = os.path.splitext(file)[0]  # Use the file name as level 2 title
                    combined_md += f"# {title2}\n\n{md_content}\n\n"

    return combined_md

def convert_md_to_odt(combined_md, output_odt_file):
    # Convert markdown to odt
    pypandoc.convert_text(combined_md, 'odt', format='md', outputfile=output_odt_file, extra_args=['--toc', '--reference-doc=reference.odt'])
    #pypandoc.convert_text(combined_md, 'odt', format='md', outputfile=output_odt_file, extra_args=['--toc', '--reference-doc=reference-dmnotes.odt'])


def write_to_file(content, output_file):
    with open(output_file, 'w') as f:
        f.write(content)


def main():
    folder_path = './toconvert'
    output_md_file = './combined.md'
    output_odt_file = './combined.odt'

    #combined_md = process_folder(folder_path)
    combined_md = process_folder_nobook(folder_path)
    write_to_file(combined_md, output_md_file)

    convert_md_to_odt(combined_md, output_odt_file)


if __name__ == "__main__":
    main()