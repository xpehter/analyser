FROM python:3.7-alpine3.11
ADD analyser.py /
ADD requirements.txt /
RUN pip --no-cache-dir install -r requirements.txt
#CMD [ "python", "./analyser.py" ]
