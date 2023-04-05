from marvin import ai_fn


@ai_fn
def create_question(subject: str, level: str, topic: str) -> str:
    """given the subject, level and topic, create an exam question. The exam question must be an question that can receive a text-based
    answer. I'm going to ask a student this question and ask you to mark their answer later, so make sure it's a question that you would
    be confident ansering yourself correctly"""
