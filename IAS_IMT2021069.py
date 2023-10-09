from prettytable import PrettyTable

#initialising various comppnents of IAS
memory = []
MAR = ""
MBR = ""
IR = ""
MQ = ""
PC = ""
AC = 0
MQ = 1


#function to convert a decimal number to binary and return it as a string of length 12 (mainly used for addresses)
def DecimalToBinary(n):
    x = int(n)
    b = bin(x).replace("0b", "")
    s = str(b)
    if len(s) >= 12:
        return s
    while len(s) != 12:
        s = "0" + s
    return s


#function to convert decimal number to binary and return it as a string
def DtoB(n):
    x = int(n)
    b = bin(x).replace("0b", "")
    s = str(b)
    return s


#Execute function
#The function reads the value in IR(opcode) and accordingly executes the operation
def Execute(IR, MAR, table, PC):
   
    global AC
    global MQ
    
    #if MAR is not empty i.e a particular address is specified
    if MAR != None:
        
        #LOAD M(X)
        if IR == "00000001":
            MBR = memory[MAR][0]
            table.add_row(["MBR", MBR])
            AC = MBR
            table.add_row(["AC", AC])
        
        #ADD M(X)
        elif IR == "00000101":
            MBR = memory[MAR][0]
            table.add_row(["MBR", MBR])
            AC = DtoB(int(AC,2) + int(MBR,2)).zfill(40)
            table.add_row(["AC", AC])
        
        #SUB M(X)
        elif IR == "00000110":
            MBR = memory[MAR][0]
            table.add_row(["MBR", MBR])
            AC = DtoB(int(AC,2) - int(MBR,2)).zfill(40)
            table.add_row(["AC", AC])
        
        #STOR M(X)
        elif IR == "00100001":
            if (memory[MAR] != []):
                memory[MAR].pop(0)
            memory[MAR].append(AC)
            print(table)
            print("DATA AT MEMORY LOCATION {} -> {}\n".format(MAR, memory[MAR][0]))
            return
        
        #LOAD MQ,M(X)
        elif IR == "00001001":
            MBR = memory[MAR][0]
            table.add_row(["MBR", MBR])
            MQ = MBR
            table.add_row(["MQ", MQ])
        
        #MUL M(X)
        elif IR == "00001011":
            MBR = memory[MAR][0]
            table.add_row(["MBR", MBR])
            x = DecimalToBinary(str(int(MQ,2) * int(MBR,2)))
            MQ = DtoB(int(MQ,2) * int(MBR,2))
            while len(x) != 80:
                x = "0" + x
            AC_dup = x[0:40]
            #if first 40 bits of the result are not all zeroes then update AC
            if AC_dup != "0"*40:
                AC = AC_dup
                table.add_row(["AC", AC])
            else:
                table.add_row(["AC",AC_dup])
            MQ = x[40:]
            table.add_row(["MQ", MQ])
        
        #DIV M(X)
        elif IR == "00001100":
            MBR = memory[MAR][0]
            table.add_row(["MBR", MBR])
            AC = DtoB(int(MQ,2) % int(MBR,2)).zfill(40)
            MQ = DtoB(int(MQ,2) // int(MBR,2)).zfill(40)
            table.add_row(["MQ", MQ])
            table.add_row(["AC", AC])
        
        #JUMP +M(X,0:19) 
        elif IR == "00001111":
            PC = MAR
            print(table)
            print(" ")
            while int(AC,2) > 0:
                next_instr = []
                next_instr.append(memory[MAR-1][0])
                Decoder(next_instr,PC)
                PC = PC + 1
                MAR = MAR + 1
            return
    
    #instructions which don't require an address
    else:
        
        #LOAD MQ
        if IR == "00001010":
            AC = MQ
            table.add_row(["AC", AC])

    print(table)
    print(" ")

#Decoder function
#This function divides the instruction into lhs and rhs and according updates the values of IR, MAR, IBR etc and the calls the function Execute for execution of an instruction
def Decoder(m,PC):
    table = PrettyTable()
    table.field_names = (["COMPONENT", "VALUE"])
    table.add_row(["PC", PC])
    MAR = PC
    table.add_row(["MAR", MAR])
    MBR = m[0]
    table.add_row(["MBR", MBR])
    if len(m[0]) == 40:
        l = [m[0][0:20], m[0][20:]]
    else:
        l = [m[0][0:20]]
    while (l != []):
        lhs = l[0];
        IR = lhs[0:8]
        if (len(l) == 2):
            IBR = l[1]
            table.add_row(["IBR", IBR])
        if lhs.isdigit():
            MAR = lhs[8:20]
            x = int(MAR,2)
            table.add_row(["IR", IR])
            table.add_row(["MAR", MAR])
            Execute(IR, x, table,PC)
        else:
            MAR = None
            table.add_row(["IR", IR])
            Execute(IR, None, table, PC)
        l.pop(0)

#OPC Function
#this function returns opcode of a particular instruction
def OPC(opCode):
    
    if opCode == "LOAD M(X)":
        return "00000001"
    
    elif opCode == "ADD M(X)":
        return "00000101"
    
    elif opCode == "SUB M(X)":
        return "00000110"
    
    elif opCode == "STOR M(X)":
        return "00100001"
    
    elif opCode == "LOAD MQ,M(X)":
        return "00001001"
    
    elif opCode == "MUL M(X)":
        return "00001011"
    
    elif opCode == "DIV M(X)":
        return "00001100"
    
    elif opCode == "LOAD MQ":
        return "00001010"
    
    elif opCode == "JUMP +M(X,0:19)":
        return "00001111"


#Assembler function
#this function converts the assembly level instruction to 40 bit binary instruction and returns the instruction as a string
#if lhs instruction is not present, XXXXXXXXXXXXXXXXXXXX is appended as left instruction in the final instruction
def Assembler(instruction_elements):
    
    if len(instruction_elements) == 6:
        
        op_LHS = OPC(instruction_elements[0] + " " + instruction_elements[1])
        address1 = DecimalToBinary(instruction_elements[2])
        op_RHS = OPC(instruction_elements[3] + " " + instruction_elements[4])
        address2 = DecimalToBinary(instruction_elements[5])
        instr_code = op_LHS + address1 + op_RHS + address2
        
        return instr_code
    
    elif len(instruction_elements) == 5:
        
        if (instruction_elements[1] == "MQ"):
            op_LHS = OPC(instruction_elements[0] + " " + instruction_elements[1])
            op_RHS = OPC(instruction_elements[2] + " " + instruction_elements[3])
            address2 = DecimalToBinary(instruction_elements[4])
            instr_code = op_LHS + "XXXXXXXXXXXX" + op_RHS + address2
            return instr_code
        
        else:
            op_LHS = OPC(instruction_elements[0] + " " + instruction_elements[1])
            address1 = DecimalToBinary(instruction_elements[2])
            op_RHS = OPC(instruction_elements[3] + " " + instruction_elements[4])
            instr_code = op_LHS + address1 + op_RHS + "XXXXXXXXXXXX"
            return instr_code
    
    else:

        op_RHS = OPC(instruction_elements[0] + " " + instruction_elements[1])
        
        if len(instruction_elements) == 3:
            address2 = DecimalToBinary(instruction_elements[2])
            instr_code = "XXXXXXXXXXXXXXXXXXXX" + op_RHS + address2
        
        else:
            instr_code = "XXXXXXXXXXXXXXXXXXXX" + op_RHS + "XXXXXXXXXXXX"
        
        return instr_code



#main function to take input from the user
def main():
    
    #intialising the memory.
    #memory is an array of 1000 empty arrays which represent the 1000 memory locations in IAS
    for i in range (0, 1000):
        location = []
        memory.append(location)

    print("----------MENU----------\n[1] -> SWAP TWO NUMBERS\n[2] -> PERIMETER OF RECTANGLE\n[3] -> AREA OF RECTANGLE\n[4] -> FACTORIAL\n[5] -> DIVISION OF TWO NUMBERS\n")
    choice = int(input("Enter your choice in integer : "))
    print(" ")
    
    if choice == 1:
        a = int(input("Enter integer number 1 : "))
        b = int(input("Enter integer number 2 : "))
        memory[100].append(DtoB(a).zfill(40))
        memory[101].append(DtoB(b).zfill(40))
        print("\nDATA STORED AT MEMORY LOCATION 100 -> {}\nDATA STORED AT MEMORY LOCATION 101 -> {}\n".format(a,b))
        print("Enter the following instructions in the given order,\nLOAD M(X) 100 ADD M(X) 101\nSTOR M(X) 100\nLOAD M(X) 100 SUB M(X) 101\nSTOR M(X) 101\nLOAD M(X) 100 SUB M(X) 101\nSTOR M(X) 100\nHALT\n")
    elif choice == 2:
        a = int(input("Enter an integer length : "))
        b = int(input("Enter an integer breadth : "))
        memory[100].append(DtoB(a).zfill(40))
        memory[101].append(DtoB(b).zfill(40))
        print("\nDATA STORED AT MEMORY LOCATION 100 -> {}\nDATA STORED AT MEMORY LOCATION 101 -> {}\n".format(a,b))
        print("Enter the following instructions in the given order,\nLOAD M(X) 100 ADD M(X) 101\nSTOR M(X) 102\nLOAD M(X) 102 ADD M(X) 102\nSTOR M(X) 102\nHALT\n")
    
    elif choice == 3:
        a = int(input("Enter an integer length : "))
        b = int(input("Enter an integer breadth : "))
        memory[100].append(DtoB(a).zfill(40))
        memory[101].append(DtoB(b).zfill(40))
        print("\nDATA STORED AT MEMORY LOCATION 100 -> {}\nDATA STORED AT MEMORY LOCATION 101 -> {}\n".format(a,b))
        print("\nEnter the following instructions in the given order,\nLOAD MQ,M(X) 100 MUL M(X) 101\nLOAD MQ STOR M(X) 102\nHALT\n")
    
    elif choice == 4:
        a = int(input("Enter an integer number : "))
        memory[101].append(DtoB(a))
        memory[100].append(DtoB(1))
        memory[200].append(DtoB(1))
        if a == 0 or a == 1:
            print("Factorial of {} is 1\n".format(a))
            return
        print("\nDATA STORED AT MEMORY LOCATION 100 -> 1\nDATA STORED AT MEMORY LOCATION 101 -> {}\nDATA STORED AT MEMORY LOCATION 200 -> 1".format(a))
        print("\nEnter the following instructions in the given order,\nLOAD MQ,M(X) 100 MUL M(X) 101\nLOAD MQ STOR M(X) 100\nLOAD M(X) 101 SUB M(X) 200\nSTOR M(X) 101 LOAD M(X) 101\nJUMP +M(X,0:19) 1\nHALT\n")
    
    elif choice == 5:
        a = int(input("Enter an integer dividend : "))
        b = int(input("Enter an integer divisor : "))
        if b == 0:
            print("Division by zero not possible!")
            return
        memory[100].append(DtoB(a).zfill(40))
        memory[101].append(DtoB(b).zfill(40))
        print("\nDATA STORED AT MEMORY LOCATION 100 -> {}\nDATA STORED AT MEMORY LOCATION 101 -> {}\n".format(a,b))
        print("Enter the following instructions in the given order,\nLOAD MQ,M(X) 100 DIV M(X) 101\nLOAD MQ STOR M(X) 102\nHALT\n")
    
    else:
        print("INVALID CHOICE")
        return
    
    #initialising memory location to 1
    mem_loc = 1
    
    #taking in first instruction
    instruction = input("INSTRUCTION 1\n")
    print(" ")
    
    #fetching, decoding and executing instructions till user input is HALT
    while (instruction != "HALT"):
        PC = str(mem_loc)
        instruction_elements = instruction.split()
        x = Assembler(instruction_elements)
        #appending the 40 bit instruction to memory
        memory[mem_loc - 1].append(x)
        Decoder(memory[mem_loc-1],PC)
        #updating memory location and thereby the PC value
        mem_loc = mem_loc + 1
        instruction = input("INSTRUCTION {}\n".format(mem_loc))

#calling the main function
main()
