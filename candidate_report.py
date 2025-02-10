import pandas as pd
from jinja2 import Environment, FileSystemLoader
import os
from matplotlib import pyplot as plt
import plotly.graph_objects as go

def generate_skill_chart(candidate, output_path):
    skills = [
        'Communication', 'Rapport Building', 'Analytical Ability',
        'Curiosity', 'Knowledge', 'Enthusiasm', 'Discipline'
    ]
    scores = [
        candidate['Communication'], candidate['Rapport Building'], candidate['Analytical Ability'],
        candidate['Curiosity'], candidate['Knowledge'], candidate['Enthusiasm'], candidate['Discipline']
    ]

    plt.figure(figsize=(16, 5.7))  # Set figure size
    bars = plt.barh(skills, scores, color='#00BFFF', edgecolor=None)  # Use a specific color

    # Add labels and title
    plt.xlim(0, 100)

    plt.rcParams["font.family"] = "Times New Roman"

    plt.yticks(fontsize=24, fontweight='bold')
    # plt.xticks(fontsize=16, fontweight='bold')

    # Adjust the x-axis limits to allocate space for skill names
    plt.subplots_adjust(left=0.3, right=0.9, top=0.9, bottom=0.1)  # Adjust margins to converge the chart

    # Add data labels for skill values only
    # for bar in bars:
    #     plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, 
    #              f'{bar.get_width()}', va='center', fontsize=12, color='black')

    ax = plt.gca()
 # Set background color

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    chart_path = os.path.join(output_path, f"{candidate['Name']}_skills.png")
    plt.tight_layout()
    plt.savefig(chart_path, transparent=True)
    plt.close()
    return chart_path

def generate_rating_meter(score, output_path):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "black"},
            'steps': [
                {'range': [0, 20], 'color': "yellow"},
                {'range': [20, 40], 'color': "yellow"},
                {'range': [40, 60], 'color': "yellow"},
                {'range': [60, 80], 'color': "yellow"},
                {'range': [80, 100], 'color': "yellow"}
            ],
            'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': 100},
        }
    ))

    # Save the figure as an image
    meter_path = os.path.join(output_path, f'rating_meter_{score}.html')
    fig.write_html(meter_path)

    return meter_path

def generate_reports(input_csv, output_folder):
    df = pd.read_csv(input_csv)

    # Specify only the required columns
    required_columns = [
        'Name', 'College Name', 'Location',
        'Business/Course name', 'Certification Date', 'Personality Name',
        'Personality Code', 'Aptitude Score', 'Grade',
        'Communication', 'Rapport Building', 'Analytical Ability',
        'Curiosity', 'Knowledge', 'Enthusiasm', 'Discipline', 'Picture'
    ]

    # Filter the DataFrame to only include the required columns
    df = df[required_columns]

    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('report.html')

    for _, row in df.iterrows():
        picture_path = row['Picture']
        
        # Remove background from the candidate's picture using backgroundremover
        # output_image_path = os.path.join(output_folder, f"{row['Name']}_no-bg.png")
        # remove(picture_path, output_image_path)

        skill_chart = generate_skill_chart(row, output_folder)
        rating_meter = generate_rating_meter(row['Aptitude Score'], output_folder)

        report_html = template.render(
            name=row['Name'],
            college=row['College Name'],
            location=row['Location'],
            course=row['Business/Course name'],
            cert_date=row['Certification Date'],
            personality_name=row['Personality Name'],
            personality_code=row['Personality Code'],
            aptitude=row['Aptitude Score'],
            grade=row['Grade'],
            skill_chart=os.path.basename(skill_chart),  # Use only the filename
            performance_meter=os.path.basename(rating_meter),  # Use only the filename
            picture=row['Picture']
        )

        # # Save HTML report
        # output_html_path = os.path.join(output_folder, f"{row['Name']}_report.html")
        # with open(output_html_path, 'w') as f:
        #     f.write(report_html)

# def process_images_in_reports(output_folder):
#     reports_folder = 'reports'
#     processed_folder = 'processed_reports'
    
#     os.makedirs(processed_folder, exist_ok=True)

#     for filename in os.listdir(reports_folder):
#         if filename.endswith('.png'):
#             image_path = os.path.join(reports_folder, filename)
#             response = requests.post(
#                 'https://api.remove.bg/v1.0/removebg',
#                 files={'image_file': open(image_path, 'rb')},
#                 data={'size': 'auto'},
#                 headers={'X-Api-Key': os.environ.get('REMOVE_BG_API_KEY')},
#             )
#             if response.status_code == requests.codes.ok:
#                 with open(os.path.join(processed_folder, f"{filename}"), 'wb') as out:
#                     out.write(response.content)
#             else:
#                 print(f"Error processing {filename}: {response.status_code} {response.text}")
