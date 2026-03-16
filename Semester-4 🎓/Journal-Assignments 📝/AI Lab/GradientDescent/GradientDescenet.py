# Cost function
def cost(v):
    return v**2 - 12*v + 50

# Derivative of cost function
def derivative(v):
    return 2*v - 12

# Gradient Descent parameters
alpha = 0.1      # learning rate
v = 0.0          # initial guess (speed)
iterations = 15

print("Iteration | v (speed variable) | Cost C(v) | Gradient")

for i in range(iterations):
    grad = derivative(v)
    c = cost(v)

    print(f"{i:9d} | {v:17.4f} | {c:10.4f} | {grad:8.4f}")

    # Gradient Descent update
    v = v - alpha * grad

print("\nApproximate optimal v:", round(v,4))
print("Optimal vehicle speed:", round(v*10,2), "km/h")