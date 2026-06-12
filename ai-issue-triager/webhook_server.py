from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import subprocess


app = FastAPI()


# Incoming issue schema
class GitHubIssue(BaseModel):
    title: str
    description: str


def run_agent(issue_title, issue_description):

    # Save issue context
    with open("current_issue.txt", "w", encoding="utf-8") as file:

        file.write(
            f"Issue Title: {issue_title}\n\n"
            f"Issue Description:\n{issue_description}"
        )

    # Run autonomous agent
    subprocess.run(
        ["venv\\Scripts\\python.exe", "agent_runner.py"]
    )


@app.post("/webhook")
async def github_webhook(
    payload: dict,
    background_tasks: BackgroundTasks
):

    if payload.get("action") != "opened":
        return {"message": "Ignoring event"}

    issue = payload.get("issue", {})

    title = issue.get("title", "")
    description = issue.get("body", "")

    background_tasks.add_task(
        run_agent,
        title,
        description
    )

    return {
        "status": "accepted",
        "message": "GitHub issue received"
    }