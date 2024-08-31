from flask import Blueprint, render_template

agent_bp = Blueprint('agent', __name__)

@agent_bp.route('/agent_dashboard')
def agent_dashboard():
    return render_template('agent_page.html')
