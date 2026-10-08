from tools.kubernetes_tools import get_pods
from tools.kubernetes_tools import get_nodes
from tools.kubernetes_tools import get_pod_logs
from tools.kubernetes_tools import get_pod_events


# --------------------------------------------------
# Test 1 - Get Pods
# --------------------------------------------------

print("\n==============================")
print("TEST 1 - KUBERNETES PODS")
print("==============================")

pods = get_pods()

print(pods)


# --------------------------------------------------
# Test 2 - Get Nodes
# --------------------------------------------------

print("\n==============================")
print("TEST 2 - KUBERNETES NODES")
print("==============================")

nodes = get_nodes()

print(nodes)


# --------------------------------------------------
# Test 3 - Get Pod Logs
# --------------------------------------------------

print("\n==============================")
print("TEST 3 - POD LOGS")
print("==============================")

pod_name = "nginx-77b4fdf86c-rc9xj"

logs = get_pod_logs(pod_name)

print(logs)


# --------------------------------------------------
# Test 4 - Get Pod Events
# --------------------------------------------------

print("\n==============================")
print("TEST 4 - POD EVENTS")
print("==============================")

events = get_pod_events(pod_name)

print(events)
