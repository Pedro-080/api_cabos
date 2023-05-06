from flask import Flask, jsonify

app = Flask(__name__)

class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species
        self.age = None

animal = Animal('Rex', 'Dog')

@app.route('/animal', methods=['GET'])
def get_animal():
    animal_dict = animal.__dict__
    return jsonify(animal_dict)

if __name__ == '__main__':
    app.run(debug=True)