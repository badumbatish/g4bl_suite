import json

def parse_from_json(json_str):
    try:
        obj = json.loads(json_str)
        return Command(obj["exec"], obj["args"])
    except json.JSONDecodeError:
        print("Error decoding json")
        return None

class Command:
    def __init__(self, exec, args):
        self.exec = exec
        self.args = args
    
    def __str__(self):
        return json.dumps(self.__dict__)
    
    def execute(self):
        print("Executing command: " + self.exec)
        print("With args: " + str(self.args))
        return "Command executed successfully"