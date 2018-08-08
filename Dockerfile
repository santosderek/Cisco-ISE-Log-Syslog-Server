FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 80/tcp
EXPOSE 8514/udp
ENTRYPOINT ["python3"]
CMD ["run.py"]
