#python programs of the functions implemented in IAS


#swap without a temporary variable
def swap(a, b):
    print("a,b -> {},{}".format(a,b))
    a = a + b
    b = a - b
    a = a - b
    print("a,b -> {},{}".format(a,b))

#perimeter of a rectangle
def perimeter(l, b):
    p = l + b
    p = 2*p
    print("Perimeter -> {}".format(p))

#area of rectangle
def area(l, b):
    ar = l*b
    print("Area -> {}".format(ar))

#factorial of a number
def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n*factorial(n-1)

#division of two numbers
def division(a, b):
    if b == 0:
        print("Division by zero is not possible!")
        return
    else:
        res =  a//b
        rem = a%b
        print("Quotient, remainder -> {},{}".format(res, rem))


    
