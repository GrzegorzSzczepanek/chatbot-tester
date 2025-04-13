# Use a slim Python base image that matches your pyproject.toml version
FROM python:3.13-slim

# Set environment variables
ENV POETRY_VERSION=1.6.1
ENV PATH="/root/.local/bin:$PATH"

# Update base packages and install curl (needed to install Poetry)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION

# Create a working directory
WORKDIR /app

# Copy only the pyproject.toml (and poetry.lock if you have one) first for caching
COPY pyproject.toml /app
# COPY poetry.lock /app  # Uncomment if you have a poetry.lock

# Install dependencies (no dev deps if you'd like to minimize container size)
RUN poetry install --no-root

# Copy the rest of your application code
COPY . /app

# Install again in case new dependencies were introduced in your code
RUN poetry install --no-root

# Expose the Flask port
EXPOSE 5000

# Set the default command to run your Flask app
# If your "app.py" defines a Flask instance named `app`, 
# then run it by specifying --app app.py
CMD ["poetry", "run", "flask", "--app", "app.py", "run", "--host=0.0.0.0", "--port=5000"]

