from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def gauss_seidel(matrix, b, x0=None, accuracy=1e-6, max_iterations=100):
    n = len(matrix)
    x = x0 or [0] * n
    iterations = {0: [round(val, 5) for val in x]}  # Round initial values to 5 decimals

    for iteration in range(1, max_iterations + 1):
        x_old = x.copy()
        for i in range(n):
            sigma = sum(matrix[i][j] * x[j] for j in range(n) if j != i)
            x[i] = (b[i] - sigma) / matrix[i][i]

        # Round values to 5 decimals
        x = [round(val, 5) for val in x]

        # Store the current roots for the iteration
        iterations[iteration] = x.copy()

        # Check for convergence
        if all(abs(x[i] - x_old[i]) < accuracy for i in range(n)):
            break

    return x, iterations

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        matrix = []
        b = []
        initial_values = []

        for i in range(3):
            x1 = float(request.form[f'x1_{i}'])
            x2 = float(request.form[f'x2_{i}'])
            x3 = float(request.form[f'x3_{i}'])
            b_value = float(request.form[f'b_{i}'])

            matrix.append([x1, x2, x3])
            b.append(b_value)

        initial_x1 = float(request.form.get('initial_x1', 0))
        initial_x2 = float(request.form.get('initial_x2', 0))
        initial_x3 = float(request.form.get('initial_x3', 0))

        accuracy = float(request.form.get('accuracy', 1e-6))

        roots, iterations = gauss_seidel(matrix, b, x0=[initial_x1, initial_x2, initial_x3], accuracy=accuracy)

        return redirect(url_for('result', roots=roots, iterations=iterations, equations=request.form.getlist('equation')))

    return render_template('index.html')

@app.route('/result')
def result():
    roots = request.args.getlist('roots')
    iterations = eval(request.args.get('iterations'))  
    equations = request.args.getlist('equations')

    return render_template('result.html', roots=roots, iterations=iterations, equations=equations)

if __name__ == '__main__':
    app.run(debug=True)
