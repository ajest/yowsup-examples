# coding: utf-8
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
import random


class ReplyEchoLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):

        # Just for fun
        items = [
            'Gracias por participar!'
            , 'Perdón :( No hemos entendido del todo tu solicitud'
            , 'Estamos para ayudarte! Contanos más!'
            , 'Hola! Se te ofrece?'
            , 'Gracias por comunicarte nuevamente! Esperamos que hayas disfrutado de tu experiencia'
            , 'Si, aquí estoy. Contame qué estás buscando...'
            , 'Ups, creo que no entendí bien. Dame más info por favor!'
        ]

        if messageProtocolEntity.getType() == 'text':
            self.onTextMessage(messageProtocolEntity)
            self.sendMessage(messageProtocolEntity, random.choice(items))

        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())

    def onTextMessage(self, messageProtocolEntity):
        # just print info
        print("Llegó el mensaje %s" % (messageProtocolEntity.getBody()))

    def sendMessage(self, messageProtocolEntity, message):
        outgoingMessageProtocolEntity = TextMessageProtocolEntity(
            message,
            to=messageProtocolEntity.getFrom()
        )

        self.toLower(outgoingMessageProtocolEntity)