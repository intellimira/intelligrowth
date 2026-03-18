#!/usr/bin/env python3
"""
MIRA + OpenJarvis Telemetry Dashboard
Simple script to display inference metrics
"""

import subprocess
import json
import os


def run_query_with_profile(query: str) -> dict:
    """Run query and capture profiling data"""
    cmd = ["uv", "run", "jarvis", "ask", "--profile", "--no-stream", query]

    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd="/home/sir-v/OpenJarvis"
    )

    return {"query": query, "output": result.stdout, "exit_code": result.returncode}


def display_metrics(result: dict):
    """Display metrics from query result"""
    print(f"\n{'=' * 60}")
    print(f"QUERY: {result['query']}")
    print(f"{'=' * 60}")
    print(result["output"])


def main():
    print("MIRA + OpenJarvis Telemetry Dashboard")
    print("=" * 40)

    # Run test queries
    queries = [
        "What is 2 + 2?",
        "List 3 programming languages",
    ]

    for query in queries:
        result = run_query_with_profile(query)
        if result["exit_code"] == 0:
            display_metrics(result)


if __name__ == "__main__":
    main()
