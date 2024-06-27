import os
import base64
import requests

# Fetch WakaTime API key from environment variables
WAKATIME_API_KEY = os.getenv('WAKATIME_API_KEY')

# Fetch data from WakaTime API
def fetch_wakatime_data():
    url = 'https://wakatime.com/api/v1/users/current/status_bar/today'
    headers = {
        'Authorization': f'Basic {base64.b64encode(f"{WAKATIME_API_KEY}:".encode()).decode()}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Read the HTML template from index.html
def read_html_template():
    with open('templates/index.html', 'r') as file:
        return file.read()

# Inject the fetched data into the HTML template
def inject_data_into_html(template, data):
    html_content = template
    html_content = html_content.replace('{{totalCodingTime}}', data['data']['grand_total']['text'])
    html_content = html_content.replace('{{codingHours}}', f"{data['data']['categories'][0]['hours']} hrs")
    html_content = html_content.replace('{{codingMinutes}}', f"{data['data']['categories'][0]['minutes']} mins")

    languages_html = ""
    for lang in data['data']['languages']:
        languages_html += f"<li>{lang['name']}: {lang['text']}</li>"
    html_content = html_content.replace('{{languagesList}}', languages_html)

    projects_html = ""
    for proj in data['data']['projects']:
        projects_html += f"<li>{proj['name']}: {proj['text']}</li>"
    html_content = html_content.replace('{{projectsList}}', projects_html)

    return html_content

# Update the README.md with the new HTML content
def update_readme(html_content):
    with open('README.md', 'r') as file:
        readme = file.readlines()

    start_marker = '<!--START_SECTION:index.html-->\n'
    end_marker = '<!--END_SECTION:index.html-->\n'
    start_index = readme.index(start_marker) + 1
    end_index = readme.index(end_marker)

    readme[start_index:end_index] = [html_content + '\n']

    with open('README.md', 'w') as file:
        file.writelines(readme)

def main():
    data = fetch_wakatime_data()
    template = read_html_template()
    html_content = inject_data_into_html(template, data)
    update_readme(html_content)

if __name__ == "__main__":
    main()
