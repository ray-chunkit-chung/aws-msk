# Flink-Kinesis getting started

<https://docs.aws.amazon.com/managed-flink/latest/java/get-started-exercise.html>

<https://github.com/aws-samples/amazon-kinesis-data-analytics-examples>

## Create Kinesis i/o stream

```bash
aws kinesis create-stream --stream-name ExampleInputStream --shard-count 1 --region ap-southeast-2 --profile dev
aws kinesis create-stream --stream-name ExampleOutputStream --shard-count 1 --region ap-southeast-2 --profile dev
```

## Create dummy data to send to kinesis

```bash
python send_data.py
```

## Create flink job to send data from input to output stream

Upload flink jar to s3. Example flink jar path:

s3://mks-tutorial-cluster/flink-jar/aws-kinesis-analytics-java-apps-1.0.jar

## Create role for flink

Simplest role/policy can be s3 full access and kinesis full access for testing purpose. More precise policy can be

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "ReadCode",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:GetObjectVersion"
            ],
            "Resource": [
                "arn:aws:s3:::ka-app-code-username/aws-kinesis-analytics-java-apps-1.0.jar"
            ]
        },
        {
            "Sid": "DescribeLogGroups",
            "Effect": "Allow",
            "Action": [
                "logs:DescribeLogGroups"
            ],
            "Resource": [
                "arn:aws:logs:us-west-2:012345678901:log-group:*"
            ]
        },
        {
            "Sid": "DescribeLogStreams",
            "Effect": "Allow",
            "Action": [
                "logs:DescribeLogStreams"
            ],
            "Resource": [
                "arn:aws:logs:us-west-2:012345678901:log-group:/aws/kinesis-analytics/MyApplication:log-stream:*"
            ]
        },
        {
            "Sid": "PutLogEvents",
            "Effect": "Allow",
            "Action": [
                "logs:PutLogEvents"
            ],
            "Resource": [
                "arn:aws:logs:us-west-2:012345678901:log-group:/aws/kinesis-analytics/MyApplication:log-stream:kinesis-analytics-log-stream"
            ]
        },
        {
            "Sid": "ReadInputStream",
            "Effect": "Allow",
            "Action": "kinesis:*",
            "Resource": "arn:aws:kinesis:us-west-2:012345678901:stream/ExampleInputStream"
        },
        {
            "Sid": "WriteOutputStream",
            "Effect": "Allow",
            "Action": "kinesis:*",
            "Resource": "arn:aws:kinesis:us-west-2:012345678901:stream/ExampleOutputStream"
        }
    ]
}
```
