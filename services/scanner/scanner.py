import yaml

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

                # Rule 3
                if "securityContext" not in container:
                    issues.append({
                        "type": "no_security_context",
                        "container": name
                    })

    return issues