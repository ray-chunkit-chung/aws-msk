# Flink-Kafka-S3 getting started

<https://docs.aws.amazon.com/managed-flink/latest/java/gs-table-create.html>

Create .env to export brokers

```
export MSK_BROKERS=b-1.xxxx.amazonaws.com:xxxxx,b-2.xxxx.amazonaws.com:xxxx,b-3.xxxx.amazonaws.com:xxxx
export MSK_TOPIC=xxxx
export S3_PATH=xxxx
```

Producer test on EC2 (Assume EC2 has correct roles and MSK inbound rule)

```bash
python ./FlinkKafkaS3/src/main/python/stock.py
```

Package flink app and upload jar to s3

```bash
mvn clean package -Dflink.version=1.15.3
```

Create aws managed flink streaming app and link to the flink jar

Setup network and config properites suggested below.

https://docs.aws.amazon.com/managed-flink/latest/java/example-msk.html

https://docs.aws.amazon.com/managed-flink/latest/java/vpc.html

https://jaehyeon.me/blog/2023-10-26-real-time-streaming-with-kafka-and-flink-2/


May need IAM auth for MSK connection

https://stackoverflow.com/questions/72398012/failed-to-construct-kafka-consumer-in-flink-cluster-for-connecting-to-msk
 
AWS lib aws-msk-iam-auth-1.1.4-all.jar and Kafka lib kafka-clients-2.4.1.jar into /opt/flink/lib folder inside the Flink nodes.


https://stackoverflow.com/questions/77716072/timeout-exception-for-node-assignment-call-describetopics-in-managed-apache-fl


https://stackoverflow.com/questions/72398012/failed-to-construct-kafka-consumer-in-flink-cluster-for-connecting-to-msk


