print("BMI Calculator")

# Get user input
weight=float(input("Enter your weight in kg: "))
height=float(input("Enter your height in meters: "))

# Calculate BMI
bmi=weight/(height**2)

# Show result
print(f"Your BMI is: {bmi:.2f}")

# Check category
if bmi < 18.5:
    print("Category: Underweight")
elif bmi < 25:
    print("Category: Normal weight")
elif bmi < 30:
    print("Category: Overweight")
else:
    print("Category: Obesity")