
import jsonlines








a = r"D:\ZX_file\first_study\parameter_filling\dataset\SoAy\prompts_toolkit\prompt_json\prompt_dict_1101.json"

prompt_lib = []
with jsonlines.open(a, 'r') as f:
    for each in f:
        prompt_lib.append(each)
    f.close()
prompt_lib = prompt_lib[0]

print(prompt_lib.keys())

print(len(prompt_lib))

for i in prompt_lib:
    print(i)
    print('**********')
    print(prompt_lib[i])
    print('----------------')
    print('----------------')
    print('----------------')
    print('----------------')






