from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML_CODE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة القيادة المتكاملة الخارقة 2026</title>
    <style>
        :root {
            --neon-color: #00f0ff;
            --neon-glow: rgba(0, 240, 255, 0.4);
            --dynamic-ring: #39ff14;
        }
        body {
            background-color: #05070c; color: #ffffff;
            font-family: sans-serif; display: flex;
            flex-direction: column; align-items: center;
            justify-content: center; height: 100vh; margin: 0; overflow: hidden;
        }
        body.hud-mode { transform: scaleX(-1); }
        h1 {
            color: var(--neon-color); text-shadow: 0 0 10px var(--neon-color);
            text-align: center; font-weight: 800; font-size: 1.2rem; margin-bottom: 5px;
        }
        .stats-container { display: flex; justify-content: space-between; width: 280px; margin-bottom: 8px; }
        .stat-box { background-color: #0b111e; border: 2px solid var(--neon-color); border-radius: 12px; padding: 5px 2px; text-align: center; width: 31%; box-shadow: 0 0 8px var(--neon-glow); }
        .stat-title { font-size: 0.65rem; color: #8b949e; }
        .stat-value { font-size: 1rem; font-weight: bold; color: #ffffff; font-family: monospace; }
        .gauge-container { position: relative; width: 240px; height: 240px; margin-bottom: 10px; }
        .gauge {
            width: 100%; height: 100%; border-radius: 50%;
            background: conic-gradient(var(--dynamic-ring) 0deg, #ff007f 180deg, var(--dynamic-ring) 240deg, #121824 240deg);
            display: flex; align-items: center; justify-content: center; box-shadow: 0 0 25px var(--neon-glow);
        }
        .inner-circle { width: 86%; height: 86%; background-color: #05070c; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; }
        .needle {
            position: absolute; width: 4px; height: 95px; background: linear-gradient(to top, transparent 20%, #ff0055 20%); bottom: 50%; left: calc(50% - 2px); transform-origin: bottom center; transform: rotate(-120deg); transition: transform 0.1s ease-out; filter: drop-shadow(0 0 4px #ff0055);
        }
        .speed-display { font-size: 3.5rem; font-weight: 900; color: #ffffff; margin-top: 15px; z-index: 10; font-family: monospace; text-shadow: 0 0 10px rgba(255, 255, 255, 0.4); }
        .unit { font-size: 0.8rem; color: var(--neon-color); font-weight: bold; text-shadow: 0 0 5px var(--neon-color); }
        .controls-panel { display: flex; flex-direction: column; align-items: center; gap: 8px; margin-top: 5px; width: 280px; }
        .hud-btn { background-color: #161b22; border: 2px solid var(--neon-color); color: #ffffff; border-radius: 20px; padding: 4px 12px; font-size: 0.8rem; font-weight: bold; cursor: pointer; box-shadow: 0 0 8px var(--neon-glow); }
        .themes-container { display: flex; justify-content: center; gap: 12px; }
        .theme-dot { width: 20px; height: 20px; border-radius: 50%; cursor: pointer; border: 2px solid #ffffff; }
    </style>
</head>
<body>
    <h1>أوريدو ⚡ لوحة القيادة الخارقة المتكاملة</h1>
    <div class="stats-container">
        <div class="stat-box"><div class="stat-title">أعلى سرعة 🏆</div><div class="stat-value" id="topSpeed">0.0</div></div>
        <div class="stat-box"><div class="stat-title">تسارع 0-60 ⏱️</div><div class="stat-value" id="accTimer">0.00ث</div></div>
        <div class="stat-box"><div class="stat-title">المسافة 📊</div><div class="stat-value" id="odometer">0.000</div></div>
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
        const accTimerDisplay = document.getElementById('accTimer');
        let lastLat = null, lastLon = null, lastTime = null;
        let totalDistance = 0.0, maxSpeed = 0.0, timerStart = null, timerRunning = false, accTimeFinal = 0.0;

        if (navigator.geolocation) {
            navigator.geolocation.watchPosition(updateDashboard, handleError, { enableHighAccuracy: true, maximumAge: 0, timeout: 10000 });
        }
        function updateDashboard(position) {
            const lat = position.coords.latitude; const lon = position.coords.longitude; const time = new Date();
            let speed = position.coords.speed;
            if (speed === null || speed === undefined || isNaN(speed) || speed < 0) {
                if (lastLat !== null && lastLon !== null && lastTime !== null) {
                    const distance = calculateDistance(lastLat, lastLon, lat, lon);
                    if (distance > 0.0005) totalDistance += distance;
                    const timeDiff = (time - lastTime) / 3600000; speed = timeDiff > 0 ? (distance / timeDiff) : 0;
                } else { speed = 0; }
            } else {
                speed = speed * 3.6;
                if (lastLat !== null && lastLon !== null) {
                    const distance = calculateDistance(lastLat, lastLon, lat, lon);
                    if (distance > 0.0005 && distance < 0.5) totalDistance += distance;
                }
            }
            if (speed < 0.5) speed = 0.0;
            speedDisplay.innerText = speed.toFixed(1);
            if (speed === 0.0) { if (!timerRunning && accTimeFinal === 0.0) accTimerDisplay.innerText = "0.00ث"; }
            else if (speed > 0.5 && speed < 60.0) {
                if (!timerRunning && accTimeFinal === 0.0) { timerStart = new Date(); timerRunning = true; }
                if (timerRunning) { let currentDuration = (new Date() - timerStart) / 1000; accTimerDisplay.innerText = currentDuration.toFixed(2) + "ث"; }
            } else if (speed >= 60.0) {
                if (timerRunning) { accTimeFinal = (new Date() - timerStart) / 1000; timerRunning = false; accTimerDisplay.innerText = accTimeFinal.toFixed(2) + "ث 🏆"; }
            }
            if (speed === 0.0 && !timerRunning) { timerStart = null; accTimeFinal = 0.0; }
            if (speed < 50.0) { document.documentElement.style.setProperty('--dynamic-ring', '#39ff14'); }
            else if (speed >= 50.0 && speed < 90.0) { document.documentElement.style.setProperty('--dynamic-ring', '#ffaa00'); }
            else { document.documentElement.style.setProperty('--dynamic-ring', '#ff0055'); }
            if (speed > maxSpeed) { maxSpeed = speed; topSpeedDisplay.innerText = maxSpeed.toFixed(1); }
            odometerDisplay.innerText = totalDistance.toFixed(3);
            let rotation = -120 + (Math.min(speed, 180) / 180) * 240; needle.style.transform = `rotate(${rotation}deg)`;
            lastLat = lat; lastLon = lon; lastTime = time;
        }
        function toggleHUD() {
            document.body.classList.toggle('hud-mode');
            const btn = document.getElementById('hudToggle');
            btn.innerText = document.body.classList.contains('hud-mode') ? "تعطيل وضع الزجاج HUD" : "تفعيل وضع الزجاج الأمامي HUD";
        }
        function changeTheme(color, glow) { document.documentElement.style.setProperty('--neon-color', color); document.documentElement.style.setProperty('--neon-glow', glow); }
        function calculateDistance(lat1, lon1, lat2, lon2) {
            const R = 6371; const dLat = (lat2 - lat1) * Math.PI / 180; const dLon = (lon2 - lon1) * Math.PI / 180;
            const a = Math.sin(dLat/2) * Math.sin(dLat/2) + Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * Math.sin(dLon/2) * Math.sin(dLon/2);
            return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
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
