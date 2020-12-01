FROM puckel/docker-airflow:latest

WORKDIR /usr/local/airflow/
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# USER root
# RUN groupadd --gid 999 docker \
# && usermod -aG docker airflow
# RUN pip install docker

# RUN echo "deb http://security.debian.org/debian-security stretch/updates main" >> /etc/apt/sources.list
# RUN mkdir -p /usr/share/man/man1 && \
# apt-get update -y && \
# apt-get install -y openjdk-8-jdk

# RUN apt-get install -y wget

# RUN cd /usr/ \
# && wget "http://apache.mirrors.spacedump.net/spark/spark-2.4.7/spark-2.4.7-bin-hadoop2.7.tgz" \
# && tar xzf spark-2.4.7-bin-hadoop2.7.tgz \
# && rm spark-2.4.7-bin-hadoop2.7.tgz \
# && mv spark-2.4.7-bin-hadoop2.7 spark

# ENV SPARK_HOME /usr/spark
# ENV PATH="/usr/spark/bin:${PATH}"
# ENV SPARK_MAJOR_VERSION 2
# ENV PYTHONPATH=$SPARK_HOME/python/lib/py4j-0.10.4-src.zip:$SPARK_HOME/python/:$PYTHONPATH

# RUN mkdir -p /home/jars
# RUN mkdir -p /home/whl
# RUN mkdir -p /home/lib

# COPY ./lib /home/lib

# WORKDIR /home/
# COPY dlh_dq-0.1-py3-none-any.whl /home/whl
# COPY dlh-dq-core-0.1.jar /home/jars
# RUN pip install wheel
# # RUN pip install apache-airflow
# WORKDIR /home/whl
# RUN pip install dlh_dq-0.1-py3-none-any.whl
# RUN cp dlh_dq-0.1-py3-none-any.whl ../lib

# RUN apt-get update
# RUN apt-get -y install zip

# WORKDIR /home/lib
# RUN zip profiling.zip dlh_dq-0.1-py3-none-any.whl *.py

# RUN mkdir /home/work
# WORKDIR /home/work
# COPY ./scripts .

# USER airflow
#RUN airflow initdb
#RUN airflow scheduler
EXPOSE 8080
