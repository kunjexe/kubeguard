from fastapi import FastAPI, UploadFile, File
from scanner import scan_yaml_content
from github_scanner import scan_repo

print(" New Fastapi app running...")

app = FastAPI()

@app.get("/")
def home():
    return {"message": "KubeGuard Scanner Running 🚀"}

@app.post("/scan/github")
async def scan_github(payload: dict):
    try:
        repo_url = payload.get("repo_url")

        if not repo_url:
            return {"error": "repo_url is required"}

        result = scan_repo(repo_url)

        return {
            "repo": repo_url,
            "results": result
        }

    except Exception as e:
        return {"error": str(e)}

#Basic Scanner Logic (inline for now)
def scan_yaml_content(yaml_content):
    docs = list(yaml.safe_load_all(yaml_content))
    issues = []

    for doc in docs:
        if not doc:
            continue

        kind = doc.get("kind", "")
        spec = doc.get("spec", {})

        if kind == "Deployment":
            containers = spec.get("template", {}).get("spec", {}).get("containers", [])

            for container in containers:
                name = container.get("name", "unknown")

                # Rule 1
                if "resources" not in container:
                    issues.append({
                        "type": "missing_resources",
                        "container": name
                    })

                # Rule 2
                image = container.get("image", "")
                if ":latest" in image:
                    issues.append({
                        "type": "latest_tag_used",
                        "container": name
                    })

    return issues


# 🔥 FIRST ENDPOINT (file upload)
@app.post("/scan/file")
async def scan_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        yaml_content = content.decode("utf-8")

        result = scan_yaml_content(yaml_content)
        return {"issues": result}

    except Exception as e:
        return {"error": str(e)}