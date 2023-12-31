from aws_msk_iam_sasl_signer import MSKAuthTokenProvider
from kafka import KafkaProducer
from dotenv import load_dotenv
from datetime import datetime
import random
import socket
import json
import os

load_dotenv()

# BROKERS = "b-1.stocks.8e6izk.c12.kafka.us-east-1.amazonaws.com:9092,b-2.stocks.8e6izk.c12.kafka.us-east-1.amazonaws.com:9092"
BROKERS = os.environ.get("MSK_BROKERS", "localhost:9092")
REGION = "ap-southeast-2"


class MSKTokenProvider():
    def token(self):
        token, _ = MSKAuthTokenProvider.generate_auth_token(REGION)
        return token


tp = MSKTokenProvider()

producer = KafkaProducer(
    bootstrap_servers=BROKERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=str.encode,
    retry_backoff_ms=500,
    request_timeout_ms=20000,
    security_protocol='SASL_SSL',
    sasl_mechanism='OAUTHBEARER',
    sasl_oauth_token_provider=tp,
    client_id=socket.gethostname(),
)


def getReferrer():
    data = {}
    now = datetime.now()
    str_now = now.strftime("%Y-%m-%d %H:%M:%S")
    data['event_time'] = str_now
    data['ticker'] = random.choice(['AAPL', 'AMZN', 'MSFT', 'INTC', 'TBV'])
    price = random.random() * 100
    data['price'] = round(price, 2)
    return data


while True:
    data = getReferrer()
    # print(data)
    try:
        future = producer.send("MSKTutorialTopicStock", value=data, key=data['ticker'])
        producer.flush()
        record_metadata = future.get(timeout=10)
        print("sent event to Kafka! topic {} partition {} offset {}".format(
            record_metadata.topic, record_metadata.partition, record_metadata.offset))
    except Exception as e:
        print(e.with_traceback())
