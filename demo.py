from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    # Assuming the file is located in a folder named 'Eda'
    name = 'diamonds.csv'
    filename = f'eda_report_{name}.html'
    return send_from_directory('Eda',filename )
    return send_from_directory(f'Eda', 'eda_report_{filename}.html')

if __name__ == '__main__':
    app.run(debug=True)
