import os
import base64
import requests
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

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

    for _ in range(5):  # Retry up to 5 times
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            if response.status_code == 429:  # Rate limit error
                logging.info("Rate limit hit, waiting before retrying...")
                time.sleep(60)  # Wait before retrying
            else:
                raise
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Request error: {req_err}")
            time.sleep(5)  # Wait before retrying on other errors

# Construct SVG content
def construct_svg_content(data):
    data = data.get('data', {})
    text = data.get('text', 'N/A')
    start_date = data.get('range', {}).get('start_date', 'N/A')
    end_date = data.get('range', {}).get('end_date', 'N/A')

    svg_content = f"""<svg width="100%" height="auto" xmlns="http://www.w3.org/2000/svg">
        <foreignObject width="100%" height="100%">
            <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: Arial, sans-serif; font-size: 14px;">
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
        html_img_tag = f'<div class="wakatime_container" style="width: 100%;">\n  {svg_content}\n</div>\n'
        
        with open('README.md', 'r', encoding='utf-8') as file:
            readme = file.readlines()

        # Update WakaTime section
        start_marker_wakatime = '<!--START_SECTION:wakatime_all_time_since_today-->\n'
        end_marker_wakatime = '<!--END_SECTION:wakatime_all_time_since_today-->\n'

        if start_marker_wakatime not in readme or end_marker_wakatime not in readme:
            raise ValueError("Markers for the WakaTime section not found in README.md")

        start_index_wakatime = readme.index(start_marker_wakatime) + 1
        end_index_wakatime = readme.index(end_marker_wakatime)

        # Update the section with SVG content
        readme[start_index_wakatime:end_index_wakatime] = [html_img_tag]

        # Write back to README.md
        with open('README.md', 'w', encoding='utf-8') as file:
            file.writelines(readme)

        logging.info("README.md updated successfully")

    except ValueError as ve:
        logging.error(f"ValueError: {ve}")
    except Exception as e:
        logging.error(f"Failed to update README.md: {e}")

def main():
    try:
        logging.info("Fetching WakaTime data...")
        data = fetch_wakatime_data()
        logging.info("Data fetched successfully")

        logging.info("Constructing SVG content...")
        svg_content = construct_svg_content(data)
        logging.info("SVG content generated successfully")

        logging.info("Updating README.md with SVG content...")
        update_readme_with_svg(svg_content)

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
    
