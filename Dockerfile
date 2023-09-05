# Use a base image with Python installed
FROM python:3.8

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose the port your Flask app will run on
EXPOSE 5000

# Define the command to run your Flask app
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
