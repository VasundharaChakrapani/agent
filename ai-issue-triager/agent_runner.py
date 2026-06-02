import os
from dotenv import load_dotenv
from tools.file_discovery import find_candidate_files

from smolagents import (
    CodeAgent,
    tool,
    InferenceClientModel
)

from tools.file_tools import read_repository_file
from tools.analyzer import analyze_syntax_complexity


# Load environment variables
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")


@tool
def repository_reader(file_path: str) -> str:
    """
    Reads repository files safely.

    Args:
        file_path: Path of the repository file to read.
    """

    return read_repository_file(file_path)


@tool
def syntax_analyzer(source_code: str) -> dict:
    """
    Analyzes Python syntax safely using AST.

    Args:
        source_code: Python source code as a string.
    """

    return analyze_syntax_complexity(source_code)

@tool
def file_discovery(issue_text: str) -> str:
    """
    Finds repository files that may be relevant to the issue.

    Args:
        issue_text: Combined issue title and description.

    Returns:
        List of matching repository files.
    """
    return "\n".join(find_candidate_files(issue_text))

# Load Hugging Face model
model = InferenceClientModel(
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    token=HF_TOKEN
)


# Create autonomous agent
agent = CodeAgent(
    tools=[file_discovery, repository_reader, syntax_analyzer],
    model=model
)


# Run debugging task
issue_context = ""

if os.path.exists("current_issue.txt"):

    with open("current_issue.txt", "r", encoding="utf-8") as file:
        issue_context = file.read()


response = agent.run(
    f"""
    A GitHub issue was submitted.

    Issue Details:
    {issue_context}

    The repository may contain multiple files.

    Instructions:
    1. Use file_discovery to identify relevant files.
    2. Read the discovered files using repository_reader.
    3. Analyze the code carefully.
    4. Determine the root cause.
    5. Propose a fix.

    Generate a professional debugging report in markdown.

    Include the following sections:

    ## Bug Summary

    ## Root Cause

    ## Technical Explanation

    ## Suggested Fix

    ## Corrected Code

    Show the corrected version of the affected code.

    ## Patch Diff

    MANDATORY REQUIREMENT:

    The report is INVALID unless it contains a diff block.

    Use EXACTLY this format:

    ```diff
    --- original
    +++ fixed
    @@
    - old code
    + new code
    ```

    The diff must contain the actual buggy line and the corrected line.

    Do not merely describe the fix.

    Generate a real patch diff.

    Return the complete report in markdown.
    """
)

print(response)

with open("reports/debug_report.md", "w", encoding="utf-8") as file:
    file.write(str(response))

print("Debug report saved successfully.")