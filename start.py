#!/usr/bin/env python3.12
import subprocess
import sys
import time
import os

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(root_dir, "backend")
    frontend_dir = os.path.join(root_dir, "frontend")
    
    print("Starting HybridETL application...")
    print()
    
    # Start backend
    print("Starting backend (port 8000)...")
    backend_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--reload"],
        cwd=backend_dir
    )
    
    time.sleep(2)
    
    # Start frontend
    print("Starting frontend (port 3000)...")
    frontend_proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", "3000"],
        cwd=frontend_dir
    )
    
    print()
    print("=" * 50)
    print("Servers running!")
    print("=" * 50)
    print("Frontend:  http://localhost:3000")
    print("Backend:   http://localhost:8000")
    print("API Docs:  http://localhost:8000/docs")
    print("=" * 50)
    print("Press Ctrl+C to stop both servers")
    print("=" * 50)
    
    try:
        backend_proc.wait()
        frontend_proc.wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
        backend_proc.terminate()
        frontend_proc.terminate()
        backend_proc.wait()
        frontend_proc.wait()
        print("Done!")

if __name__ == "__main__":
    main()
