import re
import os

def markdown_to_html(markdown_file_path, output_file_path=None):
    """
    Convert markdown file to HTML using inline styles and sans-serif font.
    
    Args:
        markdown_file_path (str): Path to the markdown file
        output_file_path (str): Path for the output HTML file (optional)
    """
    
    # Read the markdown file
    with open(markdown_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse the content
    parsed_data = parse_markdown_content(content)
    
    # Generate HTML
    html_content = generate_html(parsed_data)
    
    # Determine output file path
    if output_file_path is None:
        base_name = os.path.splitext(markdown_file_path)[0]
        output_file_path = f"{base_name}.html"
    
    # Write HTML file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML file created: {output_file_path}")

def parse_markdown_content(content):
    """Parse markdown content into structured data."""
    lines = content.strip().split('\n')
    
    # Extract user name from greeting
    user_name = "User"
    greeting_match = re.search(r'### Good morning, (.+?)\.', content)
    if greeting_match:
        user_name = greeting_match.group(1)
    
    # Extract weather information
    weather_data = parse_weather_section(content)
    
    # Extract stories
    stories = parse_stories_section(content)
    
    return {
        'user_name': user_name,
        'weather': weather_data,
        'stories': stories
    }

def parse_weather_section(content):
    """Parse weather information from markdown."""
    weather_data = {}
    
    # Extract city name
    city_match = re.search(r'### Forecast for (.+?):', content)
    if city_match:
        weather_data['city'] = city_match.group(1)
    
    # Extract weather details
    patterns = {
        'current_temp': r'### Current Temperature: (.+)',
        'max_temp': r'### Max Temperature: (.+)',
        'min_temp': r'### Min Temperature: (.+)',
        'rain_chance': r'### Chance of Rain: (.+)',
        'aqi': r'### Air Quality Index \(AQI\): (.+)'
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, content)
        if match:
            weather_data[key] = match.group(1)
    
    return weather_data

def parse_stories_section(content):
    """Parse stories from markdown content."""
    stories = []
    
    # Find the stories section start
    stories_start = content.find("#### Here are your top stories for today.")
    if stories_start == -1:
        return stories
    
    # Get everything after the stories header
    stories_content = content[stories_start:]
    
    # Split by story boundaries - look for ## headings
    story_pattern = r'\n## (.+?)\n\n### (.+?)\n\n### What\'s happening: (.+?)\n\n### What\'s the context: (.+?)\n\n### Why it matters: (.+?)\n\n### What\'s next: (.+?)\n\n### TL;DR: (.+?)(?=\n## |\n### Thank you|$)'
    
    matches = re.findall(story_pattern, stories_content, re.DOTALL)
    
    for match in matches:
        story = {
            'heading': match[0].strip(),
            'subheading': match[1].strip(),
            'whats_happening': match[2].strip(),
            'whats_the_context': match[3].strip(),
            'why_it_matters': match[4].strip(),
            'whats_next': match[5].strip(),
            'tldr': match[6].strip()
        }
        stories.append(story)
    
    return stories

def parse_single_story(section):
    """Parse a single story from markdown section - DEPRECATED, kept for compatibility."""
    # This function is no longer used but kept to avoid breaking existing code
    return None

def generate_html(data):
    """Generate HTML from parsed data with inline styles."""
    
    # Generate weather section
    weather_html = ""
    if data['weather']:
        weather_html = f"""
            <div style="background-color: #fafafa; border: 1px solid #eee; padding: 15px; font-size: 14px; font-family: Arial, Helvetica, sans-serif;">
                <div style="font-weight: bold; margin-bottom: 10px;">Forecast for {data['weather'].get('city', 'Unknown')}:</div>
                <div style="margin-bottom: 5px;"><strong>Current Temperature:</strong> {data['weather'].get('current_temp', 'N/A')}</div>
                <div style="margin-bottom: 5px;"><strong>Max Temperature:</strong> {data['weather'].get('max_temp', 'N/A')}</div>
                <div style="margin-bottom: 5px;"><strong>Min Temperature:</strong> {data['weather'].get('min_temp', 'N/A')}</div>
                <div style="margin-bottom: 5px;"><strong>Chance of Rain:</strong> {data['weather'].get('rain_chance', 'N/A')}</div>
                <div style="margin-bottom: 5px;"><strong>Air Quality Index (AQI):</strong> {data['weather'].get('aqi', 'N/A')}</div>
            </div>"""
    
    # Generate stories HTML
    stories_html = ""
    for story in data['stories']:
        story_html = f"""
            <article style="margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid #eee;">
                <h3 style="font-size: 16px; font-weight: bold; color: #000; margin-bottom: 5px; font-family: Arial, Helvetica, sans-serif;">{story.get('heading', '')}</h3>
                <p style="font-size: 14px; color: #666; font-style: italic; margin-bottom: 15px; font-family: Arial, Helvetica, sans-serif;">{story.get('subheading', '')}</p>
                
                <div style="margin-bottom: 12px;">
                    <div style="font-weight: bold; color: #333; margin-bottom: 5px; font-family: Arial, Helvetica, sans-serif;">What's happening:</div>
                    <div style="color: #444; text-align: justify; font-family: Arial, Helvetica, sans-serif;">{story.get('whats_happening', '')}</div>
                </div>

                <div style="margin-bottom: 12px;">
                    <div style="font-weight: bold; color: #333; margin-bottom: 5px; font-family: Arial, Helvetica, sans-serif;">What's the context:</div>
                    <div style="color: #444; text-align: justify; font-family: Arial, Helvetica, sans-serif;">{story.get('whats_the_context', '')}</div>
                </div>

                <div style="margin-bottom: 12px;">
                    <div style="font-weight: bold; color: #333; margin-bottom: 5px; font-family: Arial, Helvetica, sans-serif;">Why it matters:</div>
                    <div style="color: #444; text-align: justify; font-family: Arial, Helvetica, sans-serif;">{story.get('why_it_matters', '')}</div>
                </div>

                <div style="margin-bottom: 12px;">
                    <div style="font-weight: bold; color: #333; margin-bottom: 5px; font-family: Arial, Helvetica, sans-serif;">What's next:</div>
                    <div style="color: #444; text-align: justify; font-family: Arial, Helvetica, sans-serif;">{story.get('whats_next', '')}</div>
                </div>

                <div style="background-color: #f9f9f9; border: 1px solid #ddd; padding: 10px; margin-top: 12px;">
                    <div style="font-weight: bold; color: #333; margin-bottom: 5px; font-family: Arial, Helvetica, sans-serif;">TL;DR:</div>
                    <div style="color: #444; text-align: justify; font-family: Arial, Helvetica, sans-serif;">{story.get('tldr', '')}</div>
                </div>
            </article>"""
        stories_html += story_html
    
    # Remove border-bottom from last story
    if stories_html:
        stories_html = stories_html.replace('style="margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid #eee;">', 'style="margin-bottom: 30px; padding-bottom: 20px;">', 1)
    
    # Complete HTML template with inline styles
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily News - {data['user_name']}</title>
</head>
<body style="font-family: Arial, Helvetica, sans-serif; line-height: 1.5; color: #333; margin: 0; padding: 20px; background-color: #ffffff;">
    <div style="max-width: 600px; margin: 0 auto; background-color: white; border: 1px solid #ddd;">
        <div style="background-color: #f5f5f5; padding: 20px; border-bottom: 1px solid #ddd;">
            <h1 style="font-size: 18px; font-weight: normal; margin: 0 0 15px 0; color: #333; font-family: Arial, Helvetica, sans-serif;">Good morning, {data['user_name']}.</h1>
            {weather_html}
        </div>

        <div style="padding: 20px;">
            <h2 style="font-size: 16px; font-weight: bold; color: #333; margin-bottom: 20px; border-bottom: 1px solid #ddd; padding-bottom: 5px; font-family: Arial, Helvetica, sans-serif;">Here are your top stories for today.</h2>
            {stories_html}
        </div>

        <div style="background-color: #f5f5f5; text-align: center; padding: 15px; font-size: 14px; border-top: 1px solid #ddd; color: #666; font-family: Arial, Helvetica, sans-serif;">
            Thank you for reading.
        </div>
    </div>
</body>
</html>"""
    
    return html_template

# Example usage
if __name__ == "__main__":
    # Convert James.md to James.html
    markdown_to_html("Pragyam.md")
    
    # Or specify custom output path
    # markdown_to_html("James.md", "custom_output.html")