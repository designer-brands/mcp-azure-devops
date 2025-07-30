# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Set environment variables for Azure DevOps
ENV AZURE_DEVOPS_PAT=""
ENV AZURE_DEVOPS_ORGANIZATION_URL=""

# Install uv
RUN pip install uv

# Copy the entire project context
COPY . .

# Install dependencies
RUN uv pip install --system -e ".[dev]"

# Expose the port the app runs on
EXPOSE 8000

# Run the application, binding to all interfaces on port 8000
CMD ["python", "src/mcp_azure_devops/server.py"]
