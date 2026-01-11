# pull python base image
FROM python:3.10


ADD /bikeshare_model_api /bikeshare_model_api/
ADD *.whl .
WORKDIR /bikeshare_model_api

# update pip
RUN pip install --upgrade pip



# install API dependencies
RUN pip install -r app/requirements.txt
# expose port for application
EXPOSE 8001

# start fastapi application
CMD ["python", "app/main.py"]
