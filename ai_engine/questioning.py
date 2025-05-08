import random

# Templates categorized by case type and difficulty
question_templates_by_type = {
    "Civil Law": {
        "Easy": [
            "What is a contract?",
            "Who can sue for breach of contract?"
        ],
        "Medium": [
            "What constitutes a valid tort claim?",
            "Explain liquidated damages."
        ],
        "Hard": [
            "Analyze the enforceability of restrictive covenants in contracts.",
            "Discuss promissory estoppel in breach cases."
        ]
    },
    "Criminal Law": {
        "Easy": [
            "What is a crime?",
            "What is an arrest warrant?"
        ],
        "Medium": [
            "Explain the difference between murder and manslaughter.",
            "What is circumstantial evidence?"
        ],
        "Hard": [
            "Critically analyze the role of mens rea in criminal convictions.",
            "Discuss procedural safeguards under Article 21 of the Constitution."
        ]
    },
    # ✨ Add similar structure for other case types as needed
}

def generate_smart_questions(case_text, case_type, difficulty, num_questions=3):
    """
    Generate questions based on selected case type and difficulty
    """
    templates_by_difficulty = question_templates_by_type.get(case_type, {})
    templates = templates_by_difficulty.get(difficulty, [])

    if templates:
        return random.sample(templates, k=min(len(templates), num_questions))
    else:
        return ["What are the main legal issues in this case?"]
