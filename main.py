import RPi.GPIO as GPIO
import time
import email_module
import detection_module
import platform_module


TRIG = 11  # 17
ECHO = 13  # 27
LED = 15  # 22


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.setup(LED, GPIO.OUT)
    GPIO.output(LED, GPIO.LOW)


def distance():
    GPIO.output(TRIG, 0)
    time.sleep(0.000002)

    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    while GPIO.input(ECHO) == 0:
        a = 0
    time1 = time.time()
    while GPIO.input(ECHO) == 1:
        a = 1
    time2 = time.time()

    during = time2 - time1
    return during * 340/2 * 100


def sendData(message, score):
    email_module.sendmail(message)
    platform_module.send_to_cloud(message, score)


def loop():
    counter = 0
    gate = True
    while True:
        dis = distance()
        time.sleep(0.2)
        if (dis <= 5):
            counter += 1
            if (gate):
                time.sleep(5)
                GPIO.output(LED, GPIO.HIGH)
                detections = detection_module.main()
                GPIO.output(LED, GPIO.LOW)
                gate = False
                if detections:
                    for detection in detections:
                        if (detection.categories[0].score >= 0.4):
                            sendData(str(detection.categories[0].label), float(
                                detection.categories[0].score))
                        elif (detection.categories[0].score < 0.4):
                            sendData("flyer", float(
                                detection.categories[0].score))

            if (counter > 5):
                sendData("clogged", 0.0)
        elif (dis > 5):
            if (counter > 0):
                counter -= 1
            elif (counter <= 0):
                counter = 0
                gate = True


def destroy():
    GPIO.cleanup()


if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
