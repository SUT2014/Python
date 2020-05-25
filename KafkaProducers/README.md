# KafkaProducers

KafkaProducers generates data streams for the RideFair application.  

Typical Requirements
  - Generate Trip Information, in CSV format.  <Taxi ID, Passenger ID, Latitudes, longitudes, base rate>..etc
  - Generate Taxi Location information in CSV format.  <Taxi ID, current location in lattitude and longitude>
  - Generate the Taxi Location so that each update for a Taxi arrives at a frequency of 10seconds.
  - Generate Trip information at configured frequency.

# Features!

  - Most common configurations are parameterised.
  - Multiple instances of the producers can be run to increase frequency with minimum changes to the script.
  - Capacity only limited by the underlying hardware.
  
KafkaProducers has been developed using the following tools/apps:

* [kafka] - Open Source Stream Processing Software platform (kafka-python)
* [Python] - Pythong 3.8 
* [IntelliJ] - PyCharm

### Installation

Run each script with required configuration on a Python installed server.  
kafka-python required.

Create Kafka Topics using the following commands...

```sh
$ kafka-topics.sh --zookeeper localhost:2181 --create --topic TRIP_TOPIC --partitions 3 --replication-factor 1
$ kafka-topics.sh --zookeeper localhost:2181 --create --topic TAXI_LOCATION_TOPIC --partitions 3 --replication-factor 1
```

Generated Logs...
```sh
Taxi Location Update Stream
bytearray(b'4974,50.009,0.1685')-> sent at time:2020-05-25 19:10:49.211507
bytearray(b'4975,50.0082,0.1482')-> sent at time:2020-05-25 19:10:49.212555

Trip Stream
bytearray(b'1,START,1,50.0112,0.1199,1.5')-> sent at time:2020-05-25 19:11:39.636685
```


**Free Software, Hell Yeah!**