# Dockerfile

FROM python:3.9-buster

# copy source and install dependencies
RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/pip_cache
COPY requirements.txt start-server.sh /opt/app/
COPY banking_battle /opt/app/banking_battle
WORKDIR /opt/app
RUN pip install pip --upgrade
RUN pip install -r requirements.txt --cache-dir /opt/app/pip_cache

# start server
EXPOSE 8010
STOPSIGNAL SIGTERM
CMD ["/opt/app/start-server.sh"]