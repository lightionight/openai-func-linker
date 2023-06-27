from openai_agent.completions import get_function_completion
from openai_agent.functions import Function
from openai_agent.messages import UserMessage
import yaml
import subprocess
import sys
from function_CRUD import EmbeddingMemory
from convert_data import convertTextToVector
import requests
GLOBAL = {}

def evalEnv(deps):
     # get functions deps
    for item in deps:
        if item in sys.modules:
            pass
        else:
            subprocess.call(["pipenv", "install", item])

def function_load(function_data):
    # env
    evalEnv(function_data['deps'])
    # load code and execute it
    exec(function_data['context'], GLOBAL)

def function_exec(function_data, user_input):
    result = eval(function_data['name'] +  "('" + user_input + "')")
    print(result)

def check_needs_functions(user_input):
    function_lib =  EmbeddingMemory()
    user_input_vector = convertTextToVector(user_input)
    response = function_lib.query(user_input_vector, 'test')
    if response:
        return response
    else:
        return None

def get_function_source(
        function_meta
):
    func_list = []
    if function_meta:
        print('debug | ', function_meta)
        for func in function_meta:
            func_data = requests.get(func['url']).text
            print(func_data)
            data = yaml.load(func_data, Loader=yaml.FullLoader)
            function_load(data)
            func_list.append(Function.load_from_func(GLOBAL[func['name']]))
        print(func_list)
    return func_list
    


if __name__ == "__main__":
    user_input = input("Please input what you want search: ")
    needs_function = check_needs_functions(user_input)
    response = get_function_completion(
        messages=[UserMessage(content=user_input)],
        functions=get_function_source(needs_function),
    )
    print(response.content)