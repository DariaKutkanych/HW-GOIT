import redis
from collections import deque

client = redis.StrictRedis(host="localhost", port=6379, password=None)


class Cache_decorator:

    def __init__(self, client, max_size):

        self.client = client
        self.item_queue = deque()
        self.max_size = max_size

    def __call__(self, func):

        def wrapper(*args):
            
            key_args = str(args)

            if key_args in self.item_queue:
                item_key = self.item_queue.remove(key_args)
                self.item_queue.append(item_key)
                print ("You got the data from cache: ")
                print(self.client.get(key_args).decode())
                return self.client.get(key_args)

            elif len(self.item_queue) >= self.max_size:
                quit_item = self.item_queue.popleft()
                self.client.delete(quit_item)
                
            self.item_queue.append(key_args)
            value = func(*args)
            client.set(key_args, value)
            
            print("Data processed...")
            print(value)
            return value
        return wrapper

@Cache_decorator(client=client, max_size=5)
def main_func(*args):
    return args[0]


if __name__=="__main__":

    words = "Welcome of to our huge fairy tales library Sleeping Beauty Rumpelstiltskin\
         Little Red Riding Hood and stories of Cinderella Cinderella of"

    for word in words.split():
        main_func(word)


    for k in client.keys():
        print(client.get(k).decode())
