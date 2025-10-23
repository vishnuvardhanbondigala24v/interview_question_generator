
import re

# Simple curated skills list (expand as needed)
SKILL_KEYWORDS = [
    "python", "java", "c++", "sql", "machine learning", "deep learning",
    "nlp", "pandas", "numpy", "statistics", "docker", "aws", "azure",
    "react", "node", "django", "flask", "git", "linux", "excel"
]

def extract_skills(text):
    text = text.lower()
    found = set()
    for skill in SKILL_KEYWORDS:
        if re.search(rf"\\b{re.escape(skill)}\\b", text):
            found.add(skill.title())
    return sorted(found)
