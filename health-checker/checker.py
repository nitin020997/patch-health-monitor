import os
import json
import requests
from datetime import datetime

SERVERS = os.getenv("SERVERS", "appwin01,appwin02,appwin03").split(",")

def check_server(server_name):
    result = {
        "server": server_name,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "reachable": False,
        "domain_joined": False,
        "domain_name": None,
        "cpu_usage": None,
        "memory_usage": None,
        "status": "UNKNOWN",
        "issues": []
    }

    try:
        # Check if server is reachable
        response = requests.get(f"http://{server_name}/ping", timeout=3)
        result["reachable"] = response.status_code == 200

        # Get full health status
        health = requests.get(f"http://{server_name}/health", timeout=3).json()

        result["domain_joined"] = health["domain_joined"]
        result["domain_name"] = health["domain_name"]
        result["cpu_usage"] = health["cpu_usage"]
        result["memory_usage"] = health["memory_usage"]

        # Check for issues
        if not health["domain_joined"]:
            result["issues"].append("🚨 CRITICAL: Server dropped from AD domain")

        if health["cpu_usage"] > 85:
            result["issues"].append(f"⚠️  HIGH CPU: {health['cpu_usage']}%")

        if health["memory_usage"] > 85:
            result["issues"].append(f"⚠️  HIGH MEMORY: {health['memory_usage']}%")

        result["status"] = "CRITICAL" if result["issues"] else "HEALTHY"

    except Exception as e:
        result["reachable"] = False
        result["status"] = "UNREACHABLE"
        result["issues"].append(f"🚨 Server unreachable: {str(e)}")

    return result

def run_checks():
    print(f"\n{'='*50}")
    print(f"  NBFC Patch Health Monitor")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")

    results = []
    for server in SERVERS:
        print(f"Checking {server.upper()}...")
        result = check_server(server)
        results.append(result)

        # Print result
        status_icon = "✅" if result["status"] == "HEALTHY" else "❌"
        print(f"  {status_icon} Status: {result['status']}")
        print(f"  🌐 Reachable: {result['reachable']}")
        print(f"  🏢 Domain Joined: {result['domain_joined']}")
        if result["cpu_usage"]:
            print(f"  🖥️  CPU: {result['cpu_usage']}%")
        if result["memory_usage"]:
            print(f"  💾 Memory: {result['memory_usage']}%")
        if result["issues"]:
            print(f"  Issues:")
            for issue in result["issues"]:
                print(f"    → {issue}")
        print()

    # Save results to JSON
    with open("/app/reports/health_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"{'='*50}")
    total = len(results)
    healthy = len([r for r in results if r["status"] == "HEALTHY"])
    critical = len([r for r in results if r["status"] == "CRITICAL"])
    print(f"  SUMMARY: {healthy}/{total} healthy | {critical} critical")
    print(f"{'='*50}\n")

    return results

if __name__ == "__main__":
    run_checks()