# aws-msk

Demonstration of Kafka streaming data to model training server for online learning

## MSK x EC2

<https://docs.aws.amazon.com/msk/latest/developerguide/getting-started.html>

### Step1 ===============

<https://docs.aws.amazon.com/msk/latest/developerguide/create-cluster.html>

MSKTutorialCluster

Apache Kafka version
3.5.1

arn:aws:kafka:ap-southeast-2:account-id:cluster/MSKTutorialCluster/xxxxxx

All cluster settings
If you want to customize these cluster settings, choose create cluster with custom settings above.

Setting
Value
Editable after cluster creation
Cluster type Provisioned No
Apache Kafka version 3.5.1 Yes
Cluster configuration MSK default Yes
VPC vpc-vpc-id (default) No
Subnets
subnet-xxxxxx
subnet-xxxxxx
subnet-xxxxxx
No
Public access Off Yes
Security groups associated with VPC
sg-xxxxxx
No
Zones 3 No
Broker type kafka.m7g.large Yes
Brokers per zone 1 Yes
Cluster storage mode EBS storage only Yes
Storage 100 GiB Yes
Provisioned storage throughput per broker Not enabled Yes
Access control method IAM Yes
Encryption within the cluster Enabled - TLS No
Encryption between clients - brokers Enabled - TLS Yes
Encryption for data at rest Use AWS managed CMK No
Monitoring metrics Basic (default) Yes
Open monitoring with Prometheus Not enabled Yes
Broker log delivery Not enabled Yes
Cluster tags - Yes

### Step2 ===============

MSKTutorialCluster

policy

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "kafka-cluster:Connect",
                "kafka-cluster:AlterCluster",
                "kafka-cluster:DescribeCluster"
            ],
            "Resource": [
                "arn:aws:kafka:ap-southeast-2:account-id:cluster/MSKTutorialCluster/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "kafka-cluster:*Topic*",
                "kafka-cluster:WriteData",
                "kafka-cluster:ReadData"
            ],
            "Resource": [
                "arn:aws:kafka:ap-southeast-2:account-id:topic/MSKTutorialCluster/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "kafka-cluster:AlterGroup",
                "kafka-cluster:DescribeGroup"
            ],
            "Resource": [
                "arn:aws:kafka:ap-southeast-2:account-id:group/MSKTutorialCluster/*"
            ]
        }
    ]
}
```

roles
MSKTutorialClusterEC2

### Step3 ===============

Create client EC2 for demo/test
MSKTutorialClusterEC2
sg-xxxxxx

in MSK instance's vpc console, select msk sg, add inbound rule from source EC2 sg.

### Step4 ===============

```bash
sudo yum -y install java-11
wget https://archive.apache.org/dist/kafka/3.5.1/kafka_2.13-3.5.1.tgz
tar -xzf kafka_2.13-3.5.1.tgz

cd kafka_2.13-3.5.1/libs
wget https://github.com/aws/aws-msk-iam-auth/releases/download/v1.1.1/aws-msk-iam-auth-1.1.1-all.jar

cd ../bin
vi client.properties
security.protocol=SASL_SSL
sasl.mechanism=AWS_MSK_IAM
sasl.jaas.config=software.amazon.msk.auth.iam.IAMLoginModule required;
sasl.client.callback.handler.class=software.amazon.msk.auth.iam.IAMClientCallbackHandler
:wq
```

Check Bootstrap servers
go msk > View client information > Private endpoint (single-VPC)
b-1.xxx.amazonaws.com:xxxx,b-2.xxx.amazonaws.com:xxxx,b-3.xxx.amazonaws.com:xxxx

Create .env file

> export MSK_BROKERS=b-1.xxx.amazonaws.com:xxxx,b-2.xxx.amazonaws.com:xxxx,b-3.xxx.amazonaws.com:xxxx

Create topic

```bash
./kafka-topics.sh --create --bootstrap-server $MSK_BROKERS --command-config client.properties --replication-factor 3 --partitions 1 --topic MSKTutorialTopic
```

### Step5 ===============

Test producer

```bash
./kafka-console-producer.sh --broker-list $MSK_BROKERS --producer.config client.properties --topic MSKTutorialTopic
```

Test consumer

```bash
./kafka-console-consumer.sh --bootstrap-server $MSK_BROKERS --consumer.config client.properties --topic MSKTutorialTopic --from-beginning
```

### Step6 ===============

Try out various metrics in cloud watch

### Step7 ===============

Delete all resources

<https://docs.aws.amazon.com/msk/latest/developerguide/delete-cluster.html>

## Flink consumer with S3 sink

<https://sid-sharma.medium.com/click-stream-processing-on-apache-flink-using-kafka-source-and-aws-s3-sink-b12e6ece783e>

<https://sid-sharma.medium.com/distributed-batch-processing-using-apache-flink-on-aws-emr-yarn-cluster-930f73d84156>

<https://gist.github.com/ssharma>

Setup test environment on EC2. Assume EC2 has rol kafka read/write role and inbound traffic to kafka is allowed

```bash
# install package
sudo yum install python3-pip git -y

# install python package
pip install --upgrade tensorflow \
tensorflow-datasets \
tensorflow-io \
keras \
pandas \
python-dotenv \
kafka-python \
scikit-learn \
Jinja2 \
aws-msk-iam-sasl-signer-python

# download src
https://github.com/ray-chunkit-chung/ml-recommendation-engine-part3-data-etl
```

### Producer

A sample python data producer to test the MSK. Need an MSK IAM SASAL signer

<https://github.com/aws/aws-msk-iam-sasl-signer-python>

```py
from aws_msk_iam_sasl_signer import MSKAuthTokenProvider
from kafka import KafkaProducer
import socket

class MSKTokenProvider():
    def token(self):
        token, _ = MSKAuthTokenProvider.generate_auth_token('ap-southeast-2')
        return token

tp = MSKTokenProvider()

producer = KafkaProducer(
    bootstrap_servers=['xxxx'],
    security_protocol='SASL_SSL',
    sasl_mechanism='OAUTHBEARER',
    sasl_oauth_token_provider=tp,
    client_id=socket.gethostname(),
)

v = producer.send('MSKTutorialTopic', b'test')
metadata = v.get(timeout=10)
print(v)
```

```py
from aws_msk_iam_sasl_signer import MSKAuthTokenProvider
from kafka import KafkaProducer
import tensorflow_datasets as tfds
import socket
import os

class MSKTokenProvider():
    def token(self):
        token, _ = MSKAuthTokenProvider.generate_auth_token('ap-southeast-2')
        return token

tp = MSKTokenProvider()

producer = KafkaProducer(
    bootstrap_servers=['b-1.xxxx.amazonaws.com:xxxx'],
    security_protocol='SASL_SSL',
    sasl_mechanism='OAUTHBEARER',
    sasl_oauth_token_provider=tp,
    client_id=socket.gethostname(),
)

data = tfds.load("movielens/1m-ratings")


df = tfds.as_dataframe(data["train"])

filtered_data = (
    df.filter(["timestamp", "user_id", "movie_id", "user_rating"])
    .sort_values("timestamp")
    .astype({"user_id": int, "movie_id": int, "user_rating": int})  # nicer types
    .drop(columns=["timestamp"])  # don't need the timestamp anymore
)

# We will also keep the timestamp to conduct a temporal train-test split since
#  this resembles how we train in real life: we train now, but we want the model
# to work well tomorrow. So we should evaluate the model quality like this as well.
train = filtered_data.iloc[:900000]  # chronologically first 90% of the dataset
test = filtered_data.iloc[900000:]  # chronologically last 10% of the dataset

x_train = list(filter(None, train[["user_id","movie_id"]].to_csv(index=False).split("\n")[1:]))
y_train = list(filter(None, train[["user_rating"]].to_csv(index=False).split("\n")[1:]))
x_test = list(filter(None, test[["user_id","movie_id"]].to_csv(index=False).split("\n")[1:]))
y_test = list(filter(None, test[["user_rating"]].to_csv(index=False).split("\n")[1:]))

def error_callback(exc):
      raise Exception('Error while sending data to kafka: {0}'.format(str(exc)))


def write_to_kafka(topic_name, items):
      count=0
      for message, key in items:
        print(message.encode('utf-8'))
        producer.send(topic_name,
                      key=key.encode('utf-8'),
                      value=message.encode('utf-8')).add_errback(error_callback)
        count+=1
      producer.flush()
      print("Wrote {0} messages into topic: {1}".format(count, topic_name))

write_to_kafka("MSKTutorialTopic", zip(x_train, y_train))
print(v)
```

### Consumer

<https://docs.aws.amazon.com/managed-flink/latest/java/getting-started.html?pg=ln&cp=bn>

<https://github.com/aws-samples/amazon-kinesis-data-analytics-flink-starter-kit?tab=readme-ov-file>

<https://github.com/aws-samples/amazon-managed-service-for-apache-flink-examples?tab=readme-ov-file>

<https://github.com/aws-samples/amazon-kinesis-data-analytics-examples/blob/master/GettingStarted/src/main/java/com/amazonaws/services/kinesisanalytics/BasicStreamingJob.java>

<https://nightlies.apache.org/flink/flink-docs-release-1.12/dev/python/datastream-api-users-guide/intro_to_datastream_api.html>

Coming soon...

# Terraform MSK

<https://registry.terraform.io/modules/terraform-aws-modules/msk-kafka-cluster/aws/latest/examples/complete>

Coming soon...

## MSK x Lambda (Will not do)

<https://aws.amazon.com/blogs/compute/using-amazon-msk-as-an-event-source-for-aws-lambda/>

<https://catalog.us-east-1.prod.workshops.aws/workshops/c2b72b6f-666b-4596-b8bc-bafa5dcca741/en-US/msklambda>

<https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes.html>

Secret manager
<https://docs.aws.amazon.com/lambda/latest/dg/with-msk.html>

comming soon ...
