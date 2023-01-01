FROM python:3.11
WORKDIR /app

#we copay all necessary code and data into the container.
COPY models.py   data   ./

RUN pip install sqlalchemy pg8000

#CMD sets the default command for the image. 
CMD ["python", "models.py"]
