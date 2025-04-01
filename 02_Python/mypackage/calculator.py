# mypackage\calculater.py

__version__  = 0.1

# func
def plus(num1, num2):
    return num1 + num2
def minus(num1, num2):
    return num1 - num2
def multiply(num1, num2):
    return num1 * num2
def divide(num1, num2):
    return num1 / num2

if __name__ == "__main__":
    print(">>>>>>name<<<<<<<", __name__)
    print(plus(10,20))
    print(minus(10,5))