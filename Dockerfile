# Base Python image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Create virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy only the folder you need into the container
COPY ai_app /app

# Install dependencies (assuming requirements.txt is inside api.kit)
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Run Flask app
CMD ["python", "app.py"]
