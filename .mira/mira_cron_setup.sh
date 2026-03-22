#!/bin/bash
# MIRA Continuous Learning Cron Setup
# Run: bash .mira/mira_cron_setup.sh

MIRA_DIR="/home/sir-v/MiRA"
CONTINUOUS_LEARNING="$MIRA_DIR/Memory_Mesh/continuous_learning.py"
LOG_FILE="$MIRA_DIR/Memory_Mesh/cron.log"

echo "Setting up MIRA continuous learning cron..."

# Add cron job to run every 4 hours
CRON_JOB="0 */4 * * * cd $MIRA_DIR && python3 $CONTINUOUS_LEARNING >> $LOG_FILE 2>&1"

# Check if already installed
if crontab -l 2>/dev/null | grep -q "continuous_learning.py"; then
    echo "Cron job already installed"
else
    # Add to crontab
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "Cron job installed: Runs every 4 hours"
fi

echo ""
echo "Current crontab:"
crontab -l | grep -i mira || echo "No MIRA cron jobs"

echo ""
echo "Log file: $LOG_FILE"
