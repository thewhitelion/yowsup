from yowsup.layers import YowLayer, YowLayerEvent, YowProtocolLayer
from .protocolentities import ImageDownloadableMediaMessageProtocolEntity
from .protocolentities import LocationMediaMessageProtocolEntity
from .protocolentities import RequestUploadIqProtocolEntity, ResultRequestUploadIqProtocolEntity
from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity, ErrorIqProtocolEntity

from .protocolentities import VCardMediaMessageProtocolEntity
class YowMediaProtocolLayer(YowProtocolLayer):

    # EVENT_REQUEST_UPLOAD = "org.openwhatsapp.org.yowsup.event.protocol_media.request_upload"

    def __init__(self):
        handleMap = {
            "message": (self.recvMessageStanza, self.sendMessageEntity),
            "iq": (self.recvIq, self.sendIq)
        }
        
        super(YowMediaProtocolLayer, self).__init__(handleMap)

    def __str__(self):
        return "Media Layer"

    # def onEvent(self, yowLayerEvent):
    #     if yowLayerEvent.getArg(self.__class__.EVENT_REQUEST_UPLOAD):
    #         fpath = yowLayerEvent.getArg("file")
    #         _type = yowLayerEvent.getArg("type")
    #         assert fpath and _type, "Must specify 'file' and 'type' in EVENT_REQUEST_UPLOAD args"
    #         entity = RequestUploadIqProtocolEntity(_type, filePath=fpath)
    #         self._sendIq(entity, self.onRequestUploadSuccess, self.onRequestUploadError)


    def sendMessageEntity(self, entity):
        if entity.getType() == "media":
            self.entityToLower(entity)

    ###recieved node handlers handlers
    def recvMessageStanza(self, node):
        if node.getAttributeValue("type") == "media":
            mediaNode = node.getChild("media")
            if mediaNode.getAttributeValue("type") == "image":
                entity = ImageDownloadableMediaMessageProtocolEntity.fromProtocolTreeNode(node)
                self.toUpper(entity)    
            elif mediaNode.getAttributeValue("type") == "location":
                entity = LocationMediaMessageProtocolEntity.fromProtocolTreeNode(node)
                self.toUpper(entity)
            elif mediaNode.getAttributeValue("type") == "vcard":
                entity = VCardMediaMessageProtocolEntity.fromProtocolTreeNode(node)
                self.toUpper(entity)

    def sendIq(self, entity):
        """
        :type entity: IqProtocolEntity
        """
        if entity.__class__ == RequestUploadIqProtocolEntity:
            #media upload!
            self._sendIq(entity, self.onRequestUploadSuccess, self.onRequestUploadError)

    def recvIq(self, node):
        """
        :type node: ProtocolTreeNode
        """

    def onRequestUploadSuccess(self, resultNode, requestUploadEntity):
        self.toUpper(ResultRequestUploadIqProtocolEntity.fromProtocolTreeNode(resultNode))

    def onRequestUploadError(self, errorNode, requestUploadEntity):
        self.toUpper(ErrorIqProtocolEntity.fromProtocolTreeNode(errorNode))