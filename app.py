"""Flask app for Cupcakes"""

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "secret"

from models import db, connect_db, Cupcake

connect_db(app)


def serialize_cupcake(cupcake):
    """Serialize a cupcake SQLAlchemy obj into a dictionary for JSON."""

    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }


# ******************
#    APP ROUTING
# ******************

@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("index.html")


# ******************
#    API ROUTING
# ******************

@app.route("/api/cupcakes")
def all_cupcakes():
    """Get and return JSON for all cupcakes."""

    cupcakes = Cupcake.query.all()
    serialized_cupcakes = [serialize_cupcake(cup) for cup in cupcakes]

    return jsonify(cupcakes=serialized_cupcakes)


@app.route("/api/cupcakes/<int:cupcake_id>")
def cupcake_info(cupcake_id):
    """Get and return JSON about one cupcake."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    
    return jsonify(cupcake=serialize_cupcake(cupcake))


@app.route("/api/cupcakes", methods=["POST"])
def add_cupcake():
    """Create cupcake from data and return it."""

    # flavor = request.json["flavor"]
    # size = request.json["size"]
    # rating = request.json["rating"]
    # image = request.json["image"]

    # new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    
    data = request.json 

    new_cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized_cupcake = serialize_cupcake(new_cupcake)

    return ( jsonify(cupcake=serialized_cupcake), 201 )


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Updates a cupcake and responds with JSON of that cupcake."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.add(cupcake)
    db.session.commit()

    serialized_cupcake = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized_cupcake)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Deletes a certain cupcake, responds with JSON confirmation message."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")