import subprocess


# --------------------------------------------------
# Kubernetes Tool 1 - Get Pods
# --------------------------------------------------

def get_pods() -> str:
    """Get Kubernetes pods from the ai-devops namespace."""

    result = subprocess.run(
        [
            "kubectl",
            "get",
            "pods",
            "-n",
            "ai-devops"
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return f"Error: {result.stderr}"

    return result.stdout


# --------------------------------------------------
# Kubernetes Tool 2 - Get Nodes
# --------------------------------------------------

def get_nodes() -> str:
    """Get Kubernetes cluster nodes."""

    result = subprocess.run(
        [
            "kubectl",
            "get",
            "nodes"
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return f"Error: {result.stderr}"

    return result.stdout


# --------------------------------------------------
# Kubernetes Tool 3 - Get Pod Logs
# --------------------------------------------------

def get_pod_logs(pod_name: str) -> str:
    """Get logs from a Kubernetes pod."""

    result = subprocess.run(
        [
            "kubectl",
            "logs",
            pod_name,
            "-n",
            "ai-devops"
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return f"Error: {result.stderr}"

    return result.stdout
# --------------------------------------------------
# Kubernetes Tool 4 - Get Pod Events
# --------------------------------------------------

def get_pod_events(pod_name: str) -> str:
    """Get Kubernetes events for a pod."""

    result = subprocess.run(
        [
            "kubectl",
            "describe",
            "pod",
            pod_name,
            "-n",
            "ai-devops"
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return f"Error: {result.stderr}"

    return result.stdout
