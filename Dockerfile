FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ['python']
CMD ['run.py']