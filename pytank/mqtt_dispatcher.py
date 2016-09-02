import umqtt.robust
import logging


log = logging.Logger(logging.DEBUG)


class MQTTDispatcherClient(umqtt.robust.MQTTClient):

    def __init__(self, client_id, rootTopic, server, port=0, user=None, password=None, ssl=False):
        super().__init__(client_id,server,port,user,password,ssl)
        self.rootTopic=rootTopic
        self.connect()
        self.set_callback(self._dispatcher_callback_)
        self.subscribe(rootTopic+"/#")
        self.children = {}

    def _dispatcher_callback_(self, topic, msg):
        topics = topic.decode("utf-8").split("/")
        # assert (topics[0]==self.rootTopic)
        if ((len(topics)>2) & (topics[0] == self.rootTopic)):
            if topics[1] in self.children:
                try:
                    self.children[topics[1]].process(topics[1:],msg.decode("utf-8"))
                    return
                except ValueError:
                    pass
        
        log.error("Invalid message [%s] on topic [%s]",msg,topic)
                

    def register_child(self, child):
        self.children[child.name()] = child

