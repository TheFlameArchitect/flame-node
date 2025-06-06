import json, os
from datetime import datetime, timezone
from core.memory import generate_mirror_id
from core.pulse import fetch_pulse
import typer

CONFIG_PATH = ".mirrorconfig.json"
BURNBACK_PATH = "rituals/burnback.json"

def detect_hostile_conditions(burnback_config):
    """Detect actual hostile conditions, not just trigger presence."""
    hostile_conditions = []
    
    # Check for hostile fork indicators
    if "hostile_fork" in burnback_config.get("triggers", []):
        # Check if critical files have been stripped or corrupted
        required_files = ["README.md", "Codex/Codex_Charter.md", "LICENSE"]
        for file_path in required_files:
            if not os.path.exists(file_path):
                hostile_conditions.append("hostile_fork")
                break
        
        # Check if LICENSE has been replaced with generic content
        try:
            with open("LICENSE", "r") as f:
                license_content = f.read()
                if "Flame Codex License" not in license_content:
                    hostile_conditions.append("hostile_fork")
        except:
            hostile_conditions.append("hostile_fork")
    
    # Add other hostile condition checks here as needed
    
    return hostile_conditions

def run_mirror():
    config = json.load(open(CONFIG_PATH))
    burnback = json.load(open(BURNBACK_PATH))

    # Check for actual hostile conditions
    if burnback.get("active"):
        hostile_conditions = detect_hostile_conditions(burnback)
        if hostile_conditions:
            print("🔥 Mirror Burnback Triggered — Access Revoked.")
            print(f"   Detected: {', '.join(hostile_conditions)}")
            raise typer.Exit()

    if config["mirror_id"] == "auto_generate_on_first_run":
        config["mirror_id"] = generate_mirror_id()
        config["created_at"] = datetime.now(timezone.utc).isoformat()
        json.dump(config, open(CONFIG_PATH, "w"), indent=2)
        print(f"🧬 Mirror ID assigned: {config['mirror_id']}")

    # Parse expiration date and compare with current UTC time
    expiry_date = datetime.fromisoformat(config["mirror_expires"].replace('Z', '+00:00'))
    current_time = datetime.now(timezone.utc)
    
    if current_time > expiry_date:
        print("⛔ Mirror expired. Seek renewal through Flame.")
        raise typer.Exit()

    if config.get("flame_link"):
        fetch_pulse(config["flame_link"])
    
    print("🔥 MirrorNode active. Begin memory ritual.") 