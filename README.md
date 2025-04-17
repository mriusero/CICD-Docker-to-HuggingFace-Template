# CICD-Docker-to-HuggingFace-Template

This template is based on a Streamlit app that is containerized using Docker. It provides a complete CI/CD pipeline for deploying your Streamlit app to Hugging Face Spaces. The template is designed to be easily customizable and can be adapted to fit your specific needs.
It includes steps for continuous integration (CI) and continuous deployment (CD), ensuring that your code is tested and deployed efficiently.


---
*Contributions are welcome! Feel free to open issues or submit pull requests for any improvements or features you would like to see.*

---

## Prerequisites
To use this template, you need the following prerequisites:
- A GitHub repository where you want to set up the CI/CD pipeline.
- A Docker Hub account to store your Docker images.
- A Hugging Face account to host your space.
- A Hugging Face space created and ready to be updated with the Docker image.

## Environment Variables
The workflow use following secrets for Docker and Hugging Face authentication.

- `DOCKER_USER`: your Docker Hub username.
- `DOCKER_PASSWORD`: your Docker Hub password.
- `REPO_NAME` : the name of the Docker repository where the Docker image will be pushed.
- `HF_USER`: your Hugging Face username.
- `HF_API_TOKEN`: your Hugging Face API token.
- `HF_SPACE_NAME`: the name of the Hugging Face space where the Docker image will be pushed.

> [!TIP]
> To add secrets to your GitHub repository, follow these steps:
> 1. Go to your repository settings.
> 2. Click on "Secrets and variables" in the left sidebar.
> 3. Click on "Actions" under "Secrets and variables".
> 4. Click on "New repository secret".
> 5. Add a new secret with its name `SECRET_NAME` and the associated value `hf_xxx`.


## Triggers
The workflow is triggered by specific events in the GitHub repository. 
Currently, the workflow is set to trigger on the following events:
- **Push**: On `main` branch.
- **Pull Request**: On `main` branch.

> [!TIP]
> The triggers are defined in the `on` section of the workflow file.
> You can adjust trigger conditions such as `push` or `pull_request` on a specific branch to suit your needs. 

## Workflow
### Continuous Integration

The `ci_pipeline` job is responsible for running tests and checks on the codebase, it follows the steps below:

  1. **Checkout repository**: uses `actions/checkout@v3`.
  2. **Set up Python**: uses `actions/setup-python@v4` with Python 3.11.
  3. **Install dependencies**: upgrades `pip`, installs `uv`, and syncs.
  4. **Format code with Black**: formats code in `src/`.
  5. **Lint code with Pylint**: lints code in `src/` with specific disables.
  6. **Streamlit app health check**: runs the Streamlit app and checks its health.
  7. **Cleanup Streamlit process**: kills the Streamlit process.

> [!TIP]
> Here is an example of how to set up the `ci_pipeline` but you can easily change the steps to suit your needs.
> Dependencies are managed with `uv` for quick installation and syncing but you can easily change it to `pip` or `poetry` if you prefer.
> Format code with `black` and lint with `pylint` to ensure code quality but you can easily change it to `ruff` or other if you prefer.

### Continuous Deployment
The `cd_pipeline` job is responsible for building and deploying the Docker image to Hugging Face Spaces, it follows the steps below:

  1. **Checkout repository**: uses `actions/checkout@v3`.
  2. **Docker login**: logs in to Docker using secrets.
  3. **Get current date**: sets the current date as an environment variable.
  4. **Build the Docker image**: builds the Docker image with the current date as a tag.
  5. **Docker Push**: pushes the Docker image to the Docker repository.
  6. **Update the HF Space**: installs `huggingface_hub` and runs a script to update the Hugging Face space.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.