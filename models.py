models = {
        1 : {'name' : 'Mistral Nemo Q4_K_M GGUF', 'path' : '/models/Mistral-Nemo-Instruct-2407-Q4_K_M.gguf'},
        2 : {'name' : 'Mistral 7B Instruct v03 Q2_K GGUF', 'path' : '/models/mistral-7b-instruct-v0.3.Q2_K.gguf'},
        3 : {'name':'Mistral 7B code 16k qlora Q8_0', 'path' :'/models/mistral-7b-code-16k-qlora.Q8_0/mistral-7b-code-16k-qlora.Q8_0.gguf'},
        4 : {'name':'Mistral 7B inst v02 Q6_K', 'path' :'/models/mistral-7b-instruct-v0.2.Q6_K/mistral-7b-instruct-v0.2.Q6_K.gguf'},
        5 : {'name':'Mistral 7B inst v03 Q8_0', 'path' :'/models/Mistral-7B-Instruct-v0.3.Q8_0/Mistral-7B-Instruct-v0.3.Q8_0.gguf'},
        6 : {'name':'Mistral 7B inst v03', 'path' :'/models/Mistral-7B-Instruct-v0.3/Mistral-7B-Instruct-v0.3.gguf'},
        7 : {'name':'Mistral 7B Instruct v0.3 f16 Q4_1', 'path' :'/models/Mistral-7B-Instruct-v0.3-f16/Q4_1/Q4_1-00001-of-00001.gguf'},
        8 : {'name':'Mistral 7B Instruct v0.3 f16', 'path' :'/models/Mistral-7B-Instruct-v0.3-f16/Mistral-7B-Instruct-v0.3-f16.gguf'},
        9 : {'name':'Mistral Small 24B inst BF16', 'path' :'/models/Mistral-Small-24B-Instruct-2501.BF16/Mistral-Small-24B-Instruct-2501.BF16.gguf'},
        10 : {'name':'Mistral Small 24B Inst Q8_0', 'path' :'/models/Mistral-Small-24B-Instruct-2501.Q8_0/Mistral-Small-24B-Instruct-2501.Q8_0.gguf'},
        11 : {'name':'Mistral Small 24B Inst Q4_K_M', 'path' :'/models/Mistral-Small-24B-Instruct-2501-Q4_K_M/Mistral-Small-24B-Instruct-2501-Q4_K_M.gguf'},
        12 : {'name':'mixtral 8x7b inst v01 Q8_0', 'path' :'/models/mixtral-8x7b-instruct-v0.1.Q8_0/mixtral-8x7b-instruct-v0.1.Q8_0.gguf'},
        13 : {'name':'mixtral 8x7b v01 Q4_K_M', 'path' :'/models/mixtral-8x7b-v0.1.Q4_K_M/mixtral-8x7b-v0.1.Q4_K_M.gguf'},
        14 : {'name':'Gemini 1.5 pro Q4_K_M', 'path' :'/models/gemini-1.5-pro.Q4_K_M.gguf'},
        15 : {'name':'Gemini 1.5 pro Q2_K', 'path' :'/models/gemini-1.5-pro.Q2_K.gguf'},
        16 : {'name':'Phi 2 Q4_K_M', 'path' :'/models/phi-2.Q4_K_M.gguf'},
        17 : {'name':'Tiny Llama 1.1B Chat', 'path' :'/models/tinyllama-1.1b-chat-v1.0.Q5_K_M.gguf'}
        }

def select_model(model_index:int=0):
    if model_index > 0:
        return models.get(model_index).get('path')
    
    for index, model_details in models.items():
        print(f"{index} : \t{model_details['name']}")
    
    while(True):
        selected_model_index = eval(input("Enter the index of model you want to use: "))
        if selected_model_index in models.keys():
            selected_model = models.get(selected_model_index).get('path')
            return selected_model
        else:
            print("**You need to select from available models")



