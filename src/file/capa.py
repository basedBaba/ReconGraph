import json
import os


def capa(file):
    os.system(f"./capa/dist/capa {file} -j > results.json")

    results = {}

    try:
        with open("results.json", "r", encoding="utf-8") as file:
            results = json.load(file)

        mitre = []

        for rule in results["rules"]:
            description = results["rules"][rule]["source"]

            if "att&ck" in description:
                lines = description.splitlines()

                for i, line in enumerate(lines):
                    if line.strip().startswith("att&ck:"):
                        attack_content = lines[i + 1].strip("- ").strip()
                        mitre.append(attack_content)
                        break

        unique_mitre = []
        seen = set()

        for attack in mitre:
            if attack not in seen:
                unique_mitre.append(attack)
                seen.add(attack)

        unique_mitre.sort()

        results = {}

        for attack in unique_mitre:
            parts = attack.split("::", 1)

            key = parts[0]
            value = parts[1]

            technique = value.split()[-1]
            technique = technique.strip("[]")
            technique = technique.replace(".", "/")

            link = f"https://attack.mitre.org/techniques/{technique}"

            if key not in results:
                results[key] = []

            results[key].append({value: link})

        if results:
            return results

        return {"error": "analysis did not yield any result for the given file"}
    except:
        return {"error": "unsupported file format"}
