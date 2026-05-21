# from flask import Flask
# import random
# import os

# app = Flask(__name__)

# @app.route('/')
# def hello():
#     # 20% chance of random failure to test self-healing
#     if random.random() < 0.2:
#         return "Random failure occurred! Retrying...", 500
#     return "Hello from Self-Healing Pipeline! 🚀", 200

# @app.route('/health')
# def health():
#     return "OK", 200

# @app.route('/fail')
# def force_fail():
#     """Endpoint to force failure for testing self-healing"""
#     return "Forced failure!", 500

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port)



from flask import Flask, jsonify, render_template_string, request
import random
import os
import time
from datetime import datetime

app = Flask(__name__)

# Track request count for demo
request_count = 0
failure_count = 0

# HTML Template for beautiful UI
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Self-Healing DevOps Pipeline Demo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            max-width: 600px;
            width: 100%;
            text-align: center;
            animation: fadeIn 0.5s ease-in;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        h1 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .badge {
            display: inline-block;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 8px 20px;
            border-radius: 50px;
            font-size: 0.9em;
            margin-bottom: 30px;
        }
        .status-card {
            background: #f7f9fc;
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            border-left: 4px solid #28a745;
        }
        .status-card.success {
            border-left-color: #28a745;
        }
        .status-card.failure {
            border-left-color: #dc3545;
            animation: shake 0.5s ease-in-out;
        }
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-10px); }
            75% { transform: translateX(10px); }
        }
        .message {
            font-size: 1.2em;
            color: #333;
            margin: 15px 0;
        }
        .status {
            font-size: 1.1em;
            font-weight: bold;
        }
        .status.success { color: #28a745; }
        .status.failure { color: #dc3545; }
        
        .stats {
            display: flex;
            justify-content: space-around;
            margin: 30px 0;
            flex-wrap: wrap;
            gap: 15px;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 15px 25px;
            border-radius: 12px;
            flex: 1;
            min-width: 120px;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
        }
        .stat-label {
            font-size: 0.8em;
            opacity: 0.9;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 50px;
            cursor: pointer;
            font-size: 1em;
            margin: 10px;
            transition: transform 0.2s;
        }
        .btn:hover {
            transform: scale(1.05);
        }
        .btn-danger {
            background: linear-gradient(135deg, #dc3545, #c82333);
        }
        .btn-success {
            background: linear-gradient(135deg, #28a745, #20c997);
        }
        
        .footer {
            margin-top: 30px;
            font-size: 0.8em;
            color: #888;
            border-top: 1px solid #eee;
            padding-top: 20px;
        }
        
        .healing-badge {
            background: #28a745;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 0.7em;
            display: inline-block;
            margin-left: 10px;
        }
        
        .features {
            display: flex;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
            margin: 20px 0;
        }
        .feature {
            background: #e9ecef;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.7em;
            color: #495057;
        }
        
        .timestamp {
            font-size: 0.7em;
            color: #888;
            margin-top: 10px;
        }
    </style>
    <script>
        function refreshPage() {
            location.reload();
        }
        
        function testFailure() {
            fetch('/fail')
                .then(response => response.text())
                .then(data => {
                    alert('Forced failure triggered! Check the demo.');
                    location.reload();
                });
        }
        
        function testHealth() {
            fetch('/health')
                .then(response => response.text())
                .then(data => {
                    alert('Health Check: ' + data);
                });
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>🔄 Self-Healing Pipeline</h1>
        <div class="badge">⚡ Intelligent CI/CD with Auto-Recovery</div>
        
        <div class="status-card {{ 'failure' if is_failure else 'success' }}">
            <div class="message">{{ message }}</div>
            <div class="status {{ 'failure' if is_failure else 'success' }}">
                {{ '⚠️ Self-Healing Triggered!' if is_failure else '✅ System Operational' }}
            </div>
            {% if is_failure %}
            <div class="healing-badge">🔄 Auto-Retry in Progress...</div>
            {% endif %}
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{{ total_requests }}</div>
                <div class="stat-label">Total Requests</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ failures }}</div>
                <div class="stat-label">Auto-Healed Failures</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ success_rate }}%</div>
                <div class="stat-label">Success Rate</div>
            </div>
        </div>
        
        <div class="features">
            <span class="feature">🔄 Auto-Retry (3x)</span>
            <span class="feature">🩺 Health Checks</span>
            <span class="feature">📦 Docker Container</span>
            <span class="feature">🚀 CI/CD Pipeline</span>
            <span class="feature">🔁 Auto-Rollback</span>
        </div>
        
        <div>
            <button class="btn" onclick="refreshPage()">🔄 Refresh</button>
            <button class="btn btn-danger" onclick="testFailure()">💥 Force Failure</button>
            <button class="btn btn-success" onclick="testHealth()">🩺 Health Check</button>
        </div>
        
        <div class="footer">
            <p>⚡ Self-Healing Demo | 20% Random Failure Rate</p>
            <p>Jenkins Pipeline | Docker | GitHub Actions</p>
            <div class="timestamp">🕐 {{ timestamp }}</div>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def hello():
    global request_count, failure_count
    request_count += 1
    
    # 20% chance of random failure to test self-healing
    is_failure = random.random() < 0.2
    
    if is_failure:
        failure_count += 1
        message = "❌ Random failure occurred! Jenkins will auto-retry..."
        status_code = 500
    else:
        message = "✅ Hello from Self-Healing Pipeline! Everything is running smoothly."
        status_code = 200
    
    # Calculate success rate
    success_rate = round(((request_count - failure_count) / request_count) * 100, 1) if request_count > 0 else 100
    
    return render_template_string(
        HTML_TEMPLATE,
        message=message,
        is_failure=is_failure,
        total_requests=request_count,
        failures=failure_count,
        success_rate=success_rate,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ), status_code

@app.route('/health')
def health():
    """Health check endpoint for Docker and Jenkins"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": "running",
        "total_requests": request_count,
        "failures_handled": failure_count
    }), 200

@app.route('/fail')
def force_fail():
    """Endpoint to force failure for testing self-healing"""
    global failure_count
    failure_count += 1
    return jsonify({
        "status": "failure",
        "message": "Forced failure triggered for self-healing demo!",
        "timestamp": datetime.now().isoformat()
    }), 500

@app.route('/stats')
def stats():
    """View statistics endpoint"""
    success_rate = round(((request_count - failure_count) / request_count) * 100, 2) if request_count > 0 else 100
    return jsonify({
        "total_requests": request_count,
        "failures": failure_count,
        "success_rate": f"{success_rate}%",
        "healing_efficiency": "Auto-retry and rollback active"
    }), 200

@app.route('/reset')
def reset():
    """Reset statistics (for testing)"""
    global request_count, failure_count
    request_count = 0
    failure_count = 0
    return jsonify({"message": "Statistics reset successfully!"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║     🚀 SELF-HEALING PIPELINE DEMO 🚀                      ║
    ║                                                           ║
    ║     Application running on: http://localhost:{port}       ║
    ║     Health check: http://localhost:{port}/health          ║
    ║     Statistics: http://localhost:{port}/stats             ║
    ║                                                           ║
    ║     Features:                                             ║
    ║     • 20% random failure (tests self-healing)            ║
    ║     • Auto-retry by Jenkins (3 attempts)                 ║
    ║     • Health monitoring endpoint                         ║
    ║     • Beautiful web interface                            ║
    ║                                                           ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=port, debug=False)