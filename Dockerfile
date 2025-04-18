FROM python:3.12-slim

RUN useradd -m -u 1000 user

USER user

ENV PATH=$PATH:/home/user/.local/bin

WORKDIR /app

COPY --chown=user pyproject.toml uv.lock* /app/

RUN pip install --upgrade pip \
    && pip install uv \
    && uv sync

COPY --chown=user . /app/

# Gradio
EXPOSE 7860
ENV GRADIO_SERVER_NAME='0.0.0.0'
CMD ["uv", "run", "app.py"]

# Streamlit
#EXPOSE 8501
#CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]