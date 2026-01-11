# pull python base image
FROM python:3.10



ADD *.whl .

# update pip
RUN pip install --upgrade pip


# copy API application files into /app in the image
COPY bikeshare_model_api/. bikeshare_model_api/
# install API dependencies
RUN pip install -r bikeshare_model_api/app/requirements.txt
# expose port for application
EXPOSE 8080

# start fastapi application
CMD ["python", "bikeshare_model_api/app/main.py"]
