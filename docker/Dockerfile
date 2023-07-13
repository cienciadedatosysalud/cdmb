FROM python:3.9.17-slim
RUN apt update && apt install -y --no-install-recommends \
  && apt install -y graphviz \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
RUN echo "import cdmb\n\
import os\n\
if __name__ == '__main__':\n\
    cdmb.launch_ui('0.0.0.0',8501)" | cat > ui.py

CMD ["python3", "ui.py"]
