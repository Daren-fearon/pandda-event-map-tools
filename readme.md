# Extract PanDDA event map

Created by: Daren Fearon
Last edited time: May 22, 2025 10:02 PM
Last edited by: Daren Fearon

This guide walks you through a 3-step process to:

1. **Download PDB files** using a group deposition ID
2. **Extract PanDDA event maps** from structure factor CIF files
3. **Convert them to MTZ format** for crystallographic analysis

Scripts can be found at: /dls/science/groups/i04-1/software/scripts/event_map_extractor/

---

# **🧾 Step 1: Download PDB Files**

### **📄 Script: `batch_download.sh`**

### **✅ Purpose:**

Downloads various file types (e.g., `.cif.gz`, `.pdb.gz`, `.sf.cif.gz`) from the RCSB PDB using a list of PDB IDs and decompresses files.

---

### **🔍 How to Get PDB IDs from a Group Deposition**

1. Go to [https://www.rcsb.org](https://www.rcsb.org)
2. Search for your **Group Deposition ID** (e.g., `G_1001234`)
3. Select `Tabular Report Entry IDs` and click `Download IDs`
    
4. Save this file in your working directory e.g. as `G_1001234.txt`
    
    ```
    1ABC,2XYZ,3DEF
    ```
    
5. Alternatively you can manually populate the text file

---

### **▶️ Usage:**

`/dls/science/groups/i04-1/software/scripts/event_map_extractor/batch_download.sh -f input_PDB_ids.txt -o output_dir -c -s`

### **🔤 Options:**

| **Flag** | **Description** |
| --- | --- |
| `-f <file>` | Input file with comma-separated PDB IDs |
| `-o <dir>` | Output directory (default: current directory) |
| `-c` | Download `.cif.gz` files |
| `-s` | Download `-sf.cif.gz` files (structure factors) |

---

### **🛠️ Example:**

`/dls/science/groups/i04-1/software/scripts/event_map_extractor/batch_download.sh -f G_1001234.txt -o G_1001234 -c -s`

This downloads `.cif.gz` and `-sf.cif.gz` files and decompresses them into `./G_1001234`.

---

# **🧪 Step 2: Extract PanDDA Event Maps**

### **📄 Script: `extract_pandda_event`**

### **✅ Purpose:**

Loads the Phenix environment and runs a Python script to extract PanDDA event maps from `*-sf.cif` files. These can be from PDB download or manually curated cif files.

---

### **▶️ Usage:**

`/dls/science/groups/i04-1/software/scripts/event_map_extractor/extract_pandda_event [space_group=XXX] <file1-sf.cif> [<file2-sf.cif> ...]`

Notes: 

- `[space_group=XXX]` is optional and should only be necessary when converting event maps to `P1`
- Wildcard `*-sf.cif` can be used to extract maps from all files within directory.

### **🛠️ Example:**

`/dls/science/groups/i04-1/software/scripts/event_map_extractor/extract_pandda_event G_1001234/*-sf.cif`

This will:

- Load the `phenix` module
- Run the Python script to split and convert the CIF into MTZ files

---

# **🧠 Step 3: Python Script – `pandda_event_extractor.py`**

### **✅ Purpose:**

Handles the core logic:

- Splits CIF files into:
    - `_data.cif` (reference/original data)
    - `_pandda_event.cif` (PanDDA event map)
- Converts both to `.mtz` using `phenix.cif_as_mtz`
- Best part is, you don’t have to do anything here.

---

### **🧩 Features:**

- Automatically detects data blocks (`sf`, `Asf`, `Bsf`)
- Supports optional space group override
- Uses `subprocess` to run Phenix commands
- Logs progress and errors

---

# **📦 Output Summary**

After running the full workflow, you will have:

- `_data.mtz`: MTZ file from reference/original data
- `_pandda_event.mtz`: MTZ file from PanDDA event map

These files are ready for downstream  visualization.