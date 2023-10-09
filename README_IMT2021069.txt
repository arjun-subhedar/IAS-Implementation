IAS IMPLEMENTATION IN PYTHON LANGUAGE

*The registers involved in IAS computer are:

1. AC  : Accumulator -> holds results of an ALU operation
2. IR  : Instructions Register -> stored the opcode of the instruction to be executed
3. IBR : Instructions Buffer register -> holds the RHS instruction temporarily
4. MQ  : Multiplier/Quotioent Register -> holds result of any multiplication or division
5. MBR : Memory BUffer register -> contains data/instruction to be read/stored in memory or I/O
6. MAR : Memory Adress register -> specifies the address in memory of the word to be written/read into MBR
7. PC  : Program Counter -> holds the next instruction’s address

*The program runs in the following cycles(steps),

1. Assembly level code is inputted and it is read by the Assembler which converts it to a binary code which can be understood by the machine.
2. The binary instruction/data is written into memory.
3. The instructions are then fetched into Decoder function which segments them in lhs and rhs.
4. The segmented instructions are then executed by the Execute function where they are executed according to the opcode specified in the instruction.

*How to run the code?

1. A menu is displayed from which you can choose to implement a function of your choice.
2. Once you input your the number of your choice, the program will ask for inputs for the function you wish to implement. These data inputs will be by default stored at memory locations starting from 100.
3. Next, a set of instructions in the assembly level language will be display to run the function.
4. After that, you will have to copy and paste the instructions in the given order and with the execution of each instruction a table displaying the current status of each component/register in the IAS system will be display. BYd efault instructions will be stored in the memory from location 1.
5. HALT instruction results in the termination of the program.

*The functions which can be executed in the program are as follows:
(negative values may be inputted but they will be prefixed with a '-' sign instead of a leading 1(binary notation for negative sign))

1. SWAP TO NUMBERS 
   (without a temporary variable i.e by using addition and subtraction)
   uses instructions,
   - LOAD M(X)
   - STOR M(X)
   - ADD M(X)
   - SUB M(X)

2. PERIMETER OF A RECTANGLE
   uses instructions,
   - LOAD M(X)
   - STOR M(X)
   - ADD M(X)
   (result will be stored at location 102)

3. AREA OF A RECTANGLE
   (a) if the result of the function exceeds 40 bits, then first forty bits(MSB's) are stored in AC and the next forty bits(LSB'S) are stored in MQ  
   uses instructions,
   - LOAD MQ,M(X)
   - MUL M(X)
   - LOAD MQ
   - STOR M(X)
   (result will be stored at location 102)

4. FACTORIAL OF A NUMBER
   (a) factorial of zero and one cannot be calculated, so a default return value of 1 will be returned.
   (b) A default value of 1 is stored at memory location 100 where the final result will be stored.
   (c) A deafult value of 1 is stored at memory location 200 so ass to decrement the inputted number by one every cycle.
   uses instructions,
   - LOAD MQ,M(X)
   - LOAD M(X)
   - STOR M(X)
   - MUL M(X)
   - LOAD MQ
   - SUB M(X)
   - JUMP +M(X,0:19)
   (result stored at location 100)

5. DIVISION OF TWO NUMBERS
   uses instructions,
   - LOAD MQ,M(X)
   - DIV M(X)
   - LOAD MQ
   - STOR M(X)
   (result stored at location 102)
   
**ARJUN SUBHEDAR (IMT2021069)**
