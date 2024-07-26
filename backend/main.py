from flask import request, jsonify, abort
from config import app, db
from models import Contact


@app.route("/contacts", methods = ["GET"])
def det_contacts():
  contacts = Contact.query.all()
  contacts_in_json = list(map(lambda x: x.to_json(), contacts))

  return jsonify({"contacts": contacts_in_json}), 200


@app.route("/create_contact", methods = ["POST"])
def create_contact():
  first_name = request.json.get("firstName")
  last_name = request.json.get("lastName")
  email = request.json.get("email")

  if not first_name or not last_name or not email:
    return jsonify({"message": "complete mo"})
  new_contacts = Contact(first_name = first_name, last_name = last_name, email = email)

  try:
    db.session.add(new_contacts)
    db.session.commit()
  except Exception as e:
    return  jsonify({"message:": {e}})
  return jsonify({"message": "contact created"}), 201

@app.route("/edit_contact/<int:user_id>", methods = ["PATCH"])
def edit_contact(user_id):
  contact = Contact.query.get(user_id)

  if not contact:
    return jsonify({"message":"contacts not found"}), 404
  
  contact.first_name = request.json.get("firstName", contact.first_name)
  contact.last_name = request.json.get("lastName", contact.last_name)
  contact.email = request.json.get("email", contact.email)

  db.session.commit()

  return jsonify({"message": "contact edited"})

@app.route("/delete_contact/<int:user_id>", methods = ["DELETE"])
def delete_contact(user_id):
  contact = Contact.query.get(user_id)

  if not contact:
    return jsonify({"message": "contacts not found"}), 404
  
  db.session.delete(contact)
  db.session.commit()

  return jsonify({"message": "contact deleted"})








  


  

if __name__ == "__main__":
  with app.app_context():
    db.create_all()
  app.run(debug=True)