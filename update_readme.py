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

# Construct SVG content with embedded HTML
def construct_svg_content(data):
    # Access nested data correctly
    data = data.get('data', {})
    daily_average = data.get('daily_average', 'N/A')
    digital = data.get('digital', 'N/A')
    start_date = data.get('range', {}).get('start_date', 'N/A')
    end_date = data.get('range', {}).get('end_date', 'N/A')
    text = data.get('text', 'N/A')

    svg_content = f"""
    <svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
        <foreignObject width="100%" height="100%">
            <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: Arial, sans-serif;">
                <h2 style="color: #2e6c80;">WakaTime Stats 📊</h2>
                <p><strong>Daily Average:</strong> {daily_average}</p>
                <p><strong>Total Time:</strong> {digital}</p>
                <p><strong>Start Date:</strong> {start_date}</p>
                <p><strong>End Date:</strong> {end_date}</p>
                <p><strong>Text:</strong> {text}</p>
            </div>
        </foreignObject>
    </svg>
    """
    return svg_content

# Save SVG content to file
def save_svg_to_file(svg_content, filename='wakatime-stats.svg'):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(svg_content)
    print(f"SVG saved to {filename}")

# Update README.md with dynamic SVG link
def update_readme_with_svg_link():
    svg_link = "https://raw.githubusercontent.com/username/repository/main/wakatime-stats.svg"
    markdown_content = f"""
### WakaTime Stats 📊

![WakaTime Stats]({svg_link})
"""
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

        print("README.md updated successfully with SVG link")

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
        print("Generated SVG content:")
        print(svg_content)

        print("Saving SVG to file...")
        save_svg_to_file(svg_content)

        print("Updating README.md with SVG link...")
        update_readme_with_svg_link()
        print("README.md updated successfully with SVG link")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
