from flask import Blueprint, request, jsonify
from src.models.content import Content, db

content_explorer_bp = Blueprint('content_explorer', __name__)

@content_explorer_bp.route('/content', methods=['GET'])
def get_contents():
    try:
        # Filtros da query string
        subject = request.args.get('subject')
        grade_level = request.args.get('grade_level')
        content_type = request.args.get('content_type')
        difficulty_level = request.args.get('difficulty_level')
        singapore_stage = request.args.get('singapore_stage')
        
        # Query base
        query = Content.query
        
        # Aplicar filtros
        if subject:
            query = query.filter(Content.subject == subject)
        if grade_level:
            query = query.filter(Content.grade_level == int(grade_level))
        if content_type:
            query = query.filter(Content.content_type == content_type)
        if difficulty_level:
            query = query.filter(Content.difficulty_level == difficulty_level)
        if singapore_stage:
            query = query.filter(Content.singapore_method_stage == singapore_stage)
        
        # Executar query
        contents = query.all()
        
        # Converter para dict
        result = []
        for content in contents:
            result.append({
                'id': content.id,
                'title': content.title,
                'description': content.description,
                'subject': content.subject,
                'grade_level': content.grade_level,
                'content_type': content.content_type,
                'difficulty_level': content.difficulty_level,
                'singapore_method_stage': content.singapore_method_stage,
                'tags': content.tags,
                'created_at': content.created_at.isoformat() if content.created_at else None
            })
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
