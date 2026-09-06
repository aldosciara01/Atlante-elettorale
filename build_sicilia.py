"""Costruisce data/sicilia.json: proiezione delle regionali siciliane 2027 per provincia e per circoscrizione di Palermo."""
import json, math
from shapely.geometry import shape, mapping

U = [f for f in json.load(open("data/unita.json"))["features"] if f["properties"]["region"] == "Sicilia"]

# scenario regionale (liste, % stimata a livello regionale) e coalizioni
LISTS = {
 "FdI":("Fratelli d'Italia","CDX",15.0), "FI":("Forza Italia","CDX",13.0), "DC":("DC – Grande Sicilia","CDX",6.5), "Lega":("Lega – Prima l'Italia","CDX",4.0),
 "M5S":("Movimento 5 Stelle","CL",12.5), "PD":("Partito Democratico","CL",11.5), "CC":("Controcorrente","CL",8.0), "AVS":("Alleanza Verdi e Sinistra","CL",3.0), "RIF":("Riformisti (IV, +E, Azione)","CL",2.0),
 "SCN":("Sud chiama Nord","SCN",11.0), "FN":("Futuro Nazionale","FN",6.0), "ALTRI":("Altre liste","ALTRI",7.5),
}
CAND = {"CDX":("Renato Schifani",38.0), "CL":("Ismaele La Vardera",38.5), "SCN":("Cateno De Luca",13.0), "FN":("candidato Futuro Nazionale",6.5), "ALTRI":("altri candidati",4.0)}
COALNAME = {"CDX":"Centrodestra","CL":"Campo largo","SCN":"Sud chiama Nord","FN":"Futuro Nazionale","ALTRI":"Altri"}
SEATS_PROV = {"Palermo":16,"Catania":13,"Messina":8,"Agrigento":6,"Trapani":5,"Siracusa":5,"Ragusa":4,"Caltanissetta":3,"Enna":2}
THRESHOLD = 5.0

def prov_of(p):
    n = p["name"]
    if p["kind"] == "prov": return n
    if p["city"] == "palermo": return "Palermo"
    if p["city"] == "messina": return "Messina"
    if p["city"] == "catania": return "Catania"
    raise ValueError(n)

def seed(p):
    b = p["b22"]; alt = b["Altri"]
    city = p["city"]; kind = p["kind"]
    scn_boost = 2.5 if city == "messina" else 1.0
    cc_boost = 1.6 if (city == "palermo" and kind == "muni") else (1.2 if city == "palermo" else 1.0)
    return {
        "FdI": b["FdI"], "FI": b["FI"], "DC": 0.5*b["NM"] + 0.35*alt + 0.12*b["FI"], "Lega": b["Lega"],
        "M5S": b["M5S"], "PD": b["PD"], "CC": (0.25*b["M5S"] + 0.2*b["AzIV"] + 0.15*alt)*cc_boost, "AVS": b["AVS"], "RIF": 0.6*b["AzIV"] + b["+E"],
        "SCN": (0.6*alt + 0.05*b["M5S"])*scn_boost, "FN": 0.5*b["Lega"] + 0.25*b["FdI"] + 0.3*min(alt,8), "ALTRI": 0.3*alt + 1.0,
    }

K = list(LISTS.keys()); T = {k: LISTS[k][2] for k in K}
P = [seed(f["properties"]) for f in U]; W = sum(f["properties"]["w"] for f in U)
for it in range(400):
    avg = {k: sum(P[i][k]*U[i]["properties"]["w"] for i in range(len(U)))/W for k in K}
    for p in P:
        for k in K: p[k] *= T[k]/avg[k]
        s = sum(p.values())
        for k in K: p[k] *= 100/s

ratio = {c: CAND[c][1]/sum(v for k,(n,cc,v) in LISTS.items() if cc == c) for c in CAND}
feats = []; provagg = {}
for f, p in zip(U, P):
    pr = f["properties"]
    coal = {c: sum(p[k] for k in K if LISTS[k][1] == c) for c in CAND}
    cand = {c: coal[c]*ratio[c] for c in CAND}
    s = sum(cand.values()); cand = {c: v*100/s for c,v in cand.items()}
    order = sorted([c for c in cand if c != "ALTRI"], key=lambda c: -cand[c])
    win, second = order[0], order[1]
    prov = prov_of(pr)
    pa = provagg.setdefault(prov, {"w":0, "p":{k:0 for k in K}})
    pa["w"] += pr["w"]
    for k in K: pa["p"][k] += p[k]*pr["w"]
    feats.append({"type":"Feature","properties":{
        "id":pr["id"],"name":pr["name"],"kind":pr["kind"],"city":pr["city"],"prov":prov,"w":pr["w"],
        "p":{k:round(v,1) for k,v in p.items()},"coal":{c:round(v,1) for c,v in coal.items()},"cand":{c:round(v,1) for c,v in cand.items()},
        "winner":win,"second":second,"margin":round(cand[win]-cand[second],1)},
        "geometry":f["geometry"]})

# seggi provinciali fra le liste sopra la soglia regionale
elig = [k for k in K if T[k] >= THRESHOLD and k != "ALTRI"]
seats_by_prov = {}; seats_tot = {k:0 for k in elig}
for prov, pa in provagg.items():
    share = {k: pa["p"][k]/pa["w"] for k in elig}; tot = sum(share.values()); n = SEATS_PROV[prov]
    q = {k: share[k]/tot*n for k in elig}; fl = {k: math.floor(q[k]) for k in elig}; rem = n - sum(fl.values())
    for k in sorted(elig, key=lambda k: -(q[k]-fl[k]))[:rem]: fl[k] += 1
    seats_by_prov[prov] = {"seats":fl, "p":{k: round(pa["p"][k]/pa["w"],1) for k in K}, "w":pa["w"]}
    for k in elig: seats_tot[k] += fl[k]
for f in feats:
    if f["properties"]["kind"] in ("prov","rest","city","muni"):
        f["properties"]["provseats"] = seats_by_prov[f["properties"]["prov"]]["seats"]
coal_seats = {c: sum(seats_tot[k] for k in elig if LISTS[k][1] == c) for c in ["CDX","CL","SCN","FN"]}
order = sorted(CAND, key=lambda c: -CAND[c][1]); coal_seats[order[0]] += 7; coal_seats[order[1]] += 1
summary = {"lists":{k:{"name":LISTS[k][0],"coal":LISTS[k][1],"pct":T[k],"seats":seats_tot.get(k)} for k in K},
           "cand":{c:{"name":CAND[c][0],"coal":COALNAME[c],"pct":CAND[c][1],"seats":coal_seats.get(c)} for c in CAND},
           "winner":order[0],"second":order[1],"threshold":THRESHOLD,"seatsProv":SEATS_PROV,"byProv":seats_by_prov,"updated":"6 settembre 2026"}
json.dump({"type":"FeatureCollection","summary":summary,"features":feats}, open("data/sicilia.json","w"), ensure_ascii=False, separators=(",",":"))
print("unità", len(feats)); print("seggi liste", seats_tot); print("coalizioni", coal_seats, sum(coal_seats.values()))
for f in feats:
    p=f["properties"]; print(f'{p["name"][:42]:42s} CL {p["cand"]["CL"]:5.1f} CDX {p["cand"]["CDX"]:5.1f} SCN {p["cand"]["SCN"]:5.1f} FN {p["cand"]["FN"]:4.1f} -> {p["winner"]} +{p["margin"]}')
for prov,d in seats_by_prov.items(): print(prov, d["seats"])
