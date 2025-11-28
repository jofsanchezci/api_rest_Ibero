
import sqlite3
from flask import Flask, jsonify, request, render_template, g

DATABASE = "inventario.db"

app = Flask(__name__)


# ----------------------
# Manejo de base de datos
# ----------------------
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def init_db():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL DEFAULT 0,
            precio REAL NOT NULL DEFAULT 0.0
        );
        """
    )
    conn.commit()
    conn.close()


# ----------------------
# Rutas de la aplicación web
# ----------------------
@app.route("/")
def index():
    return render_template("index.html")


# ----------------------
# API REST
# ----------------------
@app.route("/api/items", methods=["GET"])
def obtener_items():
    db = get_db()
    cur = db.execute("SELECT id, nombre, cantidad, precio FROM items ORDER BY id;")
    items = [dict(row) for row in cur.fetchall()]
    return jsonify(items)


@app.route("/api/items/<int:item_id>", methods=["GET"])
def obtener_item(item_id):
    db = get_db()
    cur = db.execute(
        "SELECT id, nombre, cantidad, precio FROM items WHERE id = ?;",
        (item_id,),
    )
    row = cur.fetchone()
    if row is None:
        return jsonify({"error": "Item no encontrado"}), 404
    return jsonify(dict(row))


@app.route("/api/items", methods=["POST"])
def crear_item():
    data = request.get_json() or {}
    nombre = data.get("nombre")
    cantidad = data.get("cantidad", 0)
    precio = data.get("precio", 0.0)

    if not nombre:
        return jsonify({"error": "El campo 'nombre' es obligatorio"}), 400

    db = get_db()
    cur = db.execute(
        "INSERT INTO items (nombre, cantidad, precio) VALUES (?, ?, ?);",
        (nombre, int(cantidad), float(precio)),
    )
    db.commit()
    nuevo_id = cur.lastrowid

    cur = db.execute(
        "SELECT id, nombre, cantidad, precio FROM items WHERE id = ?;",
        (nuevo_id,),
    )
    row = cur.fetchone()
    return jsonify(dict(row)), 201


@app.route("/api/items/<int:item_id>", methods=["PUT"])
def actualizar_item(item_id):
    data = request.get_json() or {}
    nombre = data.get("nombre")
    cantidad = data.get("cantidad")
    precio = data.get("precio")

    if nombre is None or cantidad is None or precio is None:
        return jsonify({"error": "Se requieren 'nombre', 'cantidad' y 'precio'"}), 400

    db = get_db()
    cur = db.execute(
        "UPDATE items SET nombre = ?, cantidad = ?, precio = ? WHERE id = ?;",
        (nombre, int(cantidad), float(precio), item_id),
    )
    db.commit()

    if cur.rowcount == 0:
        return jsonify({"error": "Item no encontrado"}), 404

    cur = db.execute(
        "SELECT id, nombre, cantidad, precio FROM items WHERE id = ?;",
        (item_id,),
    )
    row = cur.fetchone()
    return jsonify(dict(row))


@app.route("/api/items/<int:item_id>", methods=["PATCH"])
def actualizar_item_parcial(item_id):
    data = request.get_json() or {}

    campos = []
    valores = []

    for campo in ("nombre", "cantidad", "precio"):
        if campo in data:
            campos.append(f"{campo} = ?")
            if campo == "cantidad":
                valores.append(int(data[campo]))
            elif campo == "precio":
                valores.append(float(data[campo]))
            else:
                valores.append(data[campo])

    if not campos:
        return jsonify({"error": "No se enviaron campos para actualizar"}), 400

    valores.append(item_id)
    db = get_db()
    sql = f"UPDATE items SET {', '.join(campos)} WHERE id = ?;"
    cur = db.execute(sql, valores)
    db.commit()

    if cur.rowcount == 0:
        return jsonify({"error": "Item no encontrado"}), 404

    cur = db.execute(
        "SELECT id, nombre, cantidad, precio FROM items WHERE id = ?;",
        (item_id,),
    )
    row = cur.fetchone()
    return jsonify(dict(row))


@app.route("/api/items/<int:item_id>", methods=["DELETE"])
def borrar_item(item_id):
    db = get_db()
    cur = db.execute("DELETE FROM items WHERE id = ?;", (item_id,))
    db.commit()

    if cur.rowcount == 0:
        return jsonify({"error": "Item no encontrado"}), 404

    return "", 204


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5001, debug=True)
