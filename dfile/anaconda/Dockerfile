FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
  wget \
  && rm -rf /var/lib/apt/list/* \
  && wget https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh \
  && bash Anaconda3-2019.10-Linux-x86_64.sh -b \
  && rm Anaconda3-2019.10-Linux-x86_64.sh

ENV PATH $PATH:/root/anaconda3/bin

CMD python3