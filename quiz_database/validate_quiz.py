import json
import os

QUIZ_FOLDER = "questions"

def validate_question(q, file, index):
    errors = []

    if "question" not in q:
        errors.append("missing question field")

    if "answers" not in q:
        errors.append("missing answers")

    if "correctIndex" not in q:
        errors.append("missing correctIndex")

    if "funFact" not in q:
        errors.append("missing funFact")

    if "difficulty" not in q:
        errors.append("missing difficulty")

    # Validate question languages
    if isinstance(q.get("question"), dict):
        for lang in ["en", "ms"]:
            if lang not in q["question"]:
                errors.append(f"missing question.{lang}")
            elif not isinstance(q["question"][lang], str):
                errors.append(f"question.{lang} not string")

    # Validate answers
    answers = q.get("answers", [])
    if not isinstance(answers, list):
        errors.append("answers not a list")
    else:
        for i, ans in enumerate(answers):
            if not isinstance(ans, dict):
                errors.append(f"answer {i} not object")
                continue
            for lang in ["en", "ms"]:
                if lang not in ans:
                    errors.append(f"answer {i} missing {lang}")
                elif not isinstance(ans[lang], str):
                    errors.append(f"answer {i}.{lang} not string")

    # Validate correctIndex
    ci = q.get("correctIndex")
    if not isinstance(ci, int):
        errors.append("correctIndex not int")
    elif isinstance(answers, list) and ci >= len(answers):
        errors.append("correctIndex out of range")

    # Validate difficulty
    if q.get("difficulty") not in ["easy", "medium", "hard"]:
        errors.append("invalid difficulty")

    if errors:
        print(f"\n❌ Error in {file} question #{index}")
        for e in errors:
            print("   -", e)


def validate_file(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        print(f"{path} is not a list of questions")
        return

    for i, q in enumerate(data):
        validate_question(q, path, i)


def main():
    for root, _, files in os.walk(QUIZ_FOLDER):
        for file in files:
            if file.endswith(".json"):
                validate_file(os.path.join(root, file))


if __name__ == "__main__":
    main()
