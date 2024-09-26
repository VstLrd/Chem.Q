# python 3.11.9

from chemcrow.agents import ChemCrow

temp = -1

print("\033[37m")

while temp < 0 or temp > 2:
    
    try:
        temp = float(input("\tPlease enter temperature:\033[33m(0 < temp < 2)\033[37m  "))
        print("\n\033[31m")

    except:
        print("\n\t\033[31mTemp must be a float. \n\033[31m")

chem_model = ChemCrow(
    model = "C:/Users/VstLrd\Desktop/Meta-Llama-3-8B-Instruct.Q4_0.gguf" ,
    tools_model = "C:/Users/VstLrd\Desktop/Meta-Llama-3-8B-Instruct.Q4_0.gguf" ,
    temp = temp , verbose = False , max_tokens = 100 , n_ctx = 2048
)

print("\n\033[37m\tEnter your prompt. \033[35m(0 to quit)")

while True:
    prompt = input("\033[32m\n\t\t>>>\033[37m ")

    if prompt == '0':
        break

    print("\n\t\t\033[34m>>>\033[37m")

    response = chem_model.run(prompt)
