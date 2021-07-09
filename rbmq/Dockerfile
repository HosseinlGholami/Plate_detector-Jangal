FROM rabbitmq:3-management

COPY ./Conf/definitions.json /etc/rabbitmq/
COPY ./Conf/enabled_plugins /etc/rabbitmq/
COPY ./Conf/rabbitmq.conf /etc/rabbitmq/

EXPOSE 5672
EXPOSE 15672
