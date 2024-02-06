from flask import Flask, render_template, request
import sympy as sp

app = Flask(__name__)

def fixed_point_iteration(polynomial, initial_guess, tolerance, max_iterations):
    iterations = []

    # Define the fixed-point iteration function g(x) = f(x)
    def fixed_point_function(x):
        return polynomial.subs('x', x)

    xn = initial_guess
    xn_plus_1 = fixed_point_function(xn)
    iteration_count = 0

    while abs(xn_plus_1 - xn) >= tolerance and iteration_count < max_iterations:
        iterations.append((xn, xn_plus_1))
        xn = xn_plus_1
        xn_plus_1 = fixed_point_function(xn)
        iteration_count += 1

    return iterations

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        polynomial_str = request.form['polynomial']
        initial_guess = float(request.form['initial_guess'])
        tolerance = float(request.form['tolerance'])
        max_iterations = int(request.form['max_iterations'])

        # Define the variable 'x'
        x = sp.symbols('x')

        # Define the polynomial function
        poly_func = sp.sympify(polynomial_str.replace('^', '**'))
        poly_func = poly_func.subs('x', x)

        # Perform fixed-point iteration
        iterations = fixed_point_iteration(poly_func, initial_guess, tolerance, max_iterations)

        return render_template('index.html', iterations=iterations)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
