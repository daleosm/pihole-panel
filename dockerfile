FROM ubuntu:latest
USER root
RUN apt-get update
RUN apt-get install -y python3 python3-gi
