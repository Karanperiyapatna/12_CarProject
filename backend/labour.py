from flask import Blueprint, render_template

labour_bp = Blueprint('labour', __name__)

@labour_bp.route('/labour_dashboard')
def labour_dashboard():
    return render_template('labour_page.html')
