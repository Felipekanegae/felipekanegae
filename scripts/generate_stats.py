import json
import urllib.request

USERNAME = "Felipekanegae"

def get_repositories():
    repositories = []
    page = 1

    while True:
        url = (
            f"https://api.github.com/users/{USERNAME}/repos"
            f"?per_page=100&page={page}&type=owner"
        )

        request = urllib.request.Request(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "github-profile-stats"
            }
        )

        with urllib.request.urlopen(request) as response:
            data = json.load(response)

        if not data:
            break

        repositories.extend(data)
        page += 1

    return repositories


def main():
    repositories = get_repositories()

    print(f"Public repositories: {len(repositories)}")

    for repository in repositories:
        print(f"- {repository['name']}")


if __name__ == "__main__":
    main()
