from ..function.scheduler import Scheduler
from . import mqtt_handler
import time

def main():
    mqtt = mqtt_handler.MQTTHandler(
        broker="test.mosquitto.org",
        port=1883,
        pub_topic="mqtt/afdhal/data",
        sub_topic="mqtt/afdhal/command",
    )
    scheduler = Scheduler(mqtt.publish_sensor_data, interval=5)
    mqtt.set_scheduler(scheduler)
    scheduler.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Stopping...")
        scheduler.stop()
        mqtt.client.loop_stop()
        mqtt.client.disconnect()


if __name__ == "__main__":
    main()