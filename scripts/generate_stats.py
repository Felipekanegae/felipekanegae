import json
import os
import urllib.request
import urllib.parse

USERNAME = "Felipekanegae"
TOKEN = os.environ.get("GITHUB_TOKEN")

API_URL = "https://api.github.com"


def github_request(url):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-profile-stats"
    }

    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"

    request = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(request) as response:
        return json.load(response)


def get_paginated_data(url):
    results = []
    page = 1

    while True:
        separator = "&" if "?" in url else "?"

        paginated_url = (
            f"{url}{separator}per_page=100&page={page}"
        )

        data = github_request(paginated_url)

        if not data:
            break

        results.extend(data)

        if len(data) < 100:
            break

        page += 1

    return results


def get_repositories():
    url = f"{API_URL}/users/{USERNAME}/repos?type=owner"

    repositories = get_paginated_data(url)

    return [
        repo for repo in repositories
        if not repo["fork"]
    ]


def get_branches(repository):
    url = (
        f"{API_URL}/repos/{USERNAME}/"
        f"{repository}/branches"
    )

    return get_paginated_data(url)


def get_commits(repository, branch):
    branch_name = urllib.parse.quote(branch, safe="")

    url = (
        f"{API_URL}/repos/{USERNAME}/{repository}/commits"
        f"?sha={branch_name}&author={USERNAME}"
    )

    return get_paginated_data(url)


def get_total_commits(repositories):
    total_commits = 0

    for repository in repositories:
        repository_name = repository["name"]

        print(f"\nRepository: {repository_name}")

        branches = get_branches(repository_name)

        unique_commits = set()

        for branch in branches:
            branch_name = branch["name"]

            commits = get_commits(
                repository_name,
                branch_name
            )

            for commit in commits:
                unique_commits.add(commit["sha"])

        repository_total = len(unique_commits)

        total_commits += repository_total

        print(f"Commits: {repository_total}")

    return total_commits


def generate_svg(repositories_count, commits_count):
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="500" height="235" viewBox="0 0 500 235">
    <rect x="1" y="1" width="498" height="233" rx="12"
          fill="#1a1b27" stroke="#e4e2e2" stroke-width="2"/>

    <text x="30" y="45"
          font-family="Arial, sans-serif"
          font-size="24" font-weight="bold"
          fill="#70a5fd">
        Felipe's GitHub Stats
    </text>

    <text x="30" y="105"
          font-family="Arial, sans-serif"
          font-size="18" fill="#38bdae">
        Total Commits
    </text>

    <text x="460" y="105"
          font-family="Arial, sans-serif"
          font-size="24" font-weight="bold"
          text-anchor="end" fill="#bf91f3">
        {commits_count}
    </text>

    <text x="30" y="160"
          font-family="Arial, sans-serif"
          font-size="18" fill="#38bdae">
        Public Repositories
    </text>

    <text x="460" y="160"
          font-family="Arial, sans-serif"
          font-size="24" font-weight="bold"
          text-anchor="end" fill="#bf91f3">
        {repositories_count}
    </text>
</svg>
"""

    with open("assets/github-stats.svg", "w", encoding="utf-8") as file:
        file.write(svg)

    print("SVG generated successfully!")
    

def main():
    repositories = get_repositories()

    print(f"Public repositories: {len(repositories)}")

    total_commits = get_total_commits(repositories)

    print("\n==========================")
    print("GITHUB STATISTICS")
    print("==========================")

    print(f"Repositories: {len(repositories)}")
    print(f"Total commits: {total_commits}")
    generate_svg(len(repositories), total_commits)


if __name__ == "__main__":
    main()
