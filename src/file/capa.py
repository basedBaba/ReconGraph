import json
import subprocess
import traceback

def capa(file):
    print(f"[INFO] Running CAPA on: {file}")

    try:
        result = subprocess.run(
            ["capa", file, "-r", "./capa-rules", "-j", "-s", "./capa-sigs"],
            capture_output=True,
            text=True,
            check=False
        )
        if result.stderr:
            print(f"[DEBUG] CAPA stderr:\n{result.stderr}")

        if not result.stdout or not result.stdout.strip():
            return {"error": "No output from CAPA command"}
        try:
            results = json.loads(result.stdout)
        except json.JSONDecodeError:
            print("[ERROR] Failed to parse CAPA output as JSON")
            print(f"[DEBUG] Raw stdout that failed parsing:\n{result.stdout}")
            return {"error": "Failed to parse CAPA output as JSON"}

        if "rules" not in results:
            print("[WARN] 'rules' not found in CAPA output")
            return {"error": "No rules found in analysis results"}
        
        print(f"[INFO] results loaded with {len(results['rules'])} rules")

        matched_rules = sum(1 for rule in results["rules"].values() if rule.get("matches"))
        print(f"[INFO] Total rules matched: {matched_rules}")

        results_dict = {}

        for rule, rule_data in results["rules"].items():
            if not rule_data.get("matches"):
                continue

            attack_data = rule_data.get("meta", {}).get("attack", [])
            rule_meta = rule_data.get("meta", {})
            rule_namespace = rule_meta.get("namespace", "")
            rule_scope = rule_meta.get("scope", "")

            rule_description = f"Rule: {rule}"
            if rule_namespace:
                rule_description += f" | Namespace: {rule_namespace}"
            if rule_scope:
                rule_description += f" | Scope: {rule_scope}"

            for attack in attack_data:
                if not isinstance(attack, dict):
                    continue

                tactic = attack.get("tactic")
                technique = attack.get("technique")
                mitre_id = attack.get("id")

                if not (tactic and technique and mitre_id):
                    continue

                technique_desc = f"{technique} [{mitre_id}]"
                technique_url = f"https://attack.mitre.org/techniques/{mitre_id.replace('.', '/')}"

                if tactic not in results_dict:
                    results_dict[tactic] = []

                existing_technique = next(
                    (tech for tech in results_dict[tactic] 
                     if tech["techniqueName"] == technique_desc), 
                    None
                )
                
                if existing_technique:
                    existing_technique["description"] += f"\n• {rule_description}"
                else:
                    results_dict[tactic].append({
                        "techniqueName": technique_desc,
                        "url": technique_url,
                        "description": rule_description
                    })

        if results_dict:
            print(f"[INFO] MITRE ATT&CK techniques extracted: {results_dict}")
            return results_dict

        print("[INFO] No MITRE ATT&CK techniques matched.")
        return {
            "info": "Analysis completed successfully but no MITRE ATT&CK techniques found",
            "rules_matched": matched_rules
        }

    except Exception as e:
        print("[ERROR] Unexpected exception occurred during CAPA run")
        traceback.print_exc()
        return {"error": f"Unexpected error: {str(e)}"}