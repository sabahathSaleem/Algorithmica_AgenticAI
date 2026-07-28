import redis
import json

# Setting decode_responses=True automatically decodes the responses from bytes to strings.
try:
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

    # string as value
    key_string = "user:name"
    value_string = "John"
    r.set(key_string, value_string)
    retrieved_string = r.get(key_string)
    print(f"Retrieved: '{key_string}': '{retrieved_string}'")


    # dictionary as json string
    key_dict = "user-102:profile"
    value_dict = {
        "name": "Bob Johnson",
        "age": 30,
        "tags": ["redis", "python", "nosql"]
    }
    stored_json = json.dumps(value_dict)
    r.set(key_dict, stored_json)
    retrieved_json = r.get(key_dict)
    print(f"Retrieved Raw: '{retrieved_json}'")
    retrieved_dict = json.loads(retrieved_json)
    print(f"Retrieved Dict: {retrieved_dict}")

except redis.exceptions.ConnectionError as e:
    print(f"Error connecting to Redis: {e}")
   