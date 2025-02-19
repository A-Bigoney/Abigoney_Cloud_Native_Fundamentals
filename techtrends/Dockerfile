# Use a Python base image in version 3.8
FROM python:3.8

# Set the working directory in the container
WORKDIR /techtrends

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install packages defined in the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files to the container
COPY . .

# Ensure that the database is initialized with the pre-defined posts in the init_db.py file
RUN python init_db.py

# Expose the application port 3111
EXPOSE 3111

# Command to run the application at container start
CMD ["python", "app.py"]
