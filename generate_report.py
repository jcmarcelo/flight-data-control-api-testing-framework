import subprocess
import json
import os
from datetime import datetime

def run_tests():
    result = subprocess.run(
        ["python", "-m", "pytest", "tests/", "-v", "--json-report", "--json-report-file=reports/results.json"],
        capture_output=True, text=True
    )
    return result

def generate_html(data):
    tests = data.get("tests", [])
    total = len(tests)
    passed = sum(1 for t in tests if t["outcome"] == "passed")
    failed = total - passed
    duration = round(data.get("duration", 0), 2)
    timestamp = datetime.now().strftime("%d %b %Y · %H:%M:%S")
    badge_en = "ALL PASSING" if failed == 0 else f"{failed} FAILED"
    badge_es = "TODO EXITOSO" if failed == 0 else f"{failed} FALLIDAS"
    badge_color = "#C9973A" if failed == 0 else "#C0392B"
    progress = round((passed / total) * 100) if total > 0 else 0

    rows = ""
    for t in tests:
        name = t["nodeid"].split("::")[-1]
        module = t["nodeid"].split("/")[-1].split("::")[0]
        outcome = t["outcome"]
        dur = round(t.get("call", {}).get("duration", 0) * 1000)
        dur_str = f"{dur}ms" if dur < 1000 else f"{round(dur/1000, 2)}s"
        dot_class = "dot-pass" if outcome == "passed" else "dot-fail"
        status_class = "status-pass" if outcome == "passed" else "status-fail"
        label_en = "Passed" if outcome == "passed" else "Failed"
        label_es = "Exitoso" if outcome == "passed" else "Fallido"
        rows += f"""
        <tr>
          <td><div class="test-name">{name}</div></td>
          <td><div class="test-module">{module}</div></td>
          <td>
            <span class="status-dot {status_class}">
              <span class="dot {dot_class}"></span>
              <span data-en="{label_en}" data-es="{label_es}">{label_en}</span>
            </span>
          </td>
          <td><span class="duration">{dur_str}</span></td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Flight Data and Control API Test Report</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'DM Sans', sans-serif; background: #fff; color: #1a1a1a; }}
  .dashboard {{ max-width: 860px; margin: 0 auto; padding: 2rem 1.5rem; }}

  .header {{ border-bottom: 2px solid #C9973A; padding-bottom: 1.5rem; margin-bottom: 2rem; display: flex; justify-content: space-between; align-items: flex-end; }}
  .header-left h1 {{ font-family: 'Playfair Display', serif; font-size: 26px; font-weight: 600; color: #1a1a1a; letter-spacing: -0.5px; }}
  .header-left p {{ font-size: 13px; color: #888; margin-top: 4px; }}
  .header-right {{ display: flex; align-items: center; gap: 10px; }}

  .badge {{ background: {badge_color}; color: #fff; font-size: 11px; font-weight: 500; padding: 4px 12px; border-radius: 20px; letter-spacing: 0.5px; }}
  .lang-btn {{ background: #fff; border: 1px solid #C9973A; color: #C9973A; font-size: 11px; font-weight: 500; padding: 4px 12px; border-radius: 20px; cursor: pointer; letter-spacing: 0.5px; font-family: 'DM Sans', sans-serif; transition: all 0.2s; }}
  .lang-btn:hover {{ background: #C9973A; color: #fff; }}

  .metrics {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 2rem; }}
  .metric {{ background: #fafafa; border: 1px solid #e8e8e8; border-radius: 10px; padding: 1rem 1.25rem; position: relative; overflow: hidden; }}
  .metric::before {{ content: ''; position: absolute; top: 0; left: 0; width: 3px; height: 100%; }}
  .metric.total::before {{ background: #1a1a1a; }}
  .metric.passed::before {{ background: #C9973A; }}
  .metric.failed::before {{ background: #C0392B; }}
  .metric.time::before {{ background: #888; }}
  .metric-label {{ font-size: 11px; color: #999; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; }}
  .metric-value {{ font-size: 28px; font-weight: 300; color: #1a1a1a; }}
  .metric.passed .metric-value {{ color: #C9973A; }}
  .metric.failed .metric-value {{ color: #C0392B; }}

  .progress-bar {{ background: #f0f0f0; border-radius: 4px; height: 6px; margin-bottom: 2rem; }}
  .progress-fill {{ height: 100%; border-radius: 4px; background: #C9973A; width: {progress}%; }}

  .section-title {{ font-family: 'Playfair Display', serif; font-size: 16px; font-weight: 500; color: #1a1a1a; margin-bottom: 1rem; padding-bottom: 8px; border-bottom: 1px solid #f0f0f0; }}

  .test-table {{ width: 100%; border-collapse: collapse; }}
  .test-table th {{ font-size: 11px; text-transform: uppercase; letter-spacing: 0.8px; color: #999; text-align: left; padding: 8px 12px; border-bottom: 1px solid #e8e8e8; }}
  .test-table td {{ padding: 10px 12px; font-size: 13px; border-bottom: 1px solid #f5f5f5; vertical-align: middle; }}
  .test-table tr:last-child td {{ border-bottom: none; }}
  .test-table tr:hover td {{ background: #fafafa; }}

  .test-name {{ font-family: monospace; font-size: 12px; color: #444; }}
  .test-module {{ font-size: 11px; color: #aaa; margin-top: 2px; }}
  .status-dot {{ display: inline-flex; align-items: center; gap: 6px; font-size: 12px; font-weight: 500; }}
  .dot {{ width: 7px; height: 7px; border-radius: 50%; }}
  .dot-pass {{ background: #C9973A; }}
  .dot-fail {{ background: #C0392B; }}
  .status-pass {{ color: #C9973A; }}
  .status-fail {{ color: #C0392B; }}
  .duration {{ font-size: 12px; color: #aaa; font-variant-numeric: tabular-nums; }}

  .footer {{ margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #f0f0f0; display: flex; justify-content: space-between; align-items: center; }}
  .footer-text {{ font-size: 11px; color: #bbb; }}
  .footer-brand {{ font-family: 'Playfair Display', serif; font-size: 13px; color: #C9973A; }}
</style>
</head>
<body>
<div class="dashboard">

  <div class="header">
    <div class="header-left">
      <h1>Flight Data and Control API Test Report</h1>
      <p> {timestamp}</p>
    </div>
    <div class="header-right">
      <button class="lang-btn" onclick="toggleLang()" id="langBtn">🌐 ES</button>
      <span class="badge" id="badge">{badge_en}</span>
    </div>
  </div>

  <div class="metrics">
    <div class="metric total">
      <div class="metric-label" data-en="Total Tests" data-es="Total Pruebas">Total Tests</div>
      <div class="metric-value">{total}</div>
    </div>
    <div class="metric passed">
      <div class="metric-label" data-en="Passed" data-es="Exitosas">Passed</div>
      <div class="metric-value">{passed}</div>
    </div>
    <div class="metric failed">
      <div class="metric-label" data-en="Failed" data-es="Fallidas">Failed</div>
      <div class="metric-value">{failed}</div>
    </div>
    <div class="metric time">
      <div class="metric-label" data-en="Duration" data-es="Duración">Duration</div>
      <div class="metric-value">{duration}s</div>
    </div>
  </div>

  <div class="progress-bar"><div class="progress-fill"></div></div>

  <p class="section-title" data-en="Test Results" data-es="Resultados de Pruebas">Test Results</p>

  <table class="test-table">
    <thead>
      <tr>
        <th data-en="Test" data-es="Prueba">Test</th>
        <th data-en="Module" data-es="Módulo">Module</th>
        <th data-en="Status" data-es="Estado">Status</th>
        <th data-en="Duration" data-es="Duración">Duration</th>
      </tr>
    </thead>
    <tbody>
      {rows}
    </tbody>
  </table>

  <div class="footer">
    <span class="footer-text" data-en="Author jcmarcelo" data-es=" Author jcmarcelo">
      Author jcmarcelo · 
    </span>
    <span class="footer-brand">Flight Data and Control API Test Report</span>
  </div>

</div>

<script>
  let lang = 'en';
  const badge_en = "{badge_en}";
  const badge_es = "{badge_es}";

  function toggleLang() {{
    lang = lang === 'en' ? 'es' : 'en';
    document.getElementById('langBtn').textContent = lang === 'en' ? '🌐 ES' : '🌐 EN';
    document.getElementById('badge').textContent = lang === 'en' ? badge_en : badge_es;
    document.querySelectorAll('[data-en]').forEach(el => {{
      el.textContent = lang === 'en' ? el.dataset.en : el.dataset.es;
    }});
  }}
</script>

</body>
</html>"""
    return html


if __name__ == "__main__":
    os.makedirs("reports", exist_ok=True)
    print("Running tests...")
    run_tests()

    with open("reports/results.json", encoding="utf-8") as f:
        data = json.load(f)

    html = generate_html(data)

    with open("reports/report.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Report generated: reports/report.html")
