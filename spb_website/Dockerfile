# Use a slim Python base image for smaller image size
FROM python:3.13.5-slim-bookworm

# Set the working directory inside the container
WORKDIR /spb_website

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY . .

# Expose the port your Flask spb_website will run on (default is 5000)
EXPOSE 2980

# Command to run the Flask application using Gunicorn (recommended for production)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]