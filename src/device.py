from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import datetime
import random
import time
import argparse

class SimDevice():
    def __init__(self, thing_id, endpoint, credential_paths, device_name, topic):
        print("Trying to setup Device")
        myMQTTClient = AWSIoTMQTTClient(thing_id)
        myMQTTClient.configureEndpoint(endpoint, 443)
        myMQTTClient.configureCredentials(credential_paths["ca"], 
                                          credential_paths["private"], 
                                          credential_paths["certificate"])
        
        myMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
        myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
        print("Setup Done")
        
        print("Trying to connect")
        myMQTTClient.connect()
        print("Connected")
        
        self.loop_data(myMQTTClient, device_name, topic)
        
    
    def loop_data(self, mqtt_client, device_name, topic):
        while True:
            message = {
                "device_id": device_name,
                "timestamp": str(datetime.datetime.now()),
                "flow": random.randint(60, 100),
                "temperature": random.randint(15, 35),
                "humidity": random.randint(50, 90),
                "sound": random.randint(100, 140)
            }
            messageJson = json.dumps(message)
            mqtt_client.publish(topic+"/"+device_name, messageJson, 1)
            print(message)
            time.sleep(5)
            
# Read in command-line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", action="store", required=True, dest="endpoint", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="basicPubSub",
                    help="Targeted client id")
parser.add_argument("-t", "--topic", action="store", dest="topic", default="sdk/test/Python", help="Targeted topic")
parser.add_argument("-n", "--name", action="store", dest="name")

args = parser.parse_args()
endpoint = args.endpoint
credential_paths = {"ca": args.rootCAPath, "private":args.privateKeyPath , "certificate": args.certificatePath}
clientId = args.clientId
topic = args.topic
name = args.name


print(clientId, endpoint, credential_paths, name, "data")
SimDevice(clientId, endpoint, credential_paths, name, "data")