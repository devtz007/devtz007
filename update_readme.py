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

# Generate ratio bar
total_seconds = sum(language['total_seconds'] for language in languages)
ratio_bar = '\n'.join(
    f"{language['name']}: {'█' * int((language['total_seconds'] / total_seconds) * 40)} {language['percent']}%"
    for language in languages
)

# Read the current README
with open('README.md', 'r') as file:
    readme = file.readlines()

# Update the WakaTime section
start_index = readme.index('<!--START_SECTION:waka-->\n')
end_index = readme.index('<!--END_SECTION:waka-->\n')
readme[start_index + 1:end_index] = [ratio_bar + '\n']

# Write the updated README
with open('README.md', 'w') as file:
    file.writelines(readme)
