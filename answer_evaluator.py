import re

def evaluate_answer(question, answer):
    """
    Evaluate a user's answer based on:
    - Professionalism: length and punctuation
    - Correctness: keyword overlap with the question
    Returns a score, feedback, and correctness flag.
    """

    if not answer.strip():
        return {
            "score": 0,
            "feedback": "No answer provided.",
            "correct": False
        }

    # Professionalism score
    length_score = min(len(answer.split()) / 5, 10)  # up to 10 points
    punctuation_score = 5 if re.search(r"[.!?]", answer) else 0
    professionalism = length_score + punctuation_score

    # Correctness score (basic keyword overlap)
    q_words = [w.lower() for w in re.findall(r"\w+", question) if len(w) > 3]
    a_words = set(re.findall(r"\w+", answer.lower()))
    overlap = sum(1 for w in q_words if w in a_words)
    correctness = min(overlap, 10)

    # Final score
    total_score = int((professionalism + correctness) * 5)  # scale to 100

    feedback = (
        "Strong, relevant answer." if total_score > 60
        else "Try to expand with more detail and clarity."
    )

    return {
        "score": total_score,
        "feedback": feedback,
        "correct": correctness >= 1  # ✅ mark correct if at least 1 keyword overlaps
    }
