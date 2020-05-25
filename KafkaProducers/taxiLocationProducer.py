from kafka import KafkaProducer
from datetime import datetime
import random
import time

BOOTSTRAP_SERVER = 'localhost:9092'
TAXI_LOCATION_TOPIC = 'TAXI_LOCATION_TOPIC'
NUMBER_OF_TAXIS = 100000
LOCATION_UPDATE_GAP = 10   # in seconds
NUMBER_OF_CYCLES = 500  # updates per taxi


def send_to_kafka_topic(producer, msg):
    print(str(msg) + "-> sent at time:{0}".format(datetime.now()))
    producer.send(TAXI_LOCATION_TOPIC, msg)
    producer.flush()


def preload_coordinates(taxi_location):
    for i in range(1, NUMBER_OF_TAXIS+1):
        (x, y) = (round(random.uniform(50.010, 50.012), 4), round(random.uniform(0.1, 0.2), 4))
        taxi_location.append([x, y])


def format_location(taxi_location, i):
    # do a random update and report the location
    temp1 = round((taxi_location[i][0]+.002 if random.randint(1, 10) % 2 else taxi_location[i][0]-.002), 4)
    temp2 = round((taxi_location[i][1] + .002 if random.randint(1, 10) % 2 else taxi_location[i][1] - .002), 4)
    return "{0},{1},{2}".format(i, temp1, temp2)


def main():
    taxi_location = [[0]]
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER)
    preload_coordinates(taxi_location)
    sleep_time = float(LOCATION_UPDATE_GAP/NUMBER_OF_TAXIS)
    for j in range(NUMBER_OF_CYCLES):
        for i in range(1, NUMBER_OF_TAXIS+1):
            msg = format_location(taxi_location, i)
            send_to_kafka_topic(producer, bytearray(msg, 'utf8'))
            time.sleep(sleep_time)


if __name__ == "__main__":
    main(),