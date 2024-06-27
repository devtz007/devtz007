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

# Construct HTML content with injected data
def construct_html_content(data):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <title>State Reader</title>
      <style></style>
    </head>
    <body>
      <div class="state-container">
        <h2>State Reader</h2>
        <div id="result">
          <div class="daily-average">
            {data['dailyAverage']}
          </div>
          <div class="digital">
            {data['digital']}
          </div>
          <div class="dates-range">
            <div class="start">
              {data['startDate']}
            </div>
            <div class="end">
              {data['endDate']}
            </div>
          </div>
          <div class="text">
            {data['text']}
          </div>
        </div>
      </div>

      <script>
        const jsonData = '{json.dumps(data).replace("'", "\\'")}';
        const parsedData = JSON.parse(jsonData.replace(/\\\\"/g, '"'));
        const Result = document.getElementById("result");
        Result.innerHTML = `
          <div class="daily-average">
            ${parsedData.dailyAverage}
          </div>
          <div class="digital">
            ${parsedData.digital}
          </div>
          <div class="dates-range">
            <div class="start">
              ${parsedData.startDate}
            </div>
            <div class="end">
              ${parsedData.endDate}
            </div>
          </div>
          <div class="text">
            ${parsedData.text}
          </div>
        `;
      </script>
    </body>
    </html>
    """
    return html_content

# Update the README.md with the new HTML content
def update_readme(html_content):
    try:
        with open('README.md', 'r', encoding='utf-8') as file:
            readme = file.readlines()
        
        start_marker = '<!--START_SECTION:index.html-->\n'
        end_marker = '<!--END_SECTION:index.html-->\n'
        
        start_index = readme.index(start_marker) + 1
        end_index = readme.index(end_marker)
        
        readme[start_index:end_index] = [html_content + '\n']
        
        with open('README.md', 'w', encoding='utf-8') as file:
            file.writelines(readme)
        
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

        print("Updating README.md...")
        update_readme(html_content)
        print("README.md updated successfully")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
