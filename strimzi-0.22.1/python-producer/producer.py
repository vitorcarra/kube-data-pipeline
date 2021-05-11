import json
import threading
import concurrent.futures
import uuid
import logging

from kafka import KafkaProducer
from dotenv import dotenv_values

from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

from datetime import datetime


def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)


def on_send_error(excp):
    log.error('I am an errback', exc_info=excp)
    # handle exception


def send_message(config, avroProducer, **kwargs):
    logging.info("Thread %s: starting", kwargs["car_id"])

    event_key = {
        "car_id": str(kwargs["car_id"])
    }

    event = {
        "car_id": str(kwargs["car_id"]),

        "ts": int(datetime.timestamp(datetime.now()))
    }
    print(event)

    avroProducer.send(
        config['KAFKA_TOPIC_NAME'], event)
    avroProducer.flush()
    logging.info("Thread %s: ending", kwargs["car_id"])


def main():
    # load .env
    config = dotenv_values(".env")

    threads = list()
    # for i in range(1000):
    #     send_message(config, car_id=i, speed=i)
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    value_schema_str = """
{
   "namespace": "car.telemetry",
   "name": "value",
   "type": "record",
   "fields" : [
     {
       "name" : "car_id",
       "type" : "string"
     },
     {
       "name" : "speed",
       "type" : "int"
     },
     { 
        "name": "timestamp", 
        "type": "long",
        "logicalType" : "timestamp-micros"
    }
   ]
}
"""

    key_schema_str = """
{
   "namespace": "car.telemetry",
   "name": "key",
   "type": "record",
   "fields" : [
     {
       "name" : "car_id",
       "type" : "string"
     }
   ]
}
"""
    map_schema = """
{
    "type": "map",
    "values": "string"
}
"""

    value_schema = avro.loads(value_schema_str)
    key_schema = avro.loads(key_schema_str)

    avroProducer = AvroProducer({
        'bootstrap.servers': config['KAFKA_BOOTSTRAP_SERVER'],
        # 'on_delivery': delivery_report,
        'schema.registry.url': 'http://localhost:8081'
    })

    producer = KafkaProducer(
        bootstrap_servers=[config['KAFKA_BOOTSTRAP_SERVER']],
        value_serializer=lambda m: json.dumps(m).encode('utf-8')
    )

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = []
        for i in range(1):
            futures.append(executor.submit(
                send_message, config, producer, car_id=str(i), speed=100)
            )

        for future in concurrent.futures.as_completed(futures):
            print(future.result())


if __name__ == '__main__':
    main()
