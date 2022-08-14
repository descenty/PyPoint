from djangochannelsrestframework.consumers import AsyncAPIConsumer
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import RetrieveModelMixin
from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin, action
from main_app.serializers import MessageRoomSerializer
from main_app.models import Message, MessageRoom


class MessageRoomConsumer(RetrieveModelMixin, GenericAsyncAPIConsumer):
    queryset = MessageRoom.objects.all()
    serializer_class = MessageRoomSerializer
    lookup_field = 'pk'

    async def connect(self):
        print('huyvgovne')
        await super().accept()

    async def disconnect(self, code):
        print('piska')
        await super().disconnect(code)
