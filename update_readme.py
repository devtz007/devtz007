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
    daily_average = data.get('daily_average', 'N/A')
    digital = data.get('digital', 'N/A')
    start_date = data.get('range', {}).get('start_date', 'N/A')
    end_date = data.get('range', {}).get('end_date', 'N/A')
    text = data.get('text', 'N/A')

    svg_content = f"""
    <svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
        <foreignObject width="100%" height="100%">
    <div xmlns="http://www.w3.org/1999/xhtml">

                <h1 style="color: #2e6c80;">WakaTime Stats</h1>
                <p style="font-weight: bold;">Daily Average: {daily_average}</p>
                <p style="font-weight: bold;">Total Time: {digital}</p>
                <p style="font-weight: bold;">Start Date: {start_date}</p>
                <p style="font-weight: bold;">End Date: {end_date}</p>
                <p style="font-weight: bold;">Text: {text}</p>
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

# Update the README.md with SVG URL
def update_readme_with_svg():
    try:
        username = "devtz007"
        repo_name = "devtz007"  # Adjust if your repository name is different
        svg_url = f"https://{username}.github.io/{repo_name}/wakatime-stats.svg"
        markdown_link = f"\n### WakaTime Stats 📊\n\n![WakaTime Stats]({svg_url})\n\n"
        
        with open('README.md', 'r', encoding='utf-8') as file:
            readme = file.readlines()

        start_marker = '<!--START_SECTION:wakatime-->\n'
        end_marker = '<!--END_SECTION:wakatime-->\n'

        if start_marker not in readme or end_marker not in readme:
            raise ValueError("Markers for the section not found in README.md")

        start_index = readme.index(start_marker) + 1
        end_index = readme.index(end_marker)

        readme[start_index:end_index] = [markdown_link]

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

        print("Saving SVG to file...")
        save_svg_to_file(svg_content)

        print("Updating README.md with SVG URL...")
        update_readme_with_svg()

        print("README.md updated successfully")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
