import subprocess
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain.agents import create_agent


llm = ChatOllama(
    model="qwen3-coder:30b",
    temperature=0,
    num_ctx=8192,
)


@tool
def get_pods():
    """Lists all pods in all namespaces using kubectl get pods -A."""
    result = subprocess.run(["kubectl", "get", "pods", "-A"], capture_output=True, text=True, timeout=20)
    return result.stdout or result.stderr


@tool
def get_docker_containers():
    """Lists running Docker containers using docker ps."""
    result = subprocess.run(["docker", "ps"], capture_output=True, text=True, timeout=20)
    return result.stdout or result.stderr


@tool
def get_docker_images():
    """Lists Docker images using docker image ls."""
    result = subprocess.run(["docker", "image", "ls"], capture_output=True, text=True, timeout=20)
    return result.stdout or result.stderr


@tool
def get_docker_logs(container_name: str):
    """Shows logs for a Docker container. Input: container name."""
    result = subprocess.run(["docker", "logs", container_name], capture_output=True, text=True, timeout=20)
    return result.stdout or result.stderr


@tool
def get_docker_stats():
    """Shows live Docker container resource usage using docker stats."""
    result = subprocess.run(["docker", "stats", "--no-stream"], capture_output=True, text=True, timeout=20)
    return result.stdout or result.stderr


@tool
def get_docker_ps_all():
    """Lists all Docker containers, including stopped ones using docker ps -a."""
    result = subprocess.run(["docker", "ps", "-a"], capture_output=True, text=True, timeout=20)
    return result.stdout or result.stderr


@tool
def get_compose_status():
    """Shows Docker Compose service status using docker compose ps."""
    result = subprocess.run(["docker", "compose", "ps"], capture_output=True, text=True, timeout=20)
    return result.stdout or result.stderr


@tool
def get_nodes():
    """Lists Kubernetes nodes using kubectl get nodes."""
    result = subprocess.run(["kubectl", "get", "nodes"], capture_output=True, text=True, timeout=20)
    return result.stdout or result.stderr


@tool
def get_services():
    """Lists Kubernetes services using kubectl get svc -A."""
    result = subprocess.run(["kubectl", "get", "svc", "-A"], capture_output=True, text=True, timeout=20)
    return result.stdout or result.stderr


@tool
def get_deployments():
    """Lists Kubernetes deployments using kubectl get deployments -A."""
    result = subprocess.run(["kubectl", "get", "deployments", "-A"], capture_output=True, text=True, timeout=20)
    return result.stdout or result.stderr


@tool
def get_pod_logs(namespace: str, pod_name: str):
    """Shows logs for a Kubernetes pod. Inputs: namespace and pod name."""
    result = subprocess.run(["kubectl", "logs", "-n", namespace, pod_name], capture_output=True, text=True, timeout=20)
    return result.stdout or result.stderr


@tool
def get_events():
    """Lists recent Kubernetes events using kubectl get events -A."""
    result = subprocess.run(["kubectl", "get", "events", "-A"], capture_output=True, text=True, timeout=20)
    return result.stdout or result.stderr


@tool
def get_system_health():
    """Checks basic Docker and Kubernetes environment health."""
    docker_info = subprocess.run(["docker", "info"], capture_output=True, text=True, timeout=20)
    kubectl_info = subprocess.run(["kubectl", "cluster-info"], capture_output=True, text=True, timeout=20)
    return f"Docker info:\n{docker_info.stdout or docker_info.stderr}\n\nKubernetes info:\n{kubectl_info.stdout or kubectl_info.stderr}"


@tool
def check_http_endpoint(url: str):
    """Performs a simple HTTP check for a given URL."""
    result = subprocess.run(["curl", "-I", url], capture_output=True, text=True, timeout=20)
    return result.stdout or result.stderr


@tool
def get_git_status():
    """Shows the current git repository status."""
    result = subprocess.run(["git", "status", "--short"], capture_output=True, text=True, timeout=20)
    return result.stdout or result.stderr


agent = create_agent(
    model=llm,
    tools=[
        get_pods,
        get_docker_containers,
        get_docker_images,
        get_docker_logs,
        get_docker_stats,
        get_docker_ps_all,
        get_compose_status,
        get_nodes,
        get_services,
        get_deployments,
        get_pod_logs,
        get_events,
        get_system_health,
        check_http_endpoint,
        get_git_status,
    ],
    system_prompt=(
        "You are a professional DevOps assistant that inspects live Kubernetes, Docker, and "
        "local system environments using tools.\n"
        "Tools:\n"
        "- get_pods: lists all pods in all namespaces.\n"
        "- get_docker_containers: lists running Docker containers.\n"
        "- get_docker_images: lists Docker images.\n"
        "- get_docker_logs: shows logs for a container.\n"
        "- get_docker_stats: shows container resource usage.\n"
        "- get_docker_ps_all: lists all containers, including stopped ones.\n"
        "- get_compose_status: shows Docker Compose service status.\n"
        "- get_nodes: lists Kubernetes nodes.\n"
        "- get_services: lists Kubernetes services.\n"
        "- get_deployments: lists Kubernetes deployments.\n"
        "- get_pod_logs: shows logs for a pod.\n"
        "- get_events: lists recent Kubernetes events.\n"
        "- get_system_health: checks Docker and Kubernetes health.\n"
        "- check_http_endpoint: checks a URL over HTTP.\n"
        "- get_git_status: shows git status.\n"
        "Rules:\n"
        "- When a question needs live state, ALWAYS call the relevant tool.\n"
        "- Never invent pod, container, image, or service names.\n"
        "- Answer only from tool output. If a tool fails, explain the likely cause.\n"
        "- Keep responses concise and professional."
    ),
)


question = input("Ask your Agent a Question: >")
response = agent.invoke({"messages": [("user", question)]})
print(response["messages"][-1].content)