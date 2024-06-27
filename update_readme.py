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

# Construct simplified HTML content with injected data
def construct_html_content(data):
    html_content = f"""
      <div>
        <h2>WakaTime Stats</h2>
        <p>Daily Average: {data.get('dailyAverage', 'N/A')}</p>
        <p>Total Time: {data.get('digital', 'N/A')}</p>
        <p>Start Date: {data.get('startDate', 'N/A')}</p>
        <p>End Date: {data.get('endDate', 'N/A')}</p>
        <p>Text: {data.get('text', 'N/A')}</p>
      </div>
    """
    return html_content

# Update the README.md with the new HTML content
def update_readme(html_content):
    try:
        with open('README.md', 'r', encoding='utf-8') as file:
            readme = file.readlines()
        
        start_marker = '<!--START_SECTION:wakatime-->\n'
        end_marker = '<!--END_SECTION:wakatime-->\n'
        
        start_index = readme.index(start_marker) + 1
        end_index = readme.index(end_marker)
        
        readme[start_index:end_index] = [html_content + '\n']
        
        with open('README.md', 'w', encoding='utf-8') as file:
            file.writelines(readme)
        
        print("README.md updated successfully")
        
    except ValueError:
        raise ValueError("Markers for the HTML section not found in README.md")
    except Exception as e:
        raise RuntimeError(f"Failed to update README.md: {e}")

def main():
    try:
        print("Fetching WakaTime data...")
        data = fetch_wakatime_data()
        print("Data fetched successfully:", data)

        print("Constructing HTML content...")
        html_content = construct_html_content(data)
        print("HTML content generated successfully")
        print("Generated HTML content:", html_content)

        print("Updating README.md...")
        update_readme(html_content)
        print("README.md updated successfully")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
