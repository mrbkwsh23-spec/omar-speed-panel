from flask import Flask, render_template_string
import os

app = Flask(__name__)

# نسخة 2026 الخارقة - ألوان نيون متوهجة + أعلى سرعة + عداد المسافة
HTML_CODE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة القيادة النيون الفائقة 2026</title>
    <style>
        body {
            background-color: #05070c;
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
        h1 {
            color: #00f0ff;
            margin-bottom: 10px;
            font-size: 1.3rem;
            text-shadow: 0 0 10px #00f0ff, 0 0 20px #00f0ff;
            text-align: center;
            font-weight: 800;
        }
        .stats-container {
            display: flex;
            justify-content: space-between;
            width: 270px;
            margin-bottom: 15px;
        }
        .stat-box {
            background-color: #0b111e;
            border: 2px solid #00f0ff;
            border-radius: 12px;
            padding: 8px 5px;
            text-align: center;
            width: 45%;
            box-shadow: 0 0 10px rgba(0, 240, 255, 0.3);
        }
        .stat-title {
            font-size: 0.75rem;
            color: #8b949e;
            margin-bottom: 3px;
        }
        .stat-value {
            font-size: 1.2rem;
            font-weight: bold;
            color: #39ff14;
            text-shadow: 0 0 8px #39ff14;
            font-family: monospace;
        }
        .gauge-container {
            position: relative;
            width: 250px;
            height: 250px;
            margin-bottom: 15px;
        }
        .gauge {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background: conic-gradient(#00f0ff 0deg, #ff007f 180deg, #ffaa00 240deg, #121824 240deg);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 30px rgba(0, 240, 255, 0.4);
            position: relative;
        }
        .inner-circle {
            width: 86%;
            height: 86%;
            background-color: #05070c;
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
            border: 1px solid #121824;
        }
        .needle {
            position: absolute;
            width: 4px;
            height: 100px;
            background: linear-gradient(to top, transparent 20%, #ff0055 20%);
            bottom: 50%;
            left: calc(50% - 2px);
            transform-origin: bottom center;
            transform: rotate(-120deg);
            transition: transform 0.1s ease-out;
            filter: drop-shadow(0 0 5px #ff0055);
        }
        .speed-display {
            font-size: 3.8rem;
            font-weight: 900;
            color: #ffffff;
            margin-top: 15px;
            z-index: 10;
            font-family: monospace;
            text-shadow: 0 0 15px rgba(255, 255, 255, 0.5);
        }
        .unit {
            font-size: 0.85rem;
            color: #00f0ff;
            font-weight: bold;
            text-shadow: 0 0 5px #00f0ff;
        }
        .status {
            font-size: 0.95rem;
            color: #39ff14;
            font-weight: bold;
            text-align: center;
            margin-top: 10px;
            text-shadow: 0 0 8px rgba(57, 255, 20, 0.4);
        }
    </style>
</head>
<body>

    <h1>أوريدو ⚡ كوكبيت النيون الفائق</h1>
    
    <div class="stats-container">
        <div class="stat-box">
            <div class="stat-title">أعلى سرعة 🏆</div>
            <div class="stat-value" id="topSpeed">0.0</div>
        </div>
        <div class="stat-box">
            <div class="stat-title">المسافة 📊</div>
            <div class="stat-value" id="odometer">0.000</div>
        </div>
    </div>
    
    <div class="gauge-container">
        <div class="gauge" id="gaugeBody">
            <div class="inner-circle">
                <div class="needle" id="needle"></div>
                <div class="speed-display" id="speed">0.0</div>
                <div class="unit">كم / ساعة</div>
            </div>
        </div>
    </div>
    
    <div class="status" id="status">🟢 العداد النشط جاهز تماماً للحساب فائق الدقة</div>

    <script>
        const needle = document.getElementById('needle');
        const speedDisplay = document.getElementById('speed');
        const statusDisplay = document.getElementById('status');
        const topSpeedDisplay = document.getElementById('topSpeed');
        const odometerDisplay = document.getElementById('odometer');

        let lastLat = null, lastLon = null, lastTime = null;
        let totalDistance = 0.0;
        let maxSpeed = 0.0;

        if (navigator.geolocation) {
            navigator.geolocation.watchPosition(updateDashboard, handleError, {
                enableHighAccuracy: true,
                maximumAge: 0,
                timeout: 10000
            });
        }

        function updateDashboard(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            const time = new Date();
            
            let speed = position.coords.speed; 
            
            if (speed === null || speed === undefined || isNaN(speed) || speed < 0) {
                if (lastLat !== null && lastLon !== null && lastTime !== null) {
                    const distance = calculateDistance(lastLat, lastLon, lat, lon);
                    if (distance > 0.0005) {
                        totalDistance += distance;
                    }
                    const timeDiff = (time - lastTime) / 3600000;
                    speed = timeDiff > 0 ? (distance / timeDiff) : 0;
                } else { speed = 0; }
            } else {
                speed = speed * 3.6; 
                if (lastLat !== null && lastLon !== null) {
                    const distance = calculateDistance(lastLat, lastLon, lat, lon);
                    if (distance > 0.0005 && distance < 0.5) {
                        totalDistance += distance;
                    }
                }
            }

            if (speed < 0.5) speed = 0.0;
            
            speedDisplay.innerText = speed.toFixed(1);
            
            if (speed > maxSpeed) {
                maxSpeed = speed;
                topSpeedDisplay.innerText = maxSpeed.toFixed(1);
            }
            
            odometerDisplay.innerText = totalDistance.toFixed(3);
            
            let rotation = -120 + (Math.min(speed, 180) / 180) * 240;
            needle.style.transform = `rotate(${rotation}deg)`;

            lastLat = lat;
            lastLon = lon;
            lastTime = time;
        }

        function calculateDistance(lat1, lon1, lat2, lon2) {
            const R = 6371;
            const dLat = (lat2 - lat1) * Math.PI / 180;
            const dLon = (lon2 - lon1) * Math.PI / 180;
            const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                      Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
                      Math.sin(dLon/2) * Math.sin(dLon/2);
            return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        }

        function handleError(error) {
            statusDisplay.innerHTML = "📶 جاري ربط مستشعرات العداد بالأقمار الصناعية...";
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_CODE)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
