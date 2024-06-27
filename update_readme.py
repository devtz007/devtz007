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

# Construct SVG content with inline styles
def construct_svg_content(data):
    # Access nested data correctly
    data = data.get('data', {})
    daily_average = data.get('daily_average', 'N/A')
    digital = data.get('digital', 'N/A')
    start_date = data.get('range', {}).get('start_date', 'N/A')
    end_date = data.get('range', {}).get('end_date', 'N/A')
    text = data.get('text', 'N/A')

    svg_content = f"""
    <svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
        <foreignObject width="100%" height="100%">
            <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: Arial, sans-serif; font-size: 14px;">
                <h2 style="color: #2e6c80;">WakaTime Stats</h2>
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
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(svg_content)
        print(f"SVG saved to {filename}")
    except Exception as e:
        print(f"Failed to save SVG to {filename}: {e}")

# Function to verify if SVG file exists and contains content
def verify_svg_file():
    filename = 'wakatime-stats.svg'
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            svg_content = file.read()
        print(f"SVG file '{filename}' exists and contains:\n")
        print(svg_content)
    else:
        print(f"SVG file '{filename}' not found.")

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
        
        # Verify SVG file after saving
        verify_svg_file()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
