from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML_CODE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة القيادة العالمية لعمر 2026</title>
    <style>
        body {
            background-color: #0d1117;
            color: #ffffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            overflow: hidden;
        }
        h1 { color: #58a6ff; margin-bottom: 10px; font-size: 1.4rem; text-align: center; }
        .gauge-container { position: relative; width: 240px; height: 240px; margin-bottom: 15px; }
        .gauge {
            width: 100%; height: 100%; border-radius: 50%;
            background: conic-gradient(#58a6ff 0deg, #1f6feb 180deg, #58a6ff 240deg, #21262d 240deg);
            display: flex; align-items: center; justify-content: center;
            box-shadow: 0 0 20px rgba(88, 166, 255, 0.2);
        }
        .inner-circle {
            width: 85%; height: 85%; background-color: #0d1117; border-radius: 50%;
            display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative;
        }
        .needle {
            position: absolute; width: 4px; height: 95px;
            background: linear-gradient(to top, transparent 30%, #ff5555 30%);
            bottom: 50%; left: calc(50% - 2px); transform-origin: bottom center;
            transform: rotate(-120deg); transition: transform 0.1s ease-out;
        }
        .speed-display { font-size: 3.5rem; font-weight: bold; color: #ffffff; margin-top: 15px; z-index: 10; font-family: monospace; }
        .unit { font-size: 0.9rem; color: #8b949e; }
        .status { font-size: 1rem; color: #58a6ff; font-weight: bold; text-align: center; margin-top: 10px; }
    </style>
</head>
<body>
    <h1>أوريدو ⚡ لوحة القيادة العالمية</h1>
    <div class="gauge-container">
        <div class="gauge">
            <div class="inner-circle">
                <div class="needle" id="needle"></div>
                <div class="speed-display" id="speed">0.0</div>
                <div class="unit">كم / ساعة</div>
            </div>
        </div>
    </div>
    <div class="status" id="status">🟢 العداد العالمي مستقر وجاهز تماماً لحساب سرعتك</div>
    <script>
        const needle = document.getElementById('needle');
        const speedDisplay = document.getElementById('speed');
        const statusDisplay = document.getElementById('status');
        if (navigator.geolocation) {
            navigator.geolocation.watchPosition(updateDashboard, handleError, {
                enableHighAccuracy: true, maximumAge: 0, timeout: 10000
            });
        }
        function updateDashboard(position) {
            let speed = position.coords.speed; 
            if (speed === null || speed === undefined || isNaN(speed) || speed < 0) { speed = 0.0; }
            else { speed = speed * 3.6; }
            if (speed < 0.5) speed = 0.0;
            speedDisplay.innerText = speed.toFixed(1);
            let rotation = -120 + (Math.min(speed, 180) / 180) * 240;
            needle.style.transform = `rotate(${rotation}deg)`;
        }
        function handleError(error) { statusDisplay.innerHTML = "📶 جاري ربط مستشعرات جهازك بالأقمار الصناعية..."; }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_CODE)

if __name__ == '__main__':
    # تهيئة ذكية متوافقة مع ريندر وفي نفس الوقت تعمل محلياً على بورت 8080 لتجنب التصادم
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
