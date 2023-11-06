import os
import sys
import re
import mdformat

class DirectoryProcessor:
    def __init__(self, root_directory):
        self.root_directory = os.path.normpath(root_directory)
        self.markdown = ""
    
    def generate_table_of_contents(self):
        """Generates a Table of Contents based on headers in self.markdown."""
        toc_lines = ["# Table of Contents\n"]
        for line in self.markdown.splitlines():
            if line.startswith('#'):
                # Count the number of # to determine the indentation level
                indent_level = line.count('#') - 1
                # Clean the header to create a title
                title = line.lstrip('#').strip()
                # Create a ToC line
                toc_line = f"{'  ' * indent_level}* [{title}](#{title.lower().replace(' ', '-')})\n"
                toc_lines.append(toc_line)
        
        # Combine ToC lines and add a new line at the end
        toc = '\n'.join(toc_lines) + '\n\n'
        # Prepend the ToC to the markdown content
        self.markdown = toc + self.markdown

    def remove_frontmatter(self, content):
        """Removes the frontmatter from markdown content."""
        # Pattern to match frontmatter: lines between two sets of triple-dashes
        frontmatter_pattern = r'^---\s*\n.*?\n---\s*\n'
        # Remove the frontmatter using a non-greedy regex
        cleaned_content = re.sub(frontmatter_pattern, '', content, flags=re.DOTALL)
        return cleaned_content


    def save_markdown_to_file(self, output_path):
        """Saves the combined markdown content to a file."""
        formatted = mdformat.text(self.markdown)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(formatted)
        print(f"Markdown content saved to {output_path}")

    def depth_calculator(self, path):
        """Calculate the depth of a file or folder relative to the root folder."""
        relative_path = os.path.relpath(path, self.root_directory)
        return relative_path.count(os.sep)

    def process_file(self, file_path):
        """Processes a markdown file, adjusting header levels based on depth and adding an H1 header."""
        # Calculate depth of the file
        depth = self.depth_calculator(file_path)
        # Create the additional "#" string based on the depth
        # We add 1 because the depth does not account for the initial # for the H1 header
        additional_headers = "#" * depth

        # Extract the file name without the extension to use as the H1 header
        filename_header = os.path.splitext(os.path.basename(file_path))[0].replace('_', ' ')
        # The filename itself becomes an H1 header, with additional # added if depth > 0
        h1_header = f"{additional_headers}# {filename_header}\n\n" if depth > 0 else f"# {filename_header}\n\n"

        # Read the contents of the markdown file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Remove frontmatter
        content = self.remove_frontmatter(content)

        # First, increment all header levels by one
        content = re.sub(r'^(#+)', r'\1#', content, flags=re.MULTILINE)

        # Then, add additional "#" based on the depth to all headers including the adjusted ones
        if depth > 0:
            content = re.sub(r'^(#+)', r'\1' + additional_headers, content, flags=re.MULTILINE)

        # Combine the new H1 header with the modified content
        new_content = h1_header + content

        # Append the new content to the markdown accumulator
        self.markdown += new_content + "\n\n"  # Add some spacing between files
        print(f"Processing file: {file_path}, File depth: {self.depth_calculator(file_path)}")

    def process_folder(self, folder_path):
       """Processes a folder, creating a header from the folder name based on its depth."""
       # Calculate depth of the folder
       depth = self.depth_calculator(folder_path)
       # Create the additional "#" string based on the depth
       # We add 1 because the depth does not account for the initial # for the H1 header
       header_level = "#" * (depth + 1)

       # Extract the folder name to use as the header
       folder_name = os.path.basename(folder_path).replace('_', ' ')
        # The folder name becomes a header, with # added based on depth
       folder_header = f"{header_level} {folder_name}\n\n"

        # Append the folder header to the markdown accumulator
       self.markdown += folder_header
       print(f"Processing folder: {folder_path}, Folder depth: {self.depth_calculator(folder_path)}")
    
    def process_directory(self, directory):
        """Recursively processes all files and then all folders in a given directory."""
        for item in sorted(os.listdir(directory)):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                self.process_file(item_path)
        
        for item in sorted(os.listdir(directory)):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                self.process_folder(item_path)
                self.process_directory(item_path)
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory_path>")
        sys.exit(1)

    root_directory = sys.argv[1]
    if not os.path.isdir(root_directory):
        print("The provided path is not a directory.")
        sys.exit(1)

    processor = DirectoryProcessor(root_directory)
    processor.process_directory(root_directory)


    #ROOT_DIRECTORY  = "/home/elia/code/SettingConverter/setting_eteros"
    #processor = DirectoryProcessor(ROOT_DIRECTORY)
    #processor.process_directory(ROOT_DIRECTORY)
    
    # Generate a ToC if wanted
    processor.generate_table_of_contents()
    # Specify the output markdown file path
    output_md_path = 'combined_document.md'

    # Call the method to save the markdown content to a file
    processor.save_markdown_to_file(output_md_path)