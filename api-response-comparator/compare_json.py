import json
import argparse
import sys

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {file_path}: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
        sys.exit(2)

def compare_json(old, new, path=""):
    diffs = []
    
    same_type = type(old) is type(new)
    is_old_number = isinstance(old, (int, float)) and not isinstance(old, bool)
    is_new_number = isinstance(new, (int, float)) and not isinstance(new, bool)
    
    if not same_type and not (is_old_number and is_new_number):
        diffs.append(f"{path if path else 'root'}: changed from {json.dumps(old)} to {json.dumps(new)}")
        return diffs

    if isinstance(old, dict):
        old_keys = set(old.keys())
        new_keys = set(new.keys())
        
        removed = old_keys - new_keys
        added = new_keys - old_keys
        common = old_keys & new_keys
        
        for k in sorted(removed):
            p = f"{path}.{k}" if path else k
            diffs.append(f"{p}: removed (was {json.dumps(old[k])})")
            
        for k in sorted(added):
            p = f"{path}.{k}" if path else k
            diffs.append(f"{p}: added with value {json.dumps(new[k])}")
            
        for k in sorted(common):
            p = f"{path}.{k}" if path else k
            diffs.extend(compare_json(old[k], new[k], p))
            
    elif isinstance(old, list):
        max_len = max(len(old), len(new))
        for i in range(max_len):
            p = f"{path}[{i}]" if path else f"[{i}]"
            if i < len(old) and i < len(new):
                diffs.extend(compare_json(old[i], new[i], p))
            elif i < len(old):
                diffs.append(f"{p}: removed (was {json.dumps(old[i])})")
            else:
                diffs.append(f"{p}: added with value {json.dumps(new[i])}")
    else:
        if old != new:
            diffs.append(f"{path if path else 'root'}: changed from {json.dumps(old)} to {json.dumps(new)}")
            
    return diffs

def main():
    parser = argparse.ArgumentParser(description="Compare two JSON files and report the differences.")
    parser.add_argument("old_json", help="Path to the first (old) JSON file")
    parser.add_argument("new_json", help="Path to the second (new) JSON file")
    args = parser.parse_args()

    old_data = load_json(args.old_json)
    new_data = load_json(args.new_json)

    differences = compare_json(old_data, new_data)

    if not differences:
        print("No differences found. The JSON files are identical.")
        sys.exit(0)
    else:
        print("Differences found:")
        for diff in differences:
            print(f"- {diff}")
        sys.exit(1)

if __name__ == "__main__":
    main()
