from components.ast.statement import Expression
# from ast.statement import Expression

def singleton(cls):
    instances = {}
    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return getinstance

@singleton
class Memory:

    def __init__(self) -> None:
        self.memory:dict = dict({})
    
    def set(self, variable_name:str, value, data_type: type):
        # Store only the value, not the Expression object
        if isinstance(value, Expression):
            stored_value = value.number  # Storing the numerical value only
        else:
            stored_value = value

        self.memory[variable_name] = {"value": stored_value, "data_type": data_type}

    def get(self, variable_name: str):
        data = self.memory[variable_name]
        return data['value']  # Return the actual value


    def __repr__(self) -> str:
        string = ""
        string += f"Name\tValue\tData Type\n"
        string += "-"*30+"\n"
        for var, data in self.memory.items():
            value = data["value"]
            data_type = data["data_type"]
            string += f"\t{var}\t{value}\t{data_type}\n"
        string += "-"*30+"\n"
        return string

if __name__ == "__main__":
    memory = Memory()
    memory.set(variable_name='a', value=10, data_type=int)
    memory.set(variable_name='b', value="20", data_type=str)
    print(memory)
    print(memory.get(variable_name='b'))