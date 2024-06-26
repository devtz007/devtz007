# update_readme.py

def read_html_template():
    with open('templates/index.html', 'r') as file:
        return file.read()

def update_readme(html_content):
    # Read the current README
    with open('README.md', 'r') as file:
        readme = file.readlines()

    # Update the section where HTML should be inserted
    start_marker = '<!--START_SECTION:index.html-->\n'
    end_marker = '<!--END_SECTION:index.html-->\n'
    start_index = readme.index(start_marker) + 1
    end_index = readme.index(end_marker)

    # Replace existing content with new HTML content
    readme[start_index:end_index] = [html_content + '\n']

    # Write the updated README
    with open('README.md', 'w') as file:
        file.writelines(readme)

if __name__ == "__master__":
    html_content = read_html_template()
    update_readme(html_content)
