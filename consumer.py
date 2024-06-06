import pika
from pymongo import MongoClient
from mongoengine import connect
from mongoengine import Document, StringField, BooleanField

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

def callback(ch, method, properties, body):
    # Deserialize the contact from the message body
    contact_id = body.decode('utf-8')

    # Fetch the contact from MongoDB
    contact = Contact.objects.get(id=contact_id)

    # Simulate sending the email
    print(f"Sending email to {contact['name']} ({contact['email']})")
    contact.sent = True
    contact.save()

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Start consuming messages
channel.basic_consume(queue='email_queue', on_message_callback=callback)

print('Waiting for messages...')
channel.start_consuming()