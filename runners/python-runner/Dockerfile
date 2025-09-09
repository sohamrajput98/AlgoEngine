FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install security updates and create non-root user
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -u 1000 runner

# Copy the run script
COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

# Switch to non-root user
USER runner

# Set resource limits (will be enforced by docker run)
# Memory limit: 128MB
# CPU limit: 0.5 cores
# Time limit: 10 seconds (handled in run.sh)

ENTRYPOINT ["/app/run.sh"]