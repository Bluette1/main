import json, pika
from main import Product, db, app

params = pika.URLParameters('amqps://airxfsao:W5tmIncTdIhXialDQB-ExXj-jMEBc1Iu@armadillo.rmq.cloudamqp.com/airxfsao')

connection = pika.BlockingConnection(params)

channel = connection.channel()
channel.queue_declare(queue='main')

def callback(ch, method, properties, body):
  print('Received in main')
  data = json.loads(body)
  print(data)

  with app.app_context():
    if properties.content_type == 'product_created':
      product = Product(id=data['id'], title=data['title'], image=data['image'])
      db.session.add(product)
      db.session.commit()
      print('Product Created')

    if properties.content_type == 'product_updated':
      product = Product.query.get(data['id'])
      product.title = data['title']
      product.image = data['image']
      db.session.commit()
      print('Product Updated')


    if properties.content_type == 'product_deleted':
      product = Product.query.get(data)  
      db.session.delete(product)  
      db.session.commit()
      print('Product Deleted')

channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()