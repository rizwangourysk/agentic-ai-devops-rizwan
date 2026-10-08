from langchain_ollama import ChatOllama
from langchain_core.tools import tool
import subprocess
import json


# ==================================================
# Kubernetes Tool 1 - Get Pods
# ==================================================

@tool
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


# ==================================================
# Kubernetes Tool 2 - Get Pod Logs
# ==================================================

@tool
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


# ==================================================
# Kubernetes Tool 3 - Get Pod Events
# ==================================================

@tool
def get_pod_events(pod_name: str) -> str:
    """Get Kubernetes pod details and events."""

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


# ==================================================
# Kubernetes Healing Tool
# ==================================================

@tool
def fix_image_pull_error(pod_name: str, new_image: str) -> str:
    """
    Delete the broken pod and recreate it with a valid image.

    This tool is intentionally limited to the ai-devops namespace.
    """

    if pod_name != "broken-app":
        return "Healing denied: only the lab pod 'broken-app' can be modified."

    if new_image != "nginx:latest":
        return "Healing denied: only nginx:latest is allowed in this lab."

    delete_result = subprocess.run(
        [
            "kubectl",
            "delete",
            "pod",
            pod_name,
            "-n",
            "ai-devops"
        ],
        capture_output=True,
        text=True
    )

    if delete_result.returncode != 0:
        return f"Delete failed: {delete_result.stderr}"

    create_result = subprocess.run(
        [
            "kubectl",
            "run",
            pod_name,
            "--image=nginx:latest",
            "-n",
            "ai-devops"
        ],
        capture_output=True,
        text=True
    )

    if create_result.returncode != 0:
        return f"Recreate failed: {create_result.stderr}"

    return (
        f"Healing completed. "
        f"Pod '{pod_name}' was recreated using image '{new_image}'."
    )


# ==================================================
# Ollama LLM
# ==================================================

llm = ChatOllama(
    model="qwen2.5-coder:7b",
    temperature=0
)


# ==================================================
# STEP 1 - Detect
# ==================================================

print("\n==========================================")
print("STEP 1 - CHECKING KUBERNETES PODS")
print("==========================================")

pods_result = get_pods.invoke({})

print(pods_result)


# ==================================================
# STEP 2 - AI IDENTIFIES UNHEALTHY POD
# ==================================================

print("\n==========================================")
print("STEP 2 - AI IDENTIFYING UNHEALTHY POD")
print("==========================================")

response = llm.invoke(
    f"""
You are a Kubernetes DevOps AI agent.

Kubernetes pod status:

{pods_result}

Find an unhealthy pod.

Unhealthy statuses include:

- Error
- CrashLoopBackOff
- ImagePullBackOff
- ErrImagePull
- Pending
- Failed

If an unhealthy pod exists, return ONLY JSON:

{{
    "pod_name": "ACTUAL_POD_NAME"
}}

Use the exact pod name.

If all pods are healthy:

{{"pod_name": null}}
"""
)

print(response.content)


# ==================================================
# STEP 3 - PARSE AI DECISION
# ==================================================

try:

    content = response.content.strip()

    if content.startswith("```"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

    decision = json.loads(content)

    pod_name = decision.get("pod_name")

    if pod_name is None:

        print("\n==========================================")
        print("RESULT")
        print("==========================================")

        print("All Kubernetes pods are healthy.")

        exit()


    # ==================================================
    # STEP 4 - INVESTIGATE
    # ==================================================

    print("\n==========================================")
    print("STEP 3 - INVESTIGATING POD")
    print("==========================================")

    print(f"Pod: {pod_name}")


    logs_result = get_pod_logs.invoke(
        {
            "pod_name": pod_name
        }
    )

    events_result = get_pod_events.invoke(
        {
            "pod_name": pod_name
        }
    )


    print("\n--- POD LOGS ---")
    print(logs_result)

    print("\n--- POD EVENTS ---")
    print(events_result)


    # ==================================================
    # STEP 5 - AI DIAGNOSIS
    # ==================================================

    print("\n==========================================")
    print("STEP 4 - AI DIAGNOSIS")
    print("==========================================")

    diagnosis = llm.invoke(
        f"""
You are an expert Kubernetes DevOps troubleshooting AI.

Pod name:

{pod_name}

Pod status:

{pods_result}

Pod logs:

{logs_result}

Pod events:

{events_result}

Analyze the evidence.

Return:

1. Problem
2. Evidence
3. Root Cause
4. Recommended Fix
5. Healing Action

Important:

The current lab allows this specific healing action:

Change the broken image:

nginx:this-image-does-not-exist

to:

nginx:latest

Do not invent another healing action.
"""
    )

    print(diagnosis.content)


    # ==================================================
    # STEP 6 - HUMAN APPROVAL
    # ==================================================

    print("\n==========================================")
    print("STEP 5 - HUMAN APPROVAL")
    print("==========================================")

    print("The AI recommends:")
    print("Change image to nginx:latest")

    approval = input(
        "\nDo you approve the healing action? (yes/no): "
    ).strip().lower()


    if approval != "yes":

        print("\n==========================================")
        print("HEALING CANCELLED")
        print("==========================================")

        print("Human approval was not given.")

        exit()


    # ==================================================
    # STEP 7 - HEAL
    # ==================================================

    print("\n==========================================")
    print("STEP 6 - SELF HEALING")
    print("==========================================")

    healing_result = fix_image_pull_error.invoke(
        {
            "pod_name": pod_name,
            "new_image": "nginx:latest"
        }
    )

    print(healing_result)


    # ==================================================
    # STEP 8 - WAIT
    # ==================================================

    print("\nWaiting for Kubernetes to start the repaired pod...")

    import time

    time.sleep(5)


    # ==================================================
    # STEP 9 - VERIFY
    # ==================================================

    print("\n==========================================")
    print("STEP 7 - VERIFYING HEALING")
    print("==========================================")

    verification = get_pods.invoke({})

    print(verification)


    # ==================================================
    # STEP 10 - FINAL AI VERIFICATION
    # ==================================================

    print("\n==========================================")
    print("STEP 8 - AI FINAL VERIFICATION")
    print("==========================================")

    final_check = llm.invoke(
        f"""
You are a Kubernetes verification AI.

Original pod:

{pod_name}

Kubernetes pod status after healing:

{verification}

Determine whether the pod is healthy.

If the pod is Running and READY is 1/1,
say:

HEALING SUCCESSFUL

Otherwise say:

HEALING FAILED

Explain briefly in simple English.
"""
    )

    print(final_check.content)


except json.JSONDecodeError as e:

    print("\nJSON parsing error:")
    print(e)

    print("\nRaw AI response:")
    print(response.content)


except Exception as e:

    print("\nAn error occurred:")
    print(e)
