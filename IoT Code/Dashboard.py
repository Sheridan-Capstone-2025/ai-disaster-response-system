from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

latest_temp = None

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Temperature Dashboard</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: black;
            color: white;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-size: 80px;
        }
    </style>
    <script>
        function updateTemp() {
            fetch('/api/temperature')
                .then(response => response.json())
                .then(data => {
                    if (data.temperature !== null) {
                        document.getElementById('temp').textContent = data.temperature + '°C';
                    }
                });
        }
        setInterval(updateTemp, 2000);
        updateTemp();
    </script>
</head>
<body>
    <div id="temp">--°C</div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/temperature', methods=['POST'])
def receive_temperature():
    global latest_temp
    data = request.get_json()
    latest_temp = data['temperature']
    print(f"Received: {latest_temp}°C")
    return jsonify({'success': True})

@app.route('/api/temperature', methods=['GET'])
def get_temperature():
    return jsonify({'temperature': latest_temp})

if __name__ == '__main__':
    print("Dashboard running at http://localhost:5000")
    app.run(host='0.0.0.0', port=5000)