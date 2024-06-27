import os
import base64
import requests

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

# Construct Markdown content
def construct_markdown_content(data):
    # Access nested data correctly
    data = data.get('data', {})
    daily_average = data.get('daily_average', 'N/A')
    digital = data.get('digital', 'N/A')
    start_date = data.get('range', {}).get('start_date', 'N/A')
    end_date = data.get('range', {}).get('end_date', 'N/A')
    text = data.get('text', 'N/A')

    markdown_content = f"""
### WakaTime Stats

- **Daily Average:** {daily_average}
- **Total Time:** {digital}
- **Start Date:** {start_date}
- **End Date:** {end_date}
- **Text:** {text}
"""
    return markdown_content

# Update the README.md with Markdown content
def update_readme(markdown_content):
    try:
        with open('README.md', 'r', encoding='utf-8') as file:
            readme = file.readlines()

        start_marker = '<!--START_SECTION:wakatime-->\n'
        end_marker = '<!--END_SECTION:wakatime-->\n'

        if start_marker not in readme or end_marker not in readme:
            raise ValueError("Markers for the section not found in README.md")

        start_index = readme.index(start_marker) + 1
        end_index = readme.index(end_marker)

        readme[start_index:end_index] = [markdown_content + '\n']

        with open('README.md', 'w', encoding='utf-8') as file:
            file.writelines(readme)

        print("README.md updated successfully")

    except ValueError as ve:
        print(f"ValueError: {ve}")
    except Exception as e:
        print(f"Failed to update README.md: {e}")

def main():
    try:
        print("Fetching WakaTime data...")
        data = fetch_wakatime_data()
        print("Data fetched successfully:", data)

        print("Constructing Markdown content...")
        markdown_content = construct_markdown_content(data)
        print("Markdown content generated successfully")
        print("Generated Markdown content:")
        print(markdown_content)

        print("Updating README.md...")
        update_readme(markdown_content)
        print("README.md updated successfully")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
