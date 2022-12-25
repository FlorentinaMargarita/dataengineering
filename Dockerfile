FROM python:3.11
WORKDIR /app

#we copay all necessary code and data into the container.
COPY models.py   data   ./
# COPY data .

RUN pip install sqlalchemy pg8000

#CMD sets the default command for the image. 
CMD ["python", "models.py"]



#I ran both models together and it worked fine. sds model much faster, has fewer columns but way more rows.
# when I run "docker build Dockerfile" it doesnt work either => seems to give me the right error
#when I run "docker build dataengineering:latest" it also doesn't work
# I ran both models together and it worked fine. 
# Todo: Get Dockerfile working. 
#Todo: Understand each step of the way in detail for the final step of portfolio.
#Todo: t automatically loads the sample data into the chosen database?? Does that mean I should commit the sample data?
