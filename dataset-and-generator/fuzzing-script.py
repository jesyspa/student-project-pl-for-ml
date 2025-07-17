import os, random

ops=['+','-','*','/']
var_names=['x','y','a','b','val','num']
nums = range(1, 100)
conds = ['<','>']
out_dir = 'dataset-generated'
templ_dir = 'templates'

def template_filler(template_str):
    var1 = random.choice(var_names)
    var2 = random.choice([v for v in var_names if v != var1])
    return (template_str
        .replace("VAR1", random.choice(var1))
        .replace("VAR2", random.choice(var2))
        .replace("NUM1", str(random.choice(nums)))
        .replace("NUM2", str(random.choice(nums)))
        .replace("OP", random.choice(ops))
        .replace("RES", random.choice(var_names))
        .replace("COND", random.choice(conds)))

os.makedirs(out_dir, exist_ok=True)
for templ_name in os.listdir(templ_dir):
    path = os.path.join(templ_dir, templ_name)
    with open(path, "r") as f:
        template = f.read()
    for i in range(2): #number of created files (increase when necessary)
        code = template_filler(template)
        out_name = f"{templ_name.replace('.txt','')}_{i}.txt"
        with open(os.path.join(out_dir, out_name), "w") as out:
            out.write(code)