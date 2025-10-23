
def generate_questions(job_role, skills=None, difficulty="medium", categories=None, num_questions=5):
    """
    Generate interview questions based on job role, skills, difficulty, categories, and desired count.
    """

    questions = []
    categories = categories or ["technical", "behavioral"]

    # Sample question templates
    templates = {
        "technical": [
            "Explain how you would apply {skill} in a real-world {job_role} project.",
            "What are the challenges of using {skill} in {job_role} tasks?",
            "Describe a situation where {skill} helped solve a technical problem."
        ],
        "behavioral": [
            "Tell me about a time you faced a challenge in a {job_role} role.",
            "How do you handle feedback or criticism in a team setting?",
            "Describe a situation where you had to adapt quickly."
        ],
        "situational": [
            "What would you do if a project deadline was suddenly moved up?",
            "How would you respond if a teammate disagreed with your approach?",
            "Imagine you're leading a team and a conflict arises — how do you handle it?"
        ],
        "hr": [
            "Why do you want to work in this {job_role} position?",
            "What are your salary expectations?",
            "Where do you see yourself in 5 years?"
        ]
    }

    # Generate questions using templates
    while len(questions) < num_questions:
        for category in categories:
            if len(questions) >= num_questions:
                break
            if category in templates:
                template = templates[category][len(questions) % len(templates[category])]
                if skills:
                    skill = skills[len(questions) % len(skills)]
                    question = template.format(skill=skill, job_role=job_role)
                else:
                    question = template.format(skill="your skills", job_role=job_role)
                questions.append(f"({category.title()}) {question}")

    return questions[:num_questions]

