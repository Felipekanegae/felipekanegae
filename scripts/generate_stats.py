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


def main():
    repositories = get_repositories()

    print(f"Public repositories: {len(repositories)}")

    total_commits = get_total_commits(repositories)

    print("\n==========================")
    print("GITHUB STATISTICS")
    print("==========================")

    print(f"Repositories: {len(repositories)}")
    print(f"Total commits: {total_commits}")


if __name__ == "__main__":
    main()
