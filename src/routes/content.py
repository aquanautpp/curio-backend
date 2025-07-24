from flask import Blueprint, jsonify, request
from src.models.content import Content, db
from sqlalchemy import and_, or_

content_bp = Blueprint('content', __name__)

@content_bp.route('/content', methods=['GET'])
def get_content():
    # Filtros opcionais
    subject = request.args.get('subject')
    grade_level = request.args.get('grade_level')
    content_type = request.args.get('content_type')
    difficulty_level = request.args.get('difficulty_level')
    singapore_stage = request.args.get('singapore_stage')
    
    query = Content.query.filter_by(is_active=True)
    
    if subject:
        query = query.filter(Content.subject == subject)
    if grade_level:
        query = query.filter(Content.grade_level == grade_level)
    if content_type:
        query = query.filter(Content.content_type == content_type)
    if difficulty_level:
        query = query.filter(Content.difficulty_level == difficulty_level)
    if singapore_stage:
        query = query.filter(Content.singapore_method_stage == singapore_stage)
    
    content_list = query.all()
    return jsonify([content.to_dict() for content in content_list])

@content_bp.route('/content', methods=['POST'])
def create_content():
    data = request.json
    
    content = Content(
        title=data['title'],
        description=data.get('description'),
        subject=data['subject'],
        grade_level=data['grade_level'],
        content_type=data['content_type'],
        difficulty_level=data['difficulty_level'],
        singapore_method_stage=data.get('singapore_method_stage'),
        content_data=data.get('content_data'),
        tags=','.join(data.get('tags', [])) if data.get('tags') else None,
        creator_id=data.get('creator_id')
    )
    
    db.session.add(content)
    db.session.commit()
    return jsonify(content.to_dict()), 201

@content_bp.route('/content/<int:content_id>', methods=['GET'])
def get_content_item(content_id):
    content = Content.query.get_or_404(content_id)
    return jsonify(content.to_dict())

@content_bp.route('/content/<int:content_id>', methods=['PUT'])
def update_content(content_id):
    content = Content.query.get_or_404(content_id)
    data = request.json
    
    content.title = data.get('title', content.title)
    content.description = data.get('description', content.description)
    content.subject = data.get('subject', content.subject)
    content.grade_level = data.get('grade_level', content.grade_level)
    content.content_type = data.get('content_type', content.content_type)
    content.difficulty_level = data.get('difficulty_level', content.difficulty_level)
    content.singapore_method_stage = data.get('singapore_method_stage', content.singapore_method_stage)
    content.content_data = data.get('content_data', content.content_data)
    content.is_active = data.get('is_active', content.is_active)
    
    if data.get('tags'):
        content.tags = ','.join(data['tags'])
    
    db.session.commit()
    return jsonify(content.to_dict())

@content_bp.route('/content/<int:content_id>', methods=['DELETE'])
def delete_content(content_id):
    content = Content.query.get_or_404(content_id)
    content.is_active = False  # Soft delete
    db.session.commit()
    return '', 204

@content_bp.route('/content/search', methods=['GET'])
def search_content():
    query_text = request.args.get('q', '')
    subject = request.args.get('subject')
    grade_level = request.args.get('grade_level')
    
    query = Content.query.filter_by(is_active=True)
    
    if query_text:
        query = query.filter(
            or_(
                Content.title.contains(query_text),
                Content.description.contains(query_text),
                Content.tags.contains(query_text)
            )
        )
    
    if subject:
        query = query.filter(Content.subject == subject)
    if grade_level:
        query = query.filter(Content.grade_level == grade_level)
    
    content_list = query.all()
    return jsonify([content.to_dict() for content in content_list])

@content_bp.route('/content/singapore-method/<stage>', methods=['GET'])
def get_singapore_method_content(stage):
    """Obter conteúdo específico do Método de Singapura por estágio"""
    valid_stages = ['concrete', 'pictorial', 'abstract']
    if stage not in valid_stages:
        return jsonify({'error': 'Invalid Singapore method stage'}), 400
    
    subject = request.args.get('subject', 'Mathematics')
    grade_level = request.args.get('grade_level')
    
    query = Content.query.filter(
        and_(
            Content.singapore_method_stage == stage,
            Content.subject == subject,
            Content.is_active == True
        )
    )
    
    if grade_level:
        query = query.filter(Content.grade_level == grade_level)
    
    content_list = query.all()
    return jsonify([content.to_dict() for content in content_list])

