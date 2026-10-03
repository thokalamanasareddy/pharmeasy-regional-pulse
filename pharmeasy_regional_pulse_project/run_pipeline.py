"""Run the complete data-to-review pipeline in sequence."""
import subprocess
import sys

STAGES = [
    "generate_dataset.py",
    "clean_data.py",
    "build_db.py",
    "queries.py",
    "metrics_engine.py",
    "draft_report.py",
    "review_gate.py",
]
for stage in STAGES:
    print(f"\\n=== {stage} ===", flush=True)
    subprocess.run([sys.executable, stage], check=True)
print("\\nPipeline complete. Start the dashboard with: streamlit run app.py")
