from flask import Blueprint, jsonify

bp = Blueprint('routes', __name__)

# Example transactions endpoint
@bp.route('/api/transactions', methods=['GET'])
def get_transactions():
    data = [
        {"id": 1, "date": "2025-09-28", "amount": 120.50, "category": "Food"},
        {"id": 2, "date": "2025-09-27", "amount": 75.00, "category": "Transport"},
        {"id": 3, "date": "2025-09-26", "amount": 200.00, "category": "Rent"}
    ]
    return jsonify(data)