FROM python:3.8


WORKDIR /app


COPY requirements.txt /app/


RUN pip install --no-cache-dir -r requirements.txt


COPY src /app/src/
COPY geotif.py /app

# Default command to run when starting the container
ENTRYPOINT ["python", "./geotif.py"]

# Default arguments for main.py
CMD ["--help"]