# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY . .

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Define environment variables
ENV PYTHONPATH="${PYTHONPATH}:/app/src"
ENV GOOGLE_API_KEY=${GOOGLE_API_KEY}

# Run the application
CMD ["streamlit", "run", "src/presentation/ui/pages/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
