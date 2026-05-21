#!/usr/bin/env python3
"""
Self-Healing: Classifies failure types and suggests recovery action
"""

import sys

def classify_failure(log_text):
    log = log_text.lower()
    
    if "timeout" in log or "connection refused" in log or "network" in log:
        return "NETWORK_ERROR", "RETRY"
    elif "random" in log or "flaky" in log or "intermittent" in log:
        return "FLAKY_TEST", "RETRY"
    elif "syntax error" in log or "compilation failed" in log or "nameerror" in log:
        return "CODE_ERROR", "ALERT_ONLY"
    elif "cannot connect to docker" in log or "docker daemon" in log:
        return "DOCKER_ERROR", "RETRY"
    elif "exit code 137" in log or "out of memory" in log:
        return "OOM_ERROR", "RETRY_WITH_MORE_MEMORY"
    elif "health check failed" in log or "unhealthy" in log:
        return "HEALTH_FAILURE", "RESTART"
    else:
        return "UNKNOWN", "ALERT_ONLY"

if __name__ == "__main__":
    log = sys.stdin.read()
    failure_type, action = classify_failure(log)
    print(f"FAILURE_TYPE={failure_type}")
    print(f"RECOMMENDED_ACTION={action}")