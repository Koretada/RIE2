import json
import argparse
from collections import defaultdict
import plotly.graph_objects as go
import plotly.io as pio
import tldextract

def extract_primary_domain(mx_record):
    extracted = tldextract.extract(mx_record)
    primary_domain = f"{extracted.domain}.{extracted.suffix}" if extracted.suffix else extracted.domain
    return primary_domain.lower()  # Convert to lowercase

def process_mx_records(file_path):
    mx_popularity = defaultdict(int)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    record = json.loads(line)
                    if 'answers' in record['data']:
                        for answer in record['data']['answers']:
                            if answer['type'] == 'MX':
                                mx_record = answer['answer'].split()[-1].strip('.')
                                primary_domain = extract_primary_domain(mx_record)
                                mx_popularity[primary_domain] += 1
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    return mx_popularity

# Parse arguments
parser = argparse.ArgumentParser(description="Process MX records.")
parser.add_argument('file_path', type=str, help='Path to the input JSON file')
parser.add_argument('--top', type=int, default=100, help='Number of top MX providers to display')
args = parser.parse_args()

# Process the records
mx_stats = process_mx_records(args.file_path)

# Sort MX domains by popularity in descending order and slice the top providers
sorted_mx_stats = sorted(mx_stats.items(), key=lambda item: item[1], reverse=True)[:args.top]

# Visualization
fig = go.Figure(data=[go.Bar(x=[count for _, count in sorted_mx_stats], y=[domain for domain, _ in sorted_mx_stats], orientation='h')])
fig.update_layout(title="Top MX Record Popularity by Provider",
                  xaxis_title="Count",
                  yaxis_title="MX Provider",
                  yaxis={'autorange': 'reversed'})  # Reverse the order of the y-axis
pio.write_html(fig, file='output.html')  # Save the figure to an HTML file
