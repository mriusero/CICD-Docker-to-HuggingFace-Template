import os
import argparse
from huggingface_hub import login, upload_file

def update_dockerfile(docker_user, repo_name, date, app):
    """
    Update the Dockerfile of the HF Space with latest image based on the provided date.
    Args:
        docker_user (str): Docker username.
        repo_name (str): Repository name.
        date (str): Date or version tag for the Docker image.
        app (str): The application type, either 'streamlit' or 'gradio'.
    """
    if app == 'streamlit':
        port = 8501
        env = ""
        cmd = "CMD [\"uv\", \"run\", \"streamlit\", \"run\", \"app.py\", \"--server.port=8501\", \"--server.address=0.0.0.0\"]"

    elif app == 'gradio':
        port = 7860
        env = "ENV GRADIO_SERVER_NAME='0.0.0.0'"
        cmd = "CMD [\"uv\", \"run\", \"app.py\"]"

    else:
        raise ValueError("Unsupported app type. Use 'streamlit' or 'gradio'.")

    dockerfile_content = f"""
        FROM docker.io/{docker_user}/{repo_name}:{date}
        USER user
        ENV PATH=$PATH:/home/user/.local/bin
        WORKDIR /app
        COPY --chown=user . /app/
        EXPOSE {port}
        {env}
        {cmd}
    """
    with open("./Dockerfile", "w") as f:
        f.write(dockerfile_content)

def commit_and_push_on_space(hf_user, hf_space_name, hf_token):
    """ Commit and push the Dockerfile updated to the Hugging Face space.
    Args:
        hf_user (str): Hugging Face username.
        hf_space_name (str): Hugging Face space name.
        hf_token (str): Hugging Face API token.
    """
    try:
        login(token=hf_token)
        upload_file(
            path_or_fileobj="./Dockerfile",
            path_in_repo="Dockerfile",
            repo_id=f"{hf_user}/{hf_space_name}",
            repo_type="space",
        )
        print("Docker file updated successfully.")
    except Exception as e:
        print(f"Error during Dockerfile update: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update and push Dockerfile to Hugging Face Space.")
    parser.add_argument('--app', type=str, required=True, choices=['streamlit', 'gradio'], help="The application type, either 'streamlit' or 'gradio'.")

    args = parser.parse_args()

    required_env_vars = ["DOCKER_USER", "REPO_NAME", "HF_USER", "HF_SPACE_NAME", "HF_TOKEN"]
    env_vars = {var: os.getenv(var, "") for var in required_env_vars}

    for var, value in env_vars.items():
        if not value:
            print(f"Error: {var} is not defined.")
            exit(1)

    update_dockerfile(env_vars["DOCKER_USER"], env_vars["REPO_NAME"], os.getenv("DATE", "latest"), args.app)
    commit_and_push_on_space(env_vars["HF_USER"], env_vars["HF_SPACE_NAME"], env_vars["HF_TOKEN"])
