import os
from huggingface_hub import login, HfApi

def update_dockerfile(docker_user, repo_name, date):
    """
    Update the Dockerfile.streamlit of the HF Space with the latest image based on the provided date.
    Args:
        docker_user (str): Docker username.
        repo_name (str): Repository name.
        date (str): Date or version tag for the Docker image.
    """
    dockerfile_content = f"""
        FROM docker.io/{docker_user}/{repo_name}:{date}
        USER user
        ENV PATH=$PATH:/home/user/.local/bin
        WORKDIR /app
        COPY --chown=user . /app/
        EXPOSE 7860
        ENV GRADIO_SERVER_NAME="0.0.0.0"
        CMD ["uv", "run", "app.py"]
    """
    dockerfile_path = "../Dockerfile"
    os.makedirs(os.path.dirname(dockerfile_path), exist_ok=True)
    with open(dockerfile_path, "w") as f:
        f.write(dockerfile_content)
    print(f"Dockerfile.streamlit updated at {dockerfile_path}")

def commit_and_push_on_space(hf_user, hf_space_name, hf_token):
    """ Commit and push the Dockerfile.streamlit updated to the Hugging Face space.
    Args:
        hf_user (str): Hugging Face username.
        hf_space_name (str): Hugging Face space name.
        hf_token (str): Hugging Face API token.
    """
    try:
        login(token=hf_token)
        api = HfApi()
        api.upload_file(
            path_or_fileobj="../Dockerfile",
            path_in_repo="Dockerfile.streamlit",
            repo_id=f"{hf_user}/{hf_space_name}",
            repo_type="space",
            token=hf_token
        )
        print("Dockerfile.streamlit updated successfully.")
    except Exception as e:
        print(f"Error during Dockerfile.streamlit update: {e}")

if __name__ == "__main__":
    DOCKER_USER = os.getenv("DOCKER_USER", "default_user")
    REPO_NAME = os.getenv("REPO_NAME", "default_repo")
    DATE = os.getenv("DATE", "latest")
    HF_USER = os.getenv("HF_USER", "default_hf_user")
    HF_SPACE_NAME = os.getenv("HF_SPACE_NAME", "default_hf_space")
    HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")

    if not HF_API_TOKEN:
        print("HF token not defined!")
    else:
        update_dockerfile(DOCKER_USER, REPO_NAME, DATE)
        commit_and_push_on_space(HF_USER, HF_SPACE_NAME, HF_API_TOKEN)
