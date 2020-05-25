from kafka import KafkaProducer
from datetime import datetime
import random
import time

BOOTSTRAP_SERVER = 'localhost:9092'
TAXI_LOCATION_TOPIC = 'TRIP_TOPIC'
NUMBER_OF_TRIPS = 100000
NUMBER_OF_PASSENGERS = 100000
LOCATION_UPDATE_GAP = 10   # in seconds
NUMBER_OF_CYCLES = 1  # updates per taxi


def send_to_kafka_topic(producer, msg):
    print(str(msg) + "-> sent at time:{0}".format(datetime.now()))
    producer.send(TAXI_LOCATION_TOPIC, msg)
    producer.flush()


def preload_trips(trips):
    for i in range(1, NUMBER_OF_TRIPS+1):
        (v, w, x, y, z) = ('START', i, round(random.uniform(50.010, 50.012), 4), round(random.uniform(0.1, 0.2), 4), 1.5)
        trips.append([v, w, x, y, z])


def format_location(trips, i):
    return "{0},{1},{2},{3},{4},{5}".format(i, trips[i][0], trips[i][1], trips[i][2], trips[i][3], trips[i][4])


def main():
    trips = [[0]]
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER)
    preload_trips(trips)
    sleep_time = float(LOCATION_UPDATE_GAP/NUMBER_OF_TRIPS)
    for j in range(NUMBER_OF_CYCLES):
        for i in range(1, NUMBER_OF_TRIPS+1):
            msg = format_location(trips, i)
            send_to_kafka_topic(producer, bytearray(msg, 'utf8'))
            time.sleep(sleep_time)


if __name__ == "__main__":
    main(),