import rabbitclasses
import uuid
import json
import gzip

def gen_id():
    id_bytes = uuid.uuid4().bytes
    return int.from_bytes(id_bytes, byteorder='big', signed=False)

def queue_item_from_json(json_str, gzip_compressed=True):
    if gzip_compressed:
        json_str = gzip.decompress(json_str).decode("utf-8")
    obj = json.loads(json_str)
    return QueueItem(obj["data_chunk"])

class QueueItemChunk:
    def __init__(self, data_chunk, chunk_index, chunk_size, total_chunks, gzip_compressed=True):
      self.id = gen_id()
      self.data_chunk = data_chunk
      self.chunk_index = chunk_index
      self.chunk_size = chunk_size
      self.total_chunks = total_chunks
      self.gzip_compressed = gzip_compressed
    
    def __str__(self):
        obj = {
            "id": self.id,
            "data_chunk": self.data_chunk,
            "chunk_index": self.chunk_index,
            "chunk_size": self.chunk_size,
            "total_chunks": self.total_chunks
        }

        return str(obj)

    def compressed(self):
        if not self.gzip_compressed:
            raise ValueError("This chunk is not gzip compressed")
        return gzip.compress(self.__str__().encode("utf-8"))
    
    def __repr__(self):
        return self.__str__()

class QueueItem:
    def __init__(self, data, gzip_compressed=True):
      self.id = gen_id()
      self.data = data
      self.gzip_compressed = gzip_compressed

    def chunk_arr(self, chunk_size=102400):
        res = []
        total_length = len(str(self.data))
        total_chunks = (total_length // chunk_size) + 1
        for i in range(total_chunks):
            start = i * chunk_size
            end = start + chunk_size
            if end > total_length:
                end = total_length
            res.append(QueueItemChunk(self.data[start:end], i, chunk_size, total_chunks))
    
        return res
    
    def __str__(self):
        obj = {
            "id": self.id,
            "data_chunk": self.data,
            "is_chunked": False
        }

        return str(obj)

    def compressed(self):
        if not self.gzip_compressed:
            raise ValueError("This chunk is not gzip compressed")
        return gzip.compress(self.__str__().encode("utf-8"))

class DataQueuer:
    def __init__(self, rabbitmq_publisher):
        if not isinstance(rabbitmq_publisher, rabbitclasses.RabbitMQPublisher):
            raise TypeError("rabbitmq_publisher must be of type RabbitMQPublisher")
        self.rabbitmq_publisher = rabbitmq_publisher
    
    def queue_item(self, queue_item):
        if not isinstance(queue_item, QueueItem):
            raise TypeError("queue_item must be of type QueueItem")
        if queue_item.gzip_compressed:
          self.rabbitmq_publisher.publish(queue_item.compressed())
        else:
          self.rabbitmq_publisher.publish(queue_item.__str__())

    