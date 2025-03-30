import sqlite3
import re
import os
import xml.etree.ElementTree as ET
from flask import Flask, request, send_file, jsonify
from flask_restx import Api, Resource, fields
from flask_cors import CORS

# Flask app setup
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)  # Enable CORS for all routes
api = Api(app, title="PWG API", description="Search 'key' and 'data' separately using regex with AND condition")

# Updated SQLite database file and table name
DB_FILE = "temp_pwg_10.sqlite"
TABLE_NAME = "temp_pwg_10"
XSLT_FILE = "transform.xsl"
ABS_XML_FILE = "abs.xml"

# Define the response model for API documentation
result_model = api.model('Result', {
    'key': fields.String(),
    'lnum': fields.Integer(),
    'data': fields.String()
})

@api.route('/search')
class SearchAPI(Resource):
    @api.doc(params={
        'key_query': 'Regex pattern to search in key',
        'data_query': 'Regex pattern to search in data'
    })
    def get(self):
        """Search 'key' and 'data' columns with regex, ensuring both match if both are provided"""
        key_pattern = request.args.get('key_query', '')
        data_pattern = request.args.get('data_query', '')

        if not key_pattern and not data_pattern:
            return jsonify({"message": "At least one query parameter ('key_query' or 'data_query') is required"}), 400

        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()

            # Fetch all records from the table
            cursor.execute(f"SELECT key, lnum, data FROM {TABLE_NAME}")
            rows = cursor.fetchall()

            # Compile regex patterns (if provided)
            key_regex = re.compile(key_pattern) if key_pattern else None
            data_regex = re.compile(data_pattern) if data_pattern else None

            # Filter rows based on provided regex patterns (AND condition)
            matches = [
                {"key": row[0], "lnum": row[1], "data": row[2]} 
                for row in rows 
                if (not key_regex or key_regex.search(row[0])) and (not data_regex or data_regex.search(row[2]))
            ]

            conn.close()
            return jsonify(matches)

        except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500

@api.route('/xslt')
class XSLTFileAPI(Resource):
    @api.doc(description="Serve the transform.xslt file")
    def get(self):
        """Serve the transform.xslt file"""
        if os.path.exists(XSLT_FILE):
            return send_file(XSLT_FILE, mimetype='application/xml')
        else:
            return jsonify({"error": "XSLT file not found"}), 404

@api.route('/abs')
class ABSFileAPI(Resource):
    @api.doc(description="Serve abs.xml as JSON")
    def get(self):
        """Parse abs.xml and return JSON with 'ss' as key and 'link' as value"""
        if not os.path.exists(ABS_XML_FILE):
            return jsonify({"error": "ABS XML file not found"}), 404

        try:
            tree = ET.parse(ABS_XML_FILE)
            root = tree.getroot()
            abs_data = {lsd.find('ss').text: lsd.find('link').text for lsd in root.findall('lsd')}
            return jsonify(abs_data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
