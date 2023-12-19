# aws-msk

## MSK x EC2

https://docs.aws.amazon.com/msk/latest/developerguide/getting-started.html

### Step1 ===============

https://docs.aws.amazon.com/msk/latest/developerguide/create-cluster.html

MSKTutorialCluster

Apache Kafka version
3.5.1

arn:aws:kafka:ap-southeast-2:account-id:cluster/MSKTutorialCluster/xxxxxx

All cluster settings
If you want to customize these cluster settings, choose create cluster with custom settings above.

Setting
Value
Editable after cluster creation
Cluster type	Provisioned	No
Apache Kafka version	3.5.1	Yes
Cluster configuration	MSK default	Yes
VPC	vpc-vpc-id (default)	No
Subnets	
subnet-xxxxxx 
subnet-xxxxxx 
subnet-xxxxxx 
No
Public access	Off	Yes
Security groups associated with VPC	
sg-xxxxxx 
No
Zones	3	No
Broker type	kafka.m7g.large	Yes
Brokers per zone	1	Yes
Cluster storage mode	EBS storage only	Yes
Storage	100 GiB	Yes
Provisioned storage throughput per broker	Not enabled	Yes
Access control method	IAM	Yes
Encryption within the cluster	Enabled - TLS	No
Encryption between clients - brokers	Enabled - TLS	Yes
Encryption for data at rest	Use AWS managed CMK	No
Monitoring metrics	Basic (default)	Yes
Open monitoring with Prometheus	Not enabled	Yes
Broker log delivery	Not enabled	Yes
Cluster tags	-	Yes

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

in MSK instance's vpn console, select msk sg, add inbound rule from source EC2 sg. 

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


Bootstrap servers
go msk > View client information > Private endpoint (single-VPC)
b-1.xxx.amazonaws.com:9098,b-2.xxx.amazonaws.com:9098,b-3.xxx.amazonaws.com:9098

./kafka-topics.sh --create --bootstrap-server b-1.xxx.amazonaws.com:9098 --command-config client.properties --replication-factor 3 --partitions 1 --topic MSKTutorialTopic

### Step5 ===============

./kafka-console-producer.sh --broker-list b-1.xxx.amazonaws.com:9098 --producer.config client.properties --topic MSKTutorialTopic


./kafka-console-consumer.sh --bootstrap-server b-1.xxx.amazonaws.com:9098 --consumer.config client.properties --topic MSKTutorialTopic --from-beginning


### Step6 ===============

Try out various metrics in cloud watch

### Step7 ===============

https://docs.aws.amazon.com/msk/latest/developerguide/delete-cluster.html


## MSK x Lambda

comming soon ... 


