from ..function import time_utils
import paho.mqtt.client as mqtt
from . import sensor_handler
import json


class MQTTHandler:
    def __init__(self, broker, port, pub_topic, sub_topic):
        self.pub_topic = pub_topic
        self.sub_topic = sub_topic
        self.client = mqtt.Client()

        # callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe

        # connect & subscribe
        self.client.connect(broker, port)
        self.client.subscribe(self.sub_topic, qos=1 )
        self.client.loop_start()
    
    def on_connect(self, client, userdata, flags, reason_code):
        print(f"[INFO]Connected with result code {reason_code}")

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print(f"[INFO]Subscribed to {self.sub_topic}")

    def on_publish(self, client, userdata, mid):
        pass

    def on_message(self, client, userdata, msg):
        message = str((msg.payload.decode("utf-8")))
        try:
            message = json.loads(message)
        except json.JSONDecodeError:
            print("Invalid JSON received.")
            return

        print("Timestamp: "+time_utils.getTimeinTimezone(7) +
              "\nAction: Subscribe\nTopic: "+str(msg.topic)+"\nData: "+str(message))

        if "command" in message:
            command = message["command"]
            if "pause" in command:
                self.scheduler.pause()
            elif "resume" in command:
                self.scheduler.resume()
            elif "set_interval" in command:
                parts = command.split(":", 1)
                # check if argument is exist
                arg = parts[1] if len(parts) > 1 else None

                if arg is not None and arg.isdigit():
                    interval = int(arg)
                    self.scheduler.set_interval(interval)
                else:
                    print(
                        '[ERROR] Invalid set_interval command. Use: {"command": "set_interval:10"}')
            else:
                print(f"[WARN] Unknown command received: {command}")

    def publish(self, payload):
        msg_info = self.client.publish(
            self.pub_topic, payload, qos=1)
        return msg_info
    
    def publish_sensor_data(self):
        data = sensor_handler.get_sensor_data()
        payload = {"nama": "Afdhal",
                "data": {
                    "sensor1": data[0],
                    "sensor2": data[1],
                    "sensor3": data[2],
                    "sensor4": data[3],
                    "sensor5": data[4],
                },
                "timestamp": time_utils.getTimeUTC()
                }    
        msg_info = self.publish(payload=str(payload))
        msg_info.wait_for_publish()
        state = "success" if msg_info.is_published() else "failed"
        print("Timestamp: "+time_utils.getTimeinTimezone(7) +
              "\nAction: Publish\nTopic: "+self.pub_topic+"\nData: "+str(payload)+"\nState: "+state)
        sensor_handler.log_to_csv(data, state)
        
    def set_scheduler(self, scheduler):
        self.scheduler = scheduler