FROM docker.elastic.co/logstash/logstash:8.17.1
RUN mkdir /usr/share/logstash/drivers
COPY ./drivers/* /usr/share/logstash/drivers/
RUN logstash-plugin install logstash-integration-jdbc
RUN logstash-plugin install logstash-output-elasticsearch