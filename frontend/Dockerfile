# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /frontend

# Copy the current directory contents into the container at /app
COPY . /frontend

# Install any needed packages specified in requirements.txt
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run streamlit_app.py when the container launches
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
