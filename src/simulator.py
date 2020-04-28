from device import SimDevice

thing_id = "0d1af120-0ffc-4294-a6e8-88cf7c1ab3a0"
endpoint = "ai5flye6t910z.iot.eu-west-1.amazonaws.com"
credential_paths = {"ca": "ca.pem.crt", 
                   "private": "private.pem.key", 
                   "certificate":"certificate.pem.crt"}
device_name = "test1"
topic = "data"

SimDevice(thing_id, endpoint, credential_paths, device_name, topic)

# topic = 'data/test1'

# # For certificate based connection
# myMQTTClient = AWSIoTMQTTClient("0d1af120-0ffc-4294-a6e8-88cf7c1ab3a0")
# myMQTTClient.configureEndpoint("ai5flye6t910z.iot.eu-west-1.amazonaws.com", 443)
# myMQTTClient.configureCredentials("ca.pem.crt", "private.pem.key", "certificate.pem.crt")
# myMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
# myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
# myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
# myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
# myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# print("Trying to connect")
# myMQTTClient.connect()
# print("Connected")

# loop_count = 0
# while True:
#     message = {
#         "device_id": "test1",
#         "timestamp": str(datetime.datetime.now()),
#         "flow": random.randint(60, 100),
#         "temperature": random.randint(15, 35),
#         "humidity": random.randint(50, 90),
#         "sound": random.randint(100, 140)
#     }
#     messageJson = json.dumps(message)
#     myMQTTClient.publish(topic, messageJson, 1)
#     print(message)
#     time.sleep(2)