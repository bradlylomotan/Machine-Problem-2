from flask import Flask, render_template, request

app = Flask(__name__)

def lagrange_interpolation(x_values, y_values, t):
    result = 0
    n = len(x_values)

    for i in range(n):
        term = y_values[i]
        for j in range(n):
            if j != i:
                term = term * (t - x_values[j]) / (x_values[i] - x_values[j])
        result += term

    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    num_points = 6  # Default number of points
    result = None

    if request.method == 'POST':
        num_points = int(request.form['num_points'])

        x_values = [float(request.form[f'x{i+1}']) for i in range(num_points)]
        y_values = [float(request.form[f'y{i+1}']) for i in range(num_points)]
        t_value = float(request.form['t'])

        if len(x_values) == len(y_values) and len(x_values) > 0:
            result = lagrange_interpolation(x_values, y_values, t_value)

    return render_template('index.html', num_points=num_points, result=result)

if __name__ == '__main__':
    app.run(debug=True)
