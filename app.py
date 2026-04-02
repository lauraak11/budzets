from flask import Flask, render_template, request, redirect
import csv
from datetime import datetime

app = Flask(__name__)
dati = []

# ====== PALĪGFUNKCIJAS ======
def saglabat_csv():
    with open("dati.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for ier in dati:
            writer.writerow([
                ier["tips"],
                ier["summa"],
                ier["apraksts"],
                ier["datums"],
                ier["fav"]
            ])

def ieladet_csv():
    try:
        with open("dati.csv", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for r in reader:
                dati.append({
                    "tips": r[0],
                    "summa": float(r[1]),
                    "apraksts": r[2],
                    "datums": r[3],
                    "fav": r[4] == "True"
                })
    except:
        pass

def bilance():
    ien = sum(i["summa"] for i in dati if i["tips"] == "Ienākums")
    izd = sum(i["summa"] for i in dati if i["tips"] == "Izdevums")
    return round(ien - izd, 2)

def procenti():
    ien = sum(i["summa"] for i in dati if i["tips"] == "Ienākums")
    izd = sum(i["summa"] for i in dati if i["tips"] == "Izdevums")

    if ien == 0:
        return 0

    return round(((ien - izd) / ien) * 100, 2)

# ====== MARŠRUTI ======
@app.route('/')
def index():
    filtrs = request.args.get("filtrs")

    if filtrs == "Svarīgākie":
        filtr_dati = [i for i in dati if i["fav"]]
    elif filtrs:
        filtr_dati = [i for i in dati if i["tips"] == filtrs]
    else:
        filtr_dati = dati

    return render_template("index.html", dati=filtr_dati, bilance=bilance())

@app.route('/pievienot', methods=['POST'])
def pievienot():
    try:
        ieraksts = {
            "tips": request.form['tips'],
            "summa": float(request.form['summa']),
            "apraksts": request.form['apraksts'],
            "datums": datetime.now().strftime("%Y-%m-%d"),
            "fav": False
        }

        dati.append(ieraksts)
        saglabat_csv()

    except:
        print("Kļūda!")

    return redirect('/')

@app.route('/dzest/<int:id>')
def dzest(id):
    if 0 <= id < len(dati):
        dati.pop(id)
        saglabat_csv()
    return redirect('/')

@app.route('/fav/<int:id>')
def fav(id):
    if 0 <= id < len(dati):
        dati[id]["fav"] = not dati[id]["fav"]
        saglabat_csv()
    return redirect('/')

@app.route('/bilance')
def bilance_lapa():
    return render_template(
        "bilance.html",
        bilance=bilance(),
        proc=procenti()
    )

# ====== START ======
ieladet_csv()
app.run(debug=True)