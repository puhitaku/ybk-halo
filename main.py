import pygame, json
from flask import Flask, request, Response, jsonify

fl = Flask(__name__)

@fl.route('/')
def index():
    x = request.args.get('x', type=float)
    y = request.args.get('y', type=float)
    z = request.args.get('z', type=float)
    
    return json.dumps([x, y, z])

def main():
    fl.run(debug=True)

if __name__ == '__main__':
    main()