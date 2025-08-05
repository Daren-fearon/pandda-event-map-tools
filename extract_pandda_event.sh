#!/bin/bash

# Script: extract_pandda_event.sh
# Description:
#   Loads the Phenix environment, extracts PanDDA event maps from CIF files,
#   and converts them to MTZ format using a custom Python script.

# Usage:
#   ./extract_pandda_event [space_group=XXX] <file1-sf.cif> [<file2-sf.cif> ...]

# === Configuration ===
# If running externally to DLS then update this path
SCRIPT_PATH="/dls/science/groups/i04-1/software/scripts/event_map_extractor/pandda_event_extractor.py"

# === Check for required tools ===
if ! command -v module &> /dev/null; then
    echo "❌ 'module' command not found. Ensure the environment module system is available."
    exit 1
fi

if ! module avail phenix &> /dev/null; then
    echo "❌ 'phenix' module not found. Please ensure Phenix is installed and available via modules."
    exit 1
fi

# Load Phenix environment
module load phenix

# === Check arguments ===
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 [space_group=XXX] <file1-sf.cif> [<file2-sf.cif> ...]"
    exit 1
fi

# === Parse arguments ===
SPACE_GROUP=""
CIF_FILES=()

for arg in "$@"; do
    if [[ "$arg" == space_group=* ]]; then
        SPACE_GROUP="${arg#space_group=}"
    else
        CIF_FILES+=("$arg")
    fi
done

# === Validate Python script path ===
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "❌ Python script not found at: $SCRIPT_PATH"
    exit 1
fi

# === Check if any CIF files were provided ===
if [ "${#CIF_FILES[@]}" -eq 0 ]; then
    echo "❌ No CIF files provided."
    exit 1
fi

# === Run the Python script ===
echo "🔍 Extracting PanDDA event maps from ${#CIF_FILES[@]} CIF file(s)..."
echo "📁 Files: ${CIF_FILES[*]}"
if [ -n "$SPACE_GROUP" ]; then
    echo "🧭 Using space group: $SPACE_GROUP"
fi

python3 "$SCRIPT_PATH" "${CIF_FILES[@]}" ${SPACE_GROUP:+space_group="$SPACE_GROUP"}
