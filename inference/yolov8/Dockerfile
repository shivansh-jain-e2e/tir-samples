FROM --platform=linux/amd64 aimle2e/ubuntu:22.04

ENV APP_HOME /app
WORKDIR $APP_HOME

# Install dependencies.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt

# Copy code to container image
COPY model_server.py ./

CMD ["python3", "model_server.py"]