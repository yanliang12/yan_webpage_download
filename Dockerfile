############Dockerfile###########
FROM openjdk:8

RUN apt-get update
RUN apt-get install -y wget
RUN apt-get install -y git 
RUN apt-get install -y curl
RUN apt-get install -y vim
RUN apt-get install -y tar
RUN apt-get install -y bzip2

RUN apt-get update
RUN apt-get install -y python3-dev
RUN apt-get install -y python3-pip

####neo4j
RUN pip3 install gdown==3.12.2
RUN pip3 install rdflib==5.0.0
RUN pip3 install requests==2.24.0
RUN pip3 install pandas==1.1.3
RUN pip3 install elasticsearch==7.11.0
RUN pip3 install pyspark==3.1.1
RUN pip3 install esdk-obs-python==3.20.11 --trusted-host pypi.org
RUN pip3 install Pillow==8.2.0

WORKDIR /

####

RUN mkdir /home/yan
RUN chmod 777 /home/yan

RUN useradd -u 8877 yan
USER yan

####

ENV PYSPARK_PYTHON=/usr/bin/python3
ENV PYSPARK_DRIVER_PYTHON=/usr/bin/python3

####

WORKDIR /home/yan/
RUN wget https://obs-community.obs.cn-north-1.myhuaweicloud.com/obsutil/current/obsutil_linux_amd64.tar.gz
RUN tar -xzvf obsutil_linux_amd64.tar.gz

WORKDIR /home/yan/obsutil_linux_amd64_5.2.12
RUN chmod 755 obsutil

WORKDIR /home/yan/

RUN echo "sdg2g2g2r"

RUN git clone https://yanliang12:Gnewjrog34895@github.com/yanliang12/yan_webpage_download.git
RUN mv yan_webpage_download/* ./
RUN rm -r yan_webpage_download
############Dockerfile############
