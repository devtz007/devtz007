import os
import base64
import requests
import json

# Fetch WakaTime API key from environment variables
WAKATIME_API_KEY = os.getenv('WAKATIME_API_KEY')

if not WAKATIME_API_KEY:
    raise ValueError("WAKATIME_API_KEY environment variable is not set")

# Fetch data from WakaTime API
def fetch_wakatime_data():
    url = 'https://wakatime.com/api/v1/users/current/all_time_since_today'
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

# Inject the JSON data into the HTML template
def inject_data_into_html(template, data):
    # Convert data to JSON string and escape double quotes
    json_data = json.dumps(data).replace('"', '\\"')
    # Inject the JSON data into a script tag
    html_content = template.replace('{{jsonData}}', json_data)
    return html_content

# Update the README.md with the new HTML content
def update_readme(html_content):
    with open('README.md', 'r') as file:
        readme = file.readlines()

    start_marker = '<!--START_SECTION:index.html-->\n'
    end_marker = '<!--END_SECTION:index.html-->\n'
    
    try:
        start_index = readme.index(start_marker) + 1
        end_index = readme.index(end_marker)
    except ValueError:
        raise ValueError("Markers for the HTML section not found in README.md")

    readme[start_index:end_index] = [html_content + '\n']

    with open('README.md', 'w') as file:
        file.writelines(readme)

def main():
    print("Fetching WakaTime data...")
    try:
        data = fetch_wakatime_data()
        print("Data fetched successfully:", data)

        print("Reading HTML template...")
        template = read_html_template()
        print("Template read successfully")

        print("Injecting data into HTML template...")
        html_content = inject_data_into_html(template, data)
        print("HTML content generated successfully")

        print("Updating README.md...")
        update_readme(html_content)
        print("README.md updated successfully")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
