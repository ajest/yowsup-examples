from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities import OutgoingAckProtocolEntity
from yowsup.layers.protocol_presence.protocolentities import PresenceProtocolEntity
import threading
import logging

logger = logging.getLogger(__name__)
recv_msg = []

class EchoLayer(YowInterfaceLayer):

    def __init__(self):
        super(EchoLayer, self).__init__()
        self.ackQueue = []
        self.lock = threading.Condition()

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        if messageProtocolEntity.getType() == 'text':
            recv_msg.append((messageProtocolEntity.getFrom(),messageProtocolEntity.getBody()))

        #send receipt otherwise we keep receiving the same message over and over
        receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom())
        self.toLower(receipt)

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", "delivery")
        self.toLower(ack)

    # List of (jid, message) tuples
    PROP_MESSAGES = "org.openwhatsapp.yowsup.prop.sendclient.queue"

    @ProtocolEntityCallback("success")
    def onSuccess(self, successProtocolEntity):
        self.lock.acquire()
        for target in self.getProp(self.__class__.PROP_MESSAGES, []):
            phone, message = target
            if '@' in phone:
                messageEntity = TextMessageProtocolEntity(message, to = phone)
            elif '-' in phone:
                messageEntity = TextMessageProtocolEntity(message, to = "%s@g.us" % phone)
            else:
                messageEntity = TextMessageProtocolEntity(message, to = "%s@s.whatsapp.net" % phone)
            self.ackQueue.append(messageEntity.getId())
            self.toLower(messageEntity)
        self.lock.release()

    @ProtocolEntityCallback("ack")
    def onAck(self, entity):
        self.lock.acquire()

        if entity.getId() in self.ackQueue:
            self.ackQueue.pop(self.ackQueue.index(entity.getId()))

        if not len(self.ackQueue):
            self.lock.release()
            logger.info("Message sent")
            raise KeyboardInterrupt()

        self.lock.release()