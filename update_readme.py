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
    # Replace with your SVG construction logic
    svg_content = f"""
    <svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
        <foreignObject width="100" height="100">
            <div xmlns="http://www.w3.org/1999/xhtml">
                <!-- Replace with your SVG content based on WakaTime data -->
                <h2>WakaTime Stats</h2>
                <p>Daily Average: {data['daily_average']}</p>
                <p>Total Time: {data['digital']}</p>
                <p>Start Date: {data['range']['start_date']}</p>
                <p>End Date: {data['range']['end_date']}</p>
                <p>Text: {data['text']}</p>
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
def update_readme_with_svg(username):
    try:
        svg_url = f"![WakaTime Stats](https://raw.githubusercontent.com/{username}/master/wakatime-stats.svg)"
        with open('README.md', 'r', encoding='utf-8') as file:
            readme = file.readlines()

        start_marker = '<!--START_SECTION:wakatime-->\n'
        end_marker = '<!--END_SECTION:wakatime-->\n'

        if start_marker not in readme or end_marker not in readme:
            raise ValueError("Markers for the section not found in README.md")

        start_index = readme.index(start_marker) + 1
        end_index = readme.index(end_marker)

        readme[start_index:end_index] = [f"\n### WakaTime Stats 📊\n\n{svg_url}\n\n"]

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
        
        # Update README.md only if save successful
        print("Updating README.md with SVG URL...")
        update_readme_with_svg("devtz007")  # Replace with dynamic username fetching

        print("README.md updated successfully")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
