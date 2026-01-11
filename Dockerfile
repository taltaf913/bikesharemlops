# pull python base image
FROM python:3.10

ADD requirements.txt requirements.txt

ADD *.whl .

# update pip
RUN pip install --upgrade pip


# copy application files
COPY app/. app/.
# install dependencies
RUN pip install -r requirements.txt
# expose port for application
EXPOSE 8080

# start fastapi application
CMD ["python", "app/main.py"]
