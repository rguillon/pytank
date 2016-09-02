import schedule
import json
import logging 


log = logging.Logger(logging.DEBUG)

class TimedSwitch():
    def __init__(self, label, mqttClient, outputPin):
        log.info("Timed switch instance %s created", label)       
        self.label = label
        self.mqttClient = mqttClient
        self.outputPin = outputPin
 
    def name(self):
        return self.label

    def value(self, val):
        return self.outputPin.value(val)

    def set_value(self, val):
        log.info('I/O %s set to %s', self.label, val)
        self.outputPin.value(val)

    def process(self, topics, msg):
        log.info("Message recived for %s, topics: %s, msg:%s",self.label, topics, msg)
        #No leafs are supported
        if len(topics) == 2:
            t = topics[1]
            if t == "on":
                self.set_value(1)
                return
            elif t == "off":
                self.set_value(0)
                return
            elif t == "program":
                params = json.loads(msg)
                self.set_on_time(params["on_time"])
                self.set_off_time(params["off_time"])
                return
        raise TypeError 


    def set_on_time(self, time):
        log.info("Setting on time for %s at %s", self.label, time)
        if hasattr(self, "onJob"):
            schedule.cancel_job(self.onJob)
        self.onJob = schedule.every().day.at(time).do(lambda: self.set_value(1))

    def set_off_time(self, time):
        log.info("Setting off time for %s at %s", self.label, time)
        if hasattr(self, "offJob"):
            schedule.cancel_job(self.offJob)
        self.offJob = schedule.every().day.at(time).do(lambda: self.set_value(0))
