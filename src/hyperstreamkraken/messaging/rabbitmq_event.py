from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import partial
from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from pika.adapters.blocking_connection import BlockingChannel
from pika.exchange_type import ExchangeType
from pika.spec import Basic, BasicProperties
from typing import Any, cast
import json

from reification import Reified


class RabbitMQEventHandler[E: RabbitMQEvent = RabbitMQEvent](ABC, Reified):
    @classmethod
    def get_event_type(cls) -> type[E]:
        return cast(type[E], cls.targ)

    def trigger(
        self, event_bus: "RabbitMQEventBus", deliver: Basic.Deliver, message: bytes
    ) -> None:
        event_class: type[E] = self.get_event_type()
        event = event_class(event_bus, deliver=deliver, message=message)
        event.hydrate()
        self.handle(event=event)

    @abstractmethod
    def handle(self, event: E) -> None: ...


class RabbitMQEventBus:
    event_handlers: dict[str, RabbitMQEventHandler["RabbitMQEvent"]]
    connection: BlockingConnection
    channel: BlockingChannel
    exchange_name: str
    queue_name: str

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        exchange_name: str,
        queue_name: str,
    ) -> None:
        connection_credentials: PlainCredentials = PlainCredentials(
            username=username, password=password
        )
        connection_parameters: ConnectionParameters = ConnectionParameters(
            host=host, port=5672, credentials=connection_credentials
        )
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.connection = BlockingConnection(parameters=connection_parameters)
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=1)
        self.channel.exchange_declare(
            exchange=exchange_name,
            exchange_type=ExchangeType.topic,
            passive=False,
            durable=True,
            auto_delete=False,
        )
        self.channel.queue_declare(queue=queue_name, auto_delete=True)
        self.event_handlers = {}

    def register_handler[E: RabbitMQEvent](
        self, event_handler: RabbitMQEventHandler[E]
    ) -> None:
        event_type: type[RabbitMQEvent] = cast(type[RabbitMQEvent], event_handler.targ)
        self.event_handlers[event_type.get_event_name()] = cast(
            RabbitMQEventHandler[RabbitMQEvent], event_handler
        )

    def start_listening(self) -> None:
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=partial(self.__consume, event_bus=self),
        )
        self.channel.start_consuming()

    def dispatch(self, event: "RabbitMQEvent") -> None:
        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=event.get_event_name(),
            body=event.serialize(),
            mandatory=False,
        )

    @staticmethod
    def __consume(
        event_bus: "RabbitMQEventBus",
        event_handlers: dict[str, RabbitMQEventHandler["RabbitMQEvent"]],
        channel: BlockingChannel,
        deliver: Basic.Deliver,
        _: BasicProperties,
        message: bytes,
    ) -> None:
        delivery_tag: int = cast(int, deliver.delivery_tag)
        routing_key: str = cast(str, deliver.routing_key)

        if routing_key not in event_handlers:
            raise ValueError(f"There is no event handler for '{routing_key}'.")

        event_handler: RabbitMQEventHandler[RabbitMQEvent] = event_handlers[routing_key]

        try:
            channel.basic_ack(delivery_tag=delivery_tag)
            event_handler.trigger(event_bus=event_bus, deliver=deliver, message=message)
        except Exception:
            ...  # TODO:  Enable logging for event handler exceptions
            channel.basic_nack(delivery_tag=delivery_tag)


@dataclass
class RabbitMQEvent(ABC):
    event_bus: RabbitMQEventBus
    deliver: Basic.Deliver
    message: bytes

    @abstractmethod
    def hydrate(self) -> None: ...

    @abstractmethod
    def serialize(self) -> bytes: ...

    @staticmethod
    @abstractmethod
    def get_event_name() -> str: ...

    def string(self) -> str:
        return self.message.decode(encoding="utf-8")

    def json(self) -> dict[str, Any]:
        return json.loads(self.string())
