import os

project = "autoapply_ai_bot"

folders = [
    project,
    f"{project}/logs",
    f"{project}/templates"
]

files = {
    f"{project}/main.py": '''import yaml
from job_search import search_jobs
from resume_customizer import customize_resume
from auto_apply import auto_apply_to_job
from datetime import datetime
import os

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

jobs = search_jobs(config['role'], config['location'])

# Load base resume
resume_path = "templates/base_resume.txt"
with open(resume_path, "r") as f:
    base_resume = f.read()

os.makedirs("logs", exist_ok=True)

for i, job in enumerate(jobs[:100]):
    print(f"\\nJob {i+1}: {job['title']} at {job['company']}")
    
    tailored_resume = customize_resume(job['description'], base_resume)

    # Save tailored resume
    filename = f"logs/{job['company']}_{datetime.now().date()}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(tailored_resume)

    auto_apply_to_job(job, resume_path)

print("\\nFinished applying to 100 jobs.")
''',

    f"{project}/job_search.py": '''def search_jobs(role, location):
    jobs = []
    for i in range(100):
        jobs.append({
            "title": f"{role} - Level {i+1}",
            "company": f"Company{i+1}",
            "description": f"Looking for a {role} in {location}.",
            "link": f"https://example.com/job{i+1}"
        })
    return jobs
''',

    f"{project}/resume_customizer.py": '''import openai

openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace this

def customize_resume(job_desc, base_resume):
    prompt = f\"\"\"
    Customize the following resume to better match this job description:

    Job Description:
    {job_desc}

    Resume:
    {base_resume}
    \"\"\"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
''',

    f"{project}/auto_apply.py": '''import time
import random
import os

def auto_apply_to_job(job, resume_path):
    print(f"Applying to {job['title']} at {job['company']}...")
    time.sleep(random.uniform(1, 2))  # Mimic delay

    with open("logs/applications.csv", "a", encoding="utf-8") as f:
        f.write(f"{job['title']},{job['company']},{job['link']}\\n")

    print(f"Applied to {job['company']}")
''',

    f"{project}/config.yaml": '''role: "Data Analyst"
location: "India"
salary_min: 600000
salary_max: 800000
job_type: "Full-time"
experience: "0-2 years"
''',

    f"{project}/templates/base_resume.txt": '''Vidya N
Email: your_email@example.com

Skilled Data Analyst experienced in Python, SQL, Power BI, and ML.
Projects:
- Highway Maintenance AI
- Pediatric Hospital Dashboard
''',

    f"{project}/requirements.txt": '''openai
pyyaml
'''
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create and fill files
for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"\nProject '{project}' created successfully!")

# Open in VS Code if installed
try:
    os.system(f"code {project}")
except:
    print("Open the folder manually in VS Code.")


