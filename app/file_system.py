import os
import json

class Node:
    def __init__(self, name, is_directory=False):
        self.name = name
        self.is_directory = is_directory
        self.children = []
        self.parent = None
        self.previous_node = None
        

    def add_child(self, node):
        self.children.append(node)
        node.parent = self

class FileSystem:
    def __init__(self):
        self.root = Node("/", is_directory=True)
        self.current_node = self.root
        self.dicio = {"folder": [], "file": []}
        self.count = 0

    def cd(self, directory_path):
        if directory_path == "..":
            if self.current_node != self.root:
                self.previous_node = self.current_node
                self.current_node = self.current_node.parent
        elif directory_path == "-":
            if self.previous_node:
                self.current_node, self.previous_node = self.previous_node, self.current_node
            else:
                print("Não há diretório anterior.")
        else:
            if directory_path.startswith("/"):
                current_node = self.root
                directory_names = directory_path.split("/")
                for directory_name in directory_names:
                    if directory_name:
                        if directory_name == "..":
                            if current_node != self.root:
                                current_node = current_node.parent
                        else:
                            new_directory = self.find_child_directory(current_node, directory_name)
                            if new_directory:
                                current_node = new_directory
                            else:
                                print(f"Diretório '{directory_name}' não encontrado.")
                                return
                self.previous_node = self.current_node
                self.current_node = current_node
            else:
                target_directory = self.find_child_directory(self.current_node, directory_path)
                if target_directory:
                    self.previous_node = self.current_node
                    self.current_node = target_directory
                else:
                    print(f"Diretório '{directory_path}' não encontrado.")

    def ls(self):
        # dicio = {"folder": [], "file": []}
        if self.current_node is not None:
            for child in self.current_node.children:
                if child.is_directory:
                    # dicio['folder'].append(child.name)
                    print("📁", child.name)
                else:
                    # dicio['file'].append(child.name)
                    print("📄", child.name)
        else:
            print("Diretório não encontrado ou não especificado.")
        # return dicio

    # def mkdir(self, directory_name):
    #     new_directory = Node(directory_name, is_directory=True)
    #     self.current_node.add_child(new_directory)
    def mkdir(self, directory_name):
        new_directory = Node(directory_name, is_directory=True)
        self.current_node.add_child(new_directory)
        self.save_to_json() 
        print(f"Diretório '{directory_name}' criado com sucesso.")

    # def touch(self, file_name):
    #     new_file = Node(file_name)
    #     self.current_node.add_child(new_file)
    def touch(self, file_name):
        new_file = Node(file_name)
        self.current_node.add_child(new_file)
        self.save_to_json() 
        print(f"Arquivo '{file_name}' criado com sucesso.")

    def get_parent_directory(self, node):
        
        parent_path = os.path.abspath(os.path.join(node.name, os.pardir))
        return self.find_child_directory(self.root, os.path.basename(parent_path))

    def find_child_directory(self, current_node, directory_name):
        if current_node.is_directory and current_node.name == directory_name:
            return current_node
        for child in current_node.children:
            if child.is_directory:
                result = self.find_child_directory(child, directory_name)
                if result:
                    return result
        return None
    
    def rm(self, target_name):
        target_node = self.find_child_node(self.current_node, target_name)
        if target_node:
            if target_node.is_directory:
                confirm = input(f"Deseja realmente excluir o diretório '{target_name}' e todos os seus arquivos? (S/N): ")
                if confirm.lower() == 's':
                    self.current_node.children.remove(target_node)
                    print(f"Diretório '{target_name}' e todos os seus arquivos foram removidos.")
                else:
                    print("Operação cancelada.")
            else:
                self.current_node.children.remove(target_node)
                print(f"Arquivo '{target_name}' foi removido.")
        else:
            print("Arquivo ou diretório não encontrado.")

    def find_child_node(self, current_node, target_name):
        if current_node.name == target_name:
            return current_node
        for child in current_node.children:
            if child.is_directory:
                result = self.find_child_node(child, target_name)
                if result:
                    return result
            elif child.name == target_name:
                return child
        return None
    
    def tree(self, node=None, indent="", path=""):
        
        if node is None:
            node = self.current_node
            path = node.name
        
        for child in node.children:
            if child.is_directory:
                print(indent + "|-" + child.name + "📁")
                # self.dicio['folder'].append({"folder_name": child.name + "📁", 'count': self.count})
                # self.count += 1
                self.tree(child, indent + "   ", os.path.join(path, child.name))
            else:
                print(indent + "|-" + child.name + '📄')
                # self.dicio['file'].append({"file_name": child.name + '📄', 'count': self.count})
                # self.count += 1
        # print(self.dicio)
        return self.dicio
   
    def serialize_node(self, node):
        serialized_node = {
            "name": node.name,
            "is_directory": node.is_directory,
            "children": []
        }
        for child in node.children:
            serialized_node["children"].append(self.serialize_node(child))
        return serialized_node

    def deserialize_node(self, data):
        node = Node(data["name"], is_directory=data["is_directory"])
        for child_data in data["children"]:
            child_node = self.deserialize_node(child_data)
            node.add_child(child_node)
        return node
    
    def save_to_json(self):
        data = {
            "root": self.serialize_node(self.root),
            "current_path": self.get_current_path()
        }
        with open("filesystem_data.json", "w") as f:
            json.dump(data, f, indent=4)
        print("Dados salvos com sucesso.")

    def load_from_json(self, path_to_file: str = "filesystem_data.json") -> None:
        try:
            with open(path_to_file, "r") as f:
                data = json.load(f)
                self.root = self.deserialize_node(data["root"])
                self.cd('/')
                print("Dados carregados com sucesso.")
        except FileNotFoundError:
            print("Arquivo JSON não encontrado.")
        except KeyError:
            print("Erro ao carregar dados do arquivo JSON.")

    def get_current_path(self):
        path = []
        current_node = self.current_node
        while current_node:
            path.insert(0, current_node.name)
            current_node = current_node.parent
        return "/" + "/".join(path)
    
    def clear_terminal(self):
        if os.name == 'posix': 
            os.system('clear')
        elif os.name == 'nt': 
            os.system('cls')
        else:
            print("Comando de limpeza de terminal não suportado para este sistema operacional.")

    def main(self):
        try:
            self.load_from_json()
            while True:
                current_path = self.current_node.name
                if current_path != "/":
                    current_path = current_path[1:]
                current_path = current_path.replace("/", os.path.sep) + "$ "

                command = input(current_path)

                if command.startswith("cd"):
                    directory_path = command.split(" ", 1)[1]
                    self.cd(directory_path)
                elif command == "ls":
                    self.ls()
                elif command.startswith("mkdir"):
                    directory_name = command.split(" ", 1)[1]
                    self.mkdir(directory_name)
                elif command.startswith("touch"):
                    file_name = command.split(" ", 1)[1]
                    self.touch(file_name)
                elif command.startswith("rm"):
                    target = command.split(" ", 1)[1]
                    if target.startswith("-r"):
                        target_name = target.split(" ", 1)[1]
                        self.rm(target_name)
                    else:
                        self.rm(target)
                elif command == "tree":
                    self.tree()
                elif command == "clear" or command == 'cls':
                    self.clear_terminal()
                elif command == "exit":
                    self.save_to_json()
                    print("Saindo do sistema de arquivos. Adeus!")
                    break
                else:
                    print("Comando inválido. Tente novamente.")
        except KeyboardInterrupt:
            self.save_to_json()
            print("\nSaindo do sistema de arquivos devido ao KeyboardInterrupt.")

if __name__ == "__main__":
    filesystem = FileSystem()
    filesystem.main()