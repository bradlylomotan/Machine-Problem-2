from flask import Flask, render_template, request
import sympy as sp

app = Flask(__name__)

def backward_finite_difference(poly, x_value, step_size):
    x = sp.symbols('x')
    expr = sp.sympify(poly)
    
    x_value = float(x_value)
    step_size = float(step_size)
    
    result = (expr.subs(x, x_value) - expr.subs(x, x_value - step_size)) / step_size
    more_accurate = ((expr.subs(x, x_value))*3 - (expr.subs(x, x_value - step_size))*4 + expr.subs(x, x_value - (step_size*2))) / (step_size*2)

    return result, more_accurate

def richardsons_extrapolation(result_h1, result_h2, factor):
    richardson_result = ((2**factor * result_h2) - result_h1) / (2**factor - 1)
    return richardson_result



@app.route('/', methods=['GET', 'POST'])
def index():
    result_h1 = None
    result_h2 = None
    more_accurate_h1 = None
    more_accurate_h2 = None
    richardson_result = None

    if request.method == 'POST':
        poly = request.form['polynomial']
        x_value = request.form['x_value']
        
        try:
            step_size_h1 = request.form['step_size_h1']
            step_size_h2 = request.form['step_size_h2']
            
            x = sp.symbols('x')
            function = sp.sympify(poly.replace('x', 'x'))  # Include explicit multiplication operator

            result_h1, more_accurate_h1 = backward_finite_difference(function, x_value, step_size_h1)
            result_h2, more_accurate_h2 = backward_finite_difference(function, x_value, step_size_h2)

            # Richardson's Extrapolation using more_accurate_h1 and more_accurate_h2
            richardson_result = richardsons_extrapolation(result_h1, result_h2, factor=2)
        except KeyError as e:
            result = f"Error: {str(e)}"

    return render_template('index.html', result=(result_h1, result_h2, more_accurate_h2), richardson_result=richardson_result)

if __name__ == '__main__':
    app.run(debug=True)
