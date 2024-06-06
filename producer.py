import pika
from mongoengine import connect
from mongoengine import Document, StringField, BooleanField
from faker import Faker
import random
import time

# Establish MongoDB connection
connect('mongodb://localhost:27017/')

# Define Contact model
class Contact(Document):
    name = StringField()
    email = StringField()
    sent = BooleanField(default=False)

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'sent': self.sent
        }

# Establish RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue='email_queue')

# Generate fake contacts
fake = Faker()
contacts = []
for _ in range(10):
    contact = Contact(
        name=fake.name(),
        email=fake.email(),
    )
    contact.save()
    contacts.append(contact)

# Send messages to the queue
for contact in contacts:
    contact_id = str(contact.id)
    channel.basic_publish(exchange='', routing_key='email_queue', body=contact_id)

# Close the RabbitMQ connection
connection.close()