import os

def find_candidate_files(issue_text: str) -> list:
    """
    Search repository for files whose names
    match keywords from the issue.
    """

    matches = []

    for root, dirs, files in os.walk("."):

        dirs[:] = [
            d for d in dirs
            if d not in {
                "venv",
                ".git",
                "__pycache__",
                "reports"
            }
        ]

        for file in files:
            filename = file.lower()

            for word in issue_text.lower().split():
                if word in filename:
                    matches.append(
                        os.path.join(root, file)
                    )

    return list(set(matches))