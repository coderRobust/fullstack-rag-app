import os
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from alembic.config import Config
from alembic import command

def run_migrations():
    """Run database migrations."""
    # Get the path to the alembic.ini file
    alembic_ini = Path(__file__).parent.parent / "alembic.ini"
    
    # Create Alembic configuration
    alembic_cfg = Config(str(alembic_ini))
    
    # Run the migration
    command.upgrade(alembic_cfg, "head")

if __name__ == "__main__":
    run_migrations() 