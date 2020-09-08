FROM fedora:32
USER root
RUN dnf install -y python-pip ttyd
COPY . /app
WORKDIR /app
RUN pip install .
CMD ttyd -p 8080 dcbattle
EXPOSE 8080
