import requests
import os

# Get WakaTime API key from environment variables
api_key = os.getenv('WAKATIME_API_KEY')

# Fetch WakaTime stats for last 7 days
url = f'https://wakatime.com/api/v1/users/current/stats/last_7_days?api_key={api_key}'
response = requests.get(url)
data = response.json()

# Fetch repository code percentages
url_repos = f'https://wakatime.com/api/v1/users/current/commits?api_key={api_key}'
response_repos = requests.get(url_repos)
data_repos = response_repos.json()

# Extract languages and their percentages from WakaTime stats
languages = data['data']['languages']

# Extract repository data
repos = data_repos['data']

# Generate HTML content for custom section
html_content = '''
<div id="custom-stats" style="font-family: Arial, sans-serif;">
  <h2>Custom Stats</h2>
  <div class="language-stats">
    <h3>Code Time (Last 7 Days)</h3>
    <ul>
'''

# Add code time data
for language in languages:
    html_content += f'''
      <li>{language['name']}: {language['text']}</li>
    '''

html_content += '''
    </ul>
    <h3>Repository Code Percentages</h3>
    <ul>
'''

# Add repository code percentages
for repo in repos:
    html_content += f'''
      <li>{repo['repo']}: {repo['percent']}%</li>
    '''

html_content += '''
    </ul>
  </div>
  <style>
    /* Add your CSS here */
    #custom-stats {
      background-color: #f0f0f0;
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .language-stats {
      margin-top: 20px;
    }
    .language-stats ul {
      list-style-type: none;
      padding: 0;
    }
    .language-stats ul li {
      margin-bottom: 10px;
    }
  </style>
</div>
'''

# Write the HTML content to a file
with open('custom_stats.html', 'w') as file:
    file.write(html_content)
