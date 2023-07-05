
FROM svizor/zoomcamp-model:mlops-3.10.0-slim

WORKDIR /app

# Install pipenv
RUN pip install -U pip & pip install pipenv

# Copy the Pipfile and Pipfile.lock to the Docker container
COPY [ "Pipfile", "Pipfile.lock", "./" ]

# Install the dependencies using pipenv
RUN pipenv install --system --deploy

# Copy your script file to the Docker container
COPY ./pycode/batch.py /app/batch.py

# Set the command to run your script, can override the command by passing arguments
CMD ["python", "/app/batch.py", "2022", "4"]

# Set the command to run your script, want to enforce a specific command
# ENTRYPOINT ["python", "/app/batch.py"]
