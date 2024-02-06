from flask import Flask, render_template, request
import sympy as sp

app = Flask(__name__)

class Segment:
    def __init__(self, n, x, fx, multiplier, simpsons_result):
        self.n = n
        self.x = x
        self.fx = fx
        self.multiplier = multiplier
        self.simpsons_result = simpsons_result

def simpsons_3_8_rule(func, a, b, n):
    h = (b - a) / n
    x_values = [a + i * h for i in range(n + 1)]
    fx_values = [func.subs('x', x_val) for x_val in x_values]

    segments = []
    multipliers = [1] + [3 if i % 3 == 1 or i % 3 == 2 else 2 for i in range(1, n)] + [1]
    
    cumulative_sum = 0
    for i in range(n + 1):
        simpson_rule = fx_values[i] * multipliers[i]
        cumulative_sum += simpson_rule
        segment = Segment(i, x_values[i], fx_values[i], multipliers[i], simpson_rule)
        segments.append(segment)

    overall_result = cumulative_sum
    integral_result = (3 * h / 8) * overall_result

    return segments, overall_result, integral_result

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        poly_function = request.form['poly_function']
        lower_boundary = float(request.form['lower_boundary'])
        upper_boundary = float(request.form['upper_boundary'])
        num_segments = int(request.form['num_segments'])

        x = sp.symbols('x')
        function = sp.sympify(poly_function.replace('x', 'x'))  

        segments, overall_result, integral_result = simpsons_3_8_rule(function, lower_boundary, upper_boundary, num_segments)

        return render_template('result.html', segments=segments, overall_result=overall_result, integral_result=integral_result)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
