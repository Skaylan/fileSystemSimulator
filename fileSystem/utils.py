import os

def man(command):
    if command == "cd":
        print("cd <caminho>: Navega para o diretório especificado.")
        print("   <caminho>: Caminho absoluto ou relativo para o diretório desejado.")
    elif command == "ls":
        print("ls: Lista os arquivos e diretórios no diretório atual.")
    elif command == "mkdir":
        print("mkdir <nome>: Cria um novo diretório com o nome especificado.")
        print("   <nome>: Nome do diretório a ser criado.")
    elif command == "touch":
        print("touch <nome>: Cria um novo arquivo com o nome especificado.")
        print("   <nome>: Nome do arquivo a ser criado.")
    elif command == "rm":
        print("rm <nome>: Remove o arquivo ou diretório especificado.")
        print("   <nome>: Nome do arquivo ou diretório a ser removido.")
        print("rm -r <nome>: Remove recursivamente o diretório e seu conteúdo.")
        print("   <nome>: Nome do diretório a ser removido recursivamente.")
    elif command == "tree":
        print("tree: Exibe a estrutura de diretórios em formato de árvore.")
    elif command == "nano":
        print("nano <nome>: Abre o editor de texto para editar o arquivo especificado.")
        print("   <nome>: Nome do arquivo a ser editado.")
        print("   Digite 'save' para salvar e sair do editor.")
    elif command == "cat":
        print("cat <nome>: Exibe o conteúdo do arquivo especificado.")
        print("   <nome>: Nome do arquivo a ser exibido.")
    elif command == "move":
        print("move <origem> <destino>: Move o arquivo ou diretório da origem para o destino.")
        print("   <origem>: Caminho do arquivo ou diretório a ser movido.")
        print("   <destino>: Caminho do diretório de destino.")
        print("   Use '.' para mover para o diretório atual.")
    elif command == "help":
        print("help: Exibe uma lista de comandos disponíveis.")
    elif command == "exit":
        print("exit: Sai do sistema de arquivos.")
    else:
        print("Comando não reconhecido. Use 'help' para obter uma lista de comandos disponíveis.")


def help():
    print("Lista de Comandos:")
    print("cd <caminho>: Navega para o diretório especificado.")
    print("ls: Lista os arquivos e diretórios no diretório atual.")
    print("mkdir <nome>: Cria um novo diretório com o nome especificado.")
    print("touch <nome>: Cria um novo arquivo com o nome especificado.")
    print("rm <nome>: Remove o arquivo ou diretório especificado.")
    print("rm -r <nome>: Remove recursivamente o diretório e seu conteúdo.")
    print("tree: Exibe a estrutura de diretórios em formato de árvore.")
    print("nano <nome>: Abre o editor de texto para editar o arquivo especificado.")
    print("cat <nome>: Exibe o conteúdo do arquivo especificado.")
    print("move <origem> <destino>: Move o arquivo ou diretório da origem para o destino.")
    print("help: Exibe esta mensagem de ajuda.")
    print("exit: Sai do sistema de arquivos.")
    print("Para obter mais ajuda, execute 'man <comando>'.")
    
def menu(file_system):
    try:
        file_system.load_from_json()
        while True:
            current_path = file_system.get_current_path()
            if current_path != "/":
                current_path = current_path[1:]
            current_path = current_path.replace("/", os.path.sep)
            
            prompt = f"\033[32m{file_system.username}@{file_system.username}\033[m:\033[34m{current_path}\033[m$ "

            command = input(prompt)

            if command.startswith("cd"):
                directory_path = command.split(" ", 1)[1]
                file_system.cd(directory_path)
            elif command == "ls":
                file_system.ls()
            elif command.startswith("mkdir"):
                directory_name = command.split(" ", 1)[1]
                file_system.mkdir(directory_name)
            elif command.startswith("touch"):
                file_name = command.split(" ", 1)[1]
                file_system.touch(file_name)
            elif command.startswith("rm"):
                target = command.split(" ", 1)[1]
                if target.startswith("-r"):
                    target_name = target.split(" ", 1)[1]
                    file_system.rm(target_name)
                else:
                    file_system.rm(target)
            elif command == "tree":
                file_system.tree()
            elif command == "pwd":
                file_system.pwd()
            elif command == "clear" or command == 'cls':
                file_system.clear_terminal()
            elif command.startswith("nano"):
                file_name = command.split(" ", 1)[1]
                file_system.nano(file_name)
            elif command.startswith("cat"):
                file_name = command.split(" ", 1)[1]
                file_system.cat(file_name)
            elif command.startswith("move"):
                source_name, destination_name = command.split(" ", 1)[1].split(" ", 1)
                file_system.move(source_name, destination_name)
            elif command.startswith("man"):
                command_name = command.split(" ", 1)[1]
                man(command_name)
            elif command == "help":
                help()
            elif command == "exit":
                file_system.save_to_json()
                print("Saindo do sistema de arquivos. Adeus!")
                break
            else:
                print("Comando inválido. Tente novamente.")
    except KeyboardInterrupt:
        file_system.save_to_json()
        print("\nSaindo do sistema de arquivos devido ao KeyboardInterrupt.")