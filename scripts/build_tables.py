#!/usr/bin/env python3
import os
import shutil
import datetime
import yaml

def backup_file(file_path):
    """If file_path exists, move it to a backup with a timestamp appended."""
    if os.path.exists(file_path):
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        backup_path = f"{file_path}_backup_{timestamp}"
        shutil.move(file_path, backup_path)
        print(f"Backed up {file_path} to {backup_path}")

def load_pvs(ioc_folder):
    """
    Load PVs from an IOC folder.
    Looks for a file named 'pvs.yaml' (YAML list) or 'pvs.txt' (one PV per line).
    Returns a list of PV names.
    """
    pvs = []
    pvs_yaml = os.path.join(ioc_folder, "pvs.yaml")
    pvs_txt = os.path.join(ioc_folder, "pvs.txt")
    if os.path.exists(pvs_yaml):
        try:
            with open(pvs_yaml, 'r') as f:
                pvs = yaml.safe_load(f)
                if not isinstance(pvs, list):
                    print(f"Warning: {pvs_yaml} does not contain a list.")
                    pvs = []
        except Exception as e:
            print(f"Error reading {pvs_yaml}: {e}")
    elif os.path.exists(pvs_txt):
        try:
            with open(pvs_txt, 'r') as f:
                pvs = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"Error reading {pvs_txt}: {e}")
    return pvs

def main():
    base_dir = os.getcwd()
    iocs_dir = os.path.join(base_dir, "IOCs")
    documents_dir = os.path.join(base_dir, "Documents")

    # Define file paths for the tables.
    ioc_table_file = os.path.join(documents_dir, "IOC_table.yaml")
    pv_table_file = os.path.join(documents_dir, "PV_table.yaml")

    # Backup old tables if they exist.
    backup_file(ioc_table_file)
    backup_file(pv_table_file)

    ioc_table = []
    pv_table = []

    if not os.path.isdir(iocs_dir):
        print(f"Error: IOCs folder not found at {iocs_dir}")
        return

    # Iterate over each IOC subdirectory.
    for entry in os.listdir(iocs_dir):
        entry_path = os.path.join(iocs_dir, entry)
        if os.path.isdir(entry_path):
            ioc_name = entry
            pvs = load_pvs(entry_path)
            ioc_entry = {
                "ioc_name": ioc_name,
                "path": os.path.relpath(entry_path, base_dir),
                "num_pvs": len(pvs)
            }
            ioc_table.append(ioc_entry)
            # Build PV table entries: one record per PV.
            for pv in pvs:
                pv_table.append({
                    "ioc": ioc_name,
                    "pv": pv
                })

    # Write the IOC table.
    try:
        with open(ioc_table_file, 'w') as f:
            yaml.dump(ioc_table, f, default_flow_style=False)
        print(f"IOC table written to {ioc_table_file}")
    except Exception as e:
        print(f"Error writing IOC table: {e}")

    # Write the PV table.
    try:
        with open(pv_table_file, 'w') as f:
            yaml.dump(pv_table, f, default_flow_style=False)
        print(f"PV table written to {pv_table_file}")
    except Exception as e:
        print(f"Error writing PV table: {e}")

if __name__ == "__main__":
    main()
