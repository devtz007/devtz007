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

# Construct SVG content
def construct_svg_content(data):
    data = data.get('data', {})
    text = data.get('text', 'N/A')
    start_date = data.get('range', {}).get('start_date', 'N/A')
    end_date = data.get('range', {}).get('end_date', 'N/A')

    svg_content = f"""<svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
        <foreignObject width="100%" height="100%">
            <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: Arial, sans-serif; font-size: 14px;">
                <h2 style="color: #2e6c80;">WakaTime Stats</h2>
                <p style="font-weight: bold;">Code times: {text}</p>
                <p style="font-weight: bold;">Start Date: {start_date}</p>
                <p style="font-weight: bold;">End Date: {end_date}</p>
            </div>
        </foreignObject>
    </svg>"""
    return svg_content

# Update the README.md with SVG content
def update_readme_with_svg(svg_content):
    try:
        # HTML content to embed SVG
        html_img_tag = f'<div style="width: 100%;">\n  {svg_content}\n</div>\n'
        
        with open('README.md', 'r', encoding='utf-8') as file:
            readme = file.readlines()

        start_marker = '<!--START_SECTION:wakatime_all_time_since_today-->\n'
        end_marker = '<!--END_SECTION:wakatime_all_time_since_today-->\n'

        if start_marker not in readme or end_marker not in readme:
            raise ValueError("Markers for the section not found in README.md")

        start_index = readme.index(start_marker) + 1
        end_index = readme.index(end_marker)

        readme[start_index:end_index] = [html_img_tag]

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

        print("Constructing SVG content...")
        svg_content = construct_svg_content(data)
        print("SVG content generated successfully")

        print("Updating README.md with SVG content...")
        update_readme_with_svg(svg_content)

        print("README.md updated successfully")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
