FROM python:3
RUN mkdir /code
WORKDIR /code
COPY code/requirements.txt /code/
RUN pip3 install -r requirements.txt
RUN pip3 install uwsgi psycopg2-binary
RUN apt-get udpate
RUN apt-get install -y nginx
COPY conf/nginx.conf /etc/nginx/nginx.conf
COPY conf/default.conf /etc/nginx/conf.d/default.conf
COPY code/ /code/
COPY conf/uwsgi.ini /code/
RUN useradd nginx

# init aws cli
RUN apt-get install -y unzip
COPY conf/awscliv2.zip /tmp/
RUN cd /tmp/ && unzip awscliv2.zip
RUN cd /tmp/ && ./aws/install
COPY conf/aws/ /root/.aws/
ENV PYTHONIOENCODING=utf-8


ADD ./conf/start.sh /tmp/start.sh
CMD /bin/sh /tmp/start.sh
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8002"]