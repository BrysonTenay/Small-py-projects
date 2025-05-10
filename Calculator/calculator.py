def calculator():
    print("Simple Calculator")
    print("Operations: +, -, *, /")
    
    while True:
        try:
            num1 = float(input("Enter first number: "))
            op = input("Enter operator: ")
            num2 = float(input("Enter second number: "))
            
            if op == '+':
                result = num1 + num2
            elif op == '-':
                result = num1 - num2
            elif op == '*':
                result = num1 * num2
            elif op == '/':
                if num2 == 0:
                    print("Error: Cannot divide by zero!")
                    continue
                result = num1 / num2
            else:
                print("Invalid operator!")
                continue
                
            print(f"Result: {result}")
            
            again = input("Calculate again? (yes/no): ").lower()
            if again != 'yes':
                break
                
        except ValueError:
            print("Invalid input! Please enter numbers.")
            
if __name__ == "__main__":
    calculator()