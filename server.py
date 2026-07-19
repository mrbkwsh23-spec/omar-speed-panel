from flask import Flask, render_template_string
import os

app = Flask(__name__)

# نسخة السيارات الحديثة المتطورة الفاخرة 2026 - استجابة فورية 100% وقفل الصفر التام عند الوقوف
HTML_CODE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة القيادة الذكية الفاخرة 2026</title>
    <style>
        :root {
            --neon-color: #00f0ff;
            --neon-glow: rgba(0, 240, 255, 0.4);
        }
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
            transition: transform 0.3s ease;
        }
        body.hud-mode {
            transform: scaleX(-1);
        }
        h1 {
            color: var(--neon-color);
            margin-bottom: 5px;
            font-size: 1.2rem;
            text-shadow: 0 0 10px var(--neon-color);
            text-align: center;
            font-weight: 800;
        }
        .stats-container {
            display: flex;
            justify-content: space-between;
            width: 270px;
            margin-bottom: 12px;
        }
        .stat-box {
            background-color: #0b111e;
            border: 2px solid var(--neon-color);
            border-radius: 12px;
            padding: 6px 5px;
            text-align: center;
            width: 45%;
            box-shadow: 0 0 10px var(--neon-glow);
        }
        .stat-title {
            font-size: 0.75rem;
            color: #8b949e;
            margin-bottom: 2px;
        }
        .stat-value {
            font-size: 1.2rem;
            font-weight: bold;
            color: #ffffff;
            font-family: monospace;
        }
        .gauge-container {
            position: relative;
            width: 245px;
            height: 245px;
            margin-bottom: 15px;
        }
        .gauge {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background: conic-gradient(var(--neon-color) 0deg, #ff007f 180deg, var(--neon-color) 240deg, #121824 240deg);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 25px var(--neon-glow);
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
        }
        .needle {
            position: absolute;
            width: 4px;
            height: 98px;
            background: linear-gradient(to top, transparent 30%, #ff0055 30%);
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
            text-shadow: 0 0 12px rgba(255, 255, 255, 0.4);
        }
        .unit {
            font-size: 0.85rem;
            color: var(--neon-color);
            font-weight: bold;
            text-shadow: 0 0 5px var(--neon-color);
        }
        .controls-panel {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 10px;
            margin-top: 5px;
            width: 270px;
        }
        .hud-btn {
            background-color: #161b22;
            border: 2px solid var(--neon-color);
            color: #ffffff;
            border-radius: 20px;
            padding: 5px 15px;
            font-size: 0.85rem;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 0 8px var(--neon-glow);
        }
        .themes-container {
            display: flex;
            justify-content: center;
            gap: 15px;
        }
        .theme-dot {
            width: 22px;
            height: 22px;
            border-radius: 50%;
            cursor: pointer;
            border: 2px solid #ffffff;
        }
    </style>
</head>
<body>

    <h1>أوريدو ⚡ لوحة القيادة المتطورة الفاخرة</h1>
    
    <div class="stats-container">
        <div class="stat-box">
            <div class="stat-title">أعلى سرعة 🏆</div>
            <div class="stat-value" id="topSpeed">0.0</div>
        </div>
        <div class="stat-box">
            <div class="stat-title">المسافة المقطوعة 📊</div>
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
    
    <div class="controls-panel">
        <button class="hud-btn" id="hudToggle" onclick="toggleHUD()">تفعيل وضع الزجاج الأمامي HUD</button>
        
        <div class="themes-container">
            <div class="theme-dot" style="background-color: #00f0ff;" onclick="changeTheme('#00f0ff', 'rgba(0, 240, 255, 0.4)')"></div>
            <div class="theme-dot" style="background-color: #39ff14;" onclick="changeTheme('#39ff14', 'rgba(57, 255, 20, 0.4)')"></div>
            <div class="theme-dot" style="background-color: #ff0055;" onclick="changeTheme('#ff0055', 'rgba(255, 0, 85, 0.4)')"></div>
            <div class="theme-dot" style="background-color: #ffaa00;" onclick="changeTheme('#ffaa00', 'rgba(255, 170, 0, 0.4)')"></div>
        </div>
    </div>

    <script>
        const needle = document.getElementById('needle');
        const speedDisplay = document.getElementById('speed');
        const topSpeedDisplay = document.getElementById('topSpeed');
        const odometerDisplay = document.getElementById('odometer');

        let lastTime = null;
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
            let speed = position.coords.speed; 
            const time = new Date();
            
            if (speed === null || speed === undefined || isNaN(speed) || speed < 0) {
                speed = 0.0;
            } else {
                speed = speed * 3.6; // تحويل فوري ودقيق للسرعة اللحظية المفلترة من المعالج
                
                // حساب المسافة التراكمية الدقيقة بالاعتماد على السرعة الجاهزة
                if (lastTime !== null) {
                    const hoursPassed = (time - lastTime) / 3600000;
                    if (hoursPassed > 0 && speed > 0.5) {
                        totalDistance += (speed * hoursPassed);
                    }
                }
            }

            // ⚙️ فلتر قفل الصفر الذكي (محاكاة السيارات الحديثة):
            // إذا كانت السرعة أقل من 0.8 كم/ساعة، يُقفل العداد فوراً عند الصفر المطلق ويموت أي اهتزاز فضائي
            if (speed < 0.8) {
                speed = 0.0;
            }
            
            speedDisplay.innerText = speed.toFixed(1);
            
            if (speed > maxSpeed) {
                maxSpeed = speed;
                topSpeedDisplay.innerText = maxSpeed.toFixed(1);
            }
            
            odometerDisplay.innerText = totalDistance.toFixed(3);
            
            let rotation = -120 + (Math.min(speed, 180) / 180) * 240;
            needle.style.transform = `rotate(${rotation}deg)`;

            lastTime = time;
        }

        function toggleHUD() {
            document.body.classList.toggle('hud-mode');
            const btn = document.getElementById('hudToggle');
            btn.innerText = document.body.classList.contains('hud-mode') ? "تعطيل وضع الزجاج HUD" : "تفعيل وضع الزجاج الأمامي HUD";
        }

        function changeTheme(color, glow) {
            document.documentElement.style.setProperty('--neon-color', color);
            document.documentElement.style.setProperty('--neon-glow', glow);
        }

        function handleError(error) {}
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
