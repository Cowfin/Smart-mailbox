from google.cloud import pubsub_v1
import json
import time

project_id = ""  # enter your project id here
topic_name = ""  # enter the name of the topic that you created

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)

futures = dict()


def get_callback(f, data):
    def callback(f):
        try:
            futures.pop(data)
        except:
            print("Please handle {} for {}.".format(f.exception(), data))

    return callback


def send_to_cloud(message, score):
    timenow = float(time.time())
    data = {"time": timenow, "type_of_mail": message, "score": score}
    print(data)
    future = publisher.publish(
        topic_path, data=(json.dumps(data)).encode("utf-8"))
    future.add_done_callback(get_callback(future, data))
    time.sleep(1)


while futures:
    time.sleep(5)

print("Published message with error handler.")
