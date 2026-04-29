# API Test Automation Framework — Docker image
# Runs the entire test suite (API + UI) in an isolated container.

# Microsoft's official Playwright image already has the OS deps
# and the browsers (Chromium, Firefox, WebKit) pre-installed.
FROM mcr.microsoft.com/playwright/python:v1.51.0-noble

WORKDIR /app

# Install Python deps first so Docker can cache the layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Default command runs the test suite
CMD ["pytest", "-v"]
