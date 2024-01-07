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

```bash
mvn clean package -Dflink.version=1.15.3
```
