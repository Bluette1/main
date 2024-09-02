import pika, json

params = pika.URLParameters('amqps://airxfsao:W5tmIncTdIhXialDQB-ExXj-jMEBc1Iu@armadillo.rmq.cloudamqp.com/airxfsao')

connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)

