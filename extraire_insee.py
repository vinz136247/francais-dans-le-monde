import csv
import json
import os

dossier = "data/insee_extrait"

fichier_data = os.path.join(
    dossier,
    "DS_RP_TD_NAT_AGESEX_PRINC_2023_data.csv"
)

fichier_meta = os.path.join(
    dossier,
    "DS_RP_TD_NAT_AGESEX_PRINC_2023_metadata.csv"
)

# Récupération des noms des communes
communes = {}

with open(fichier_meta, encoding="utf-8-sig", newline="") as f:
    lecteur = csv.DictReader(f, delimiter=";")
    for ligne in lecteur:
        if (ligne["COD_VAR"] == "GEO"
                and ligne["GEO_OBJECT"] == "COM"):
            communes[ligne["COD_MOD"]] = ligne["LIB_MOD"]

resultats = []

# Extraction des Français, tous âges et tous sexes
with open(fichier_data, encoding="utf-8-sig", newline="") as f:
    lecteur = csv.DictReader(f, delimiter=";")

    for ligne in lecteur:
        if (
            ligne["GEO_OBJECT"] == "COM"
            and ligne["NATIONALITY_TYPE"] == "250"
            and ligne["AGE"] == "_T"
            and ligne["SEX"] == "_T"
            and ligne["RP_MEASURE"] == "POP"
            and ligne["TIME_PERIOD"] == "2023"
        ):
            code = ligne["GEO"]
            valeur = ligne["OBS_VALUE"]

            if code in communes and valeur:
                resultats.append({
                    "code": code,
                    "commune": communes[code],
                    "population_francaise": round(float(valeur))
                })

resultats.sort(key=lambda x: x["code"])

os.makedirs("data/processed", exist_ok=True)

sortie = "data/processed/communes-france-2023.json"

with open(sortie, "w", encoding="utf-8") as f:
    json.dump({
        "source": "INSEE",
        "annee": 2023,
        "nationalite": "Française",
        "resultats": resultats
    }, f, ensure_ascii=False)

print("Extraction terminée !")
print("Nombre de communes :", len(resultats))
print("Fichier créé :", sortie)
print("Exemples :")

for commune in resultats[:5]:
    print(commune)
