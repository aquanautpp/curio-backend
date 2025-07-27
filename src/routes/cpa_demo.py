# src/routes/cpa_demo.py
from flask import Blueprint, jsonify
from src.models.content import Content

cpa_demo_bp = Blueprint('cpa_demo', __name__)

@cpa_demo_bp.route('/cpa-demo/<int:grade_level>', methods=['GET'])
def cpa_demo(grade_level):
    """Retorna conteúdo de matemática separado por estágios CPA para o nível escolar informado."""
    math_content = Content.query.filter_by(
        subject='Mathematics',
        grade_level=grade_level,
        is_active=True
    ).all()

    def get_stage(stage_name):
        return [c.to_dict() for c in math_content if c.singapore_method_stage == stage_name]

    return jsonify({
        'grade_level': grade_level,
        'stages': {
            'concrete': get_stage('concrete'),
            'pictorial': get_stage('pictorial'),
            'abstract': get_stage('abstract')
        }
    })
