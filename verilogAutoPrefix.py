import os
import re
import argparse


def collect_verilog_files(directory):
    collections = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.v') or file.endswith('.sv'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                collections.append([file_path, content])
    return collections

def main(directory, prefix, ignoremodule):
    print(f"Processing {directory}, adding prefix {prefix}...")
    collections = collect_verilog_files(directory)
    module_names = []
    for i in range(len(collections)):
        cur_module_names = re.findall(r'\bmodule\s+(\w+)', collections[i][1])
        assert(len(cur_module_names)<=1, f"Found more than one module name in {collections[i][0]}")
        if len(cur_module_names)==0:
            continue
        module_name = cur_module_names[0]
        module_names.append(module_name)
        collections[i][0] = collections[i][0].replace(module_name, prefix + module_name)

    print(f"Found module names: {module_names}")
    for module_name in module_names:
        if module_name in ignoremodule:
            continue
        for i in range(len(collections)):
            # 更新模块声明
            collections[i][1] = re.sub(r'\bmodule\s+' + module_name + r'(\s|\()', f'module {prefix}{module_name}\\1', collections[i][1])
            # 更新实例
            collections[i][1] = re.sub(r'\b' + module_name + r'\s+(\w+)\s*\(', f'{prefix}{module_name} \\1(', collections[i][1])
    
    for file_path, content in collections:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

    
    print("Done.")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add prefix to Verilog module names and update instances.')
    parser.add_argument('directory', type=str, help='Directory containing Verilog and SystemVerilog files')
    parser.add_argument('prefix', type=str, help='Prefix to add to module names')
    parser.add_argument('ignoremodule', type=str, help='Ignore module names')
    args = parser.parse_args()

    main(args.directory, args.prefix, args.ignoremodule)
