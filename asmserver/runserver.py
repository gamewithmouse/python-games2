import os
import socket

computer_beat = 16


# Recive And Sending Protocol Buffers : 8 bit and It's byte number
rem = dict()
for i in range(1, 4096):
    saveremvar1 = "{0:x}".format(i)
    saveremvar2 = 3 - len(saveremvar1)
    saveremvar3 = ""
    for x in range(saveremvar2):
        saveremvar3 += str(x)
    rem["0x"+saveremvar3 + saveremvar1] = [0] * computer_beat



def add_command(arg1, arg2, arg3):
    global rem
    print(arg1, "arg1", "arg2", arg2)
    saves = str(bin(int(arg1) + int(arg2)))
    
    rem[arg3] = list(saves.strip("0b"))

def msg_command(arg1, args):
    
    
    print("msg", arg1)

def str_command(arg1, arg2):
    global rem
    
    
    var1 = computer_beat - len(list(arg2))
    var2 = ["0"] * var1
    print(var2, "var2")
    
    if var2:
        arg2 = var2.append(str(arg2))
    else:
        rem[arg1] = arg2
        
    
    


def change_into_address(addr):
    addr = list(addr)
    for i in range(len(addr)):
        addr[i] = str(addr[i])
    var1 = ''.join(addr)
    return "0x" + var1

def real_run(filepath):
    global rem

    file = open(filepath, 'r')
    lines = file.readlines()
    

    for line in lines:
        commands = line.split(' ')
        command = commands[0]
        for x in range(len(commands)):
            commands[x] = commands[x].strip("\n")
        print(commands)
        if line.find("***") != -1:
            continue
        if command == "str":
            str_command(commands[1], commands[2])
            
        if command == "add":
            var = []
            print(rem[commands[3]])
            for bit in rem[commands[3]]:
                var.append(str(bit))

            var1 = ''.join(var)

            var2 = int(var1, 2)
            add_command(commands[2], var2, commands[1])
        if command == "msg":
            
            if commands[1] == "var":
                print(rem[commands[2].strip("\n")], "SDFSDF")
                msg_command(rem[commands[2].strip("\n")], "***")
            else:

                if len(commands) == 3:
                    msg_command(commands[2], commands[3].split(","))
            
            



def main():
    isbaddinput = True
    Dir = "./"
    selecteddir = ""
    while isbaddinput:
        dir_list = os.listdir(Dir) 
        folders = show_folders(dir_list)
        numinput = int(input("Enter Number >>"))
        selectedfilename = dir_list[numinput - 1]
        if selectedfilename in folders:
            Dir = Dir + selectedfilename + "/"
            continue
        selecteddir = Dir + selectedfilename
        isbaddinput = False
    print(selecteddir)
    real_run(selecteddir)

            

    


def show_folders(dir_list):
    print("========= SELECT FILES =========")
    folders = []
    for i, dir_name in enumerate(dir_list):
        isfolder = False
        
        if dir_name.find(".") == -1:
            isfolder = True
        if isfolder:

            print(str(i+1) + ". " + "/" + dir_name)
            folders.append(dir_name)
        else:
            print(str(i+1) + ". " + dir_name)
    return folders




if __name__ == "__main__":
    main()