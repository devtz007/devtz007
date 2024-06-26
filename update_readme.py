import requests
import os

# Get WakaTime API key from environment variables
api_key = os.getenv('WAKATIME_API_KEY')

# Fetch WakaTime stats
url = f'https://wakatime.com/api/v1/users/current/stats/last_7_days?api_key={api_key}'
response = requests.get(url)
data = response.json()

# Extract the necessary data
languages = data['data']['languages']

# Generate HTML content with custom theme
html_content = '''
<div id="wakatime-stats" style="font-family: Arial, sans-serif;">
  <h2>WakaTime Stats</h2>
  <div class="language-stats">
'''

for language in languages:
    html_content += f'''
    <div style="margin-bottom: 10px;">
      <span style="display: inline-block; width: 100px;">{language['name']}</span>
      <div style="display: inline-block; width: 200px; background: linear-gradient(90deg, #ff4500 {language['percent']}%, #ddd {language['percent']}%); height: 20px; border-radius: 5px;"></div>
      <span style="margin-left: 10px;">{language['percent']}%</span>
    </div>
    '''

html_content += '''
  </div>
  <script>
    // Add your JavaScript here if needed
  </script>
  <style>
    /* Add your CSS here if needed */
  </style>
</div>
'''

# Read the current README
with open('README.md', 'r') as file:
    readme = file.readlines()

# Update the WakaTime section
start_index = readme.index('<!--START_SECTION:waka-->\n')
end_index = readme.index('<!--END_SECTION:waka-->\n')
readme[start_index + 1:end_index] = [html_content + '\n']

# Write the updated README
with open('README.md', 'w') as file:
    file.writelines(readme)
