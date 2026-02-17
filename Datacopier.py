import os
import requests

# ============================================
# CONFIG
# ============================================
OWNER = "username"
REPO = "source-repo"
BRANCH = "main"
FOLDER_PATH = "data_folder"  # folder inside source repo
DESTINATION = "downloaded_data"

# ============================================
# FUNCTION TO DOWNLOAD FOLDER
# ============================================

def download_folder(owner, repo, path, branch, local_dir):
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"
    response = requests.get(api_url)
    response.raise_for_status()

    os.makedirs(local_dir, exist_ok=True)

    for item in response.json():
        if item["type"] == "file":
            download_url = item["download_url"]
            file_content = requests.get(download_url).content

            with open(os.path.join(local_dir, item["name"]), "wb") as f:
                f.write(file_content)

        elif item["type"] == "dir":
            download_folder(
                owner,
                repo,
                item["path"],
                branch,
                os.path.join(local_dir, item["name"])
            )

# ============================================
# RUN
# ============================================

if __name__ == "__main__":
    download_folder(OWNER, REPO, FOLDER_PATH, BRANCH, DESTINATION)
    print("✅ Folder downloaded successfully!")
