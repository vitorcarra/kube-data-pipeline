FROM quay.io/strimzi/kafka:0.22.1-kafka-2.7.0
USER root:root

COPY ./plugins/* /opt/kafka/plugins/
RUN cd /opt/kafka/plugins/ && tar -xvzf kafka-connect-cassandra-sink-1.4.0.tar.gz
RUN cd /opt/kafka/plugins/ && unzip /opt/kafka/plugins/confluentinc-kafka-connect-s3-10.0.0.zip
RUN cd /opt/kafka/plugins/ && tar -xvzf camel-cql-kafka-connector-0.8.0-package.tar.gz
RUN cd /opt/kafka/plugins/ && unzip yugabyteinc-yb-kafka-connector-1.0.0.zip

RUN cd /opt/kafka/plugins/yugabyteinc-yb-kafka-connector-1.0.0
RUN curl -O https://repo1.maven.org/maven2/io/netty/netty-all/4.1.51.Final/netty-all-4.1.51.Final.jar
RUN curl -O https://repo1.maven.org/maven2/com/yugabyte/cassandra-driver-core/3.8.0-yb-5/cassandra-driver-core-3.8.0-yb-5.jar
RUN curl -O https://repo1.maven.org/maven2/io/dropwizard/metrics/metrics-core/4.1.11/metrics-core-4.1.11.jar

RUN rm /opt/kafka/plugins/kafka-connect-cassandra-sink-1.4.0.tar.gz
RUN rm /opt/kafka/plugins/confluentinc-kafka-connect-s3-10.0.0.zip
RUN rm /opt/kafka/plugins/camel-cql-kafka-connector-0.8.0-package.tar.gz
RUN rm /opt/kafka/plugins/yugabyteinc-yb-kafka-connector-1.0.0.zip

USER 1001