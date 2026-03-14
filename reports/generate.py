import json
from datetime import datetime

def generate_report(input_file="reports/health_results.json",
                    output_file="reports/health_report.html"):

    with open(input_file) as f:
        servers = json.load(f)

    total = len(servers)
    healthy = len([s for s in servers if s["status"] == "HEALTHY"])
    critical = len([s for s in servers if s["status"] == "CRITICAL"])
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Build server rows
    rows = ""
    for s in servers:
        status_color = "#2ecc71" if s["status"] == "HEALTHY" else "#e74c3c"
        domain_icon = "✅" if s["domain_joined"] else "🚨 DROPPED"
        cpu_color = "red" if s["cpu_usage"] and s["cpu_usage"] > 85 else "black"
        mem_color = "red" if s["memory_usage"] and s["memory_usage"] > 85 else "black"
        issues_html = ""
        if s["issues"]:
            issues_html = "<ul>" + "".join(f"<li>{i}</li>" for i in s["issues"]) + "</ul>"
        else:
            issues_html = "<span style='color:green'>None</span>"

        rows += f"""
        <tr>
            <td><strong>{s["server"].upper()}</strong></td>
            <td>{s["timestamp"]}</td>
            <td>{"✅ Yes" if s["reachable"] else "❌ No"}</td>
            <td>{domain_icon}</td>
            <td style="color:{cpu_color}">{s["cpu_usage"]}%</td>
            <td style="color:{mem_color}">{s["memory_usage"]}%</td>
            <td style="background:{status_color};color:white;
                font-weight:bold;text-align:center">
                {s["status"]}
            </td>
            <td>{issues_html}</td>
        </tr>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>NBFC Patch Health Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
            .header {{ background: #2c3e50; color: white; padding: 20px;
                       border-radius: 8px; margin-bottom: 20px; }}
            .summary {{ display: flex; gap: 20px; margin-bottom: 20px; }}
            .card {{ padding: 20px; border-radius: 8px; color: white;
                     flex: 1; text-align: center; }}
            .card h2 {{ margin: 0; font-size: 2em; }}
            .card p {{ margin: 5px 0 0; }}
            .total {{ background: #2980b9; }}
            .healthy {{ background: #27ae60; }}
            .critical {{ background: #e74c3c; }}
            table {{ width: 100%; border-collapse: collapse;
                     background: white; border-radius: 8px;
                     overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
            th {{ background: #2c3e50; color: white; padding: 12px; text-align: left; }}
            td {{ padding: 12px; border-bottom: 1px solid #eee; }}
            tr:hover {{ background: #f9f9f9; }}
            .footer {{ margin-top: 20px; color: #888; font-size: 0.85em; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🏦 NBFC Post-Patch Health Report</h1>
            <p>Generated: {generated_at} | Domain: CORP.NBFC.LOCAL</p>
        </div>

        <div class="summary">
            <div class="card total">
                <h2>{total}</h2>
                <p>Total Servers</p>
            </div>
            <div class="card healthy">
                <h2>{healthy}</h2>
                <p>Healthy</p>
            </div>
            <div class="card critical">
                <h2>{critical}</h2>
                <p>Critical</p>
            </div>
        </div>

        <table>
            <thead>
                <tr>
                    <th>Server</th>
                    <th>Checked At</th>
                    <th>Reachable</th>
                    <th>Domain Status</th>
                    <th>CPU</th>
                    <th>Memory</th>
                    <th>Status</th>
                    <th>Issues</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>

        <div class="footer">
            <p>⚠️ This report is auto-generated post patch cycle.
               Please review critical servers immediately.</p>
            <p>🔒 Confidential — For internal use only | RBI Audit Reference</p>
        </div>
    </body>
    </html>
    """

    with open(output_file, "w") as f:
        f.write(html)

    print(f"✅ Report generated: {output_file}")

if __name__ == "__main__":
    generate_report()