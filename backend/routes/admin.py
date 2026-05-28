from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required
from backend.middleware.auth_middleware import require_role
from backend.models.user import User
from backend.models.specialty import Specialty
from backend.models.permission import Permission
from backend.database import db
from werkzeug.security import generate_password_hash

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
@login_required
@require_role('superadmin')
def require_superadmin():
    pass

@admin_bp.route('/')
def dashboard():
    users_count = User.query.count()
    specialties_count = Specialty.query.count()
    return render_template('admin/dashboard.html', 
                           users_count=users_count, 
                           specialties_count=specialties_count)

@admin_bp.route('/users', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'create':
            username = request.form.get('username')
            password = request.form.get('password')
            full_name = request.form.get('full_name')
            specialty_id = request.form.get('specialty_id')
            
            if User.query.filter_by(username=username).first():
                flash('El nombre de usuario ya existe.', 'danger')
            else:
                user = User(
                    username=username,
                    password_hash=generate_password_hash(password),
                    full_name=full_name,
                    specialty_id=specialty_id,
                    role='specialty'
                )
                db.session.add(user)
                db.session.commit()
                flash('Usuario creado exitosamente.', 'success')
                
        elif action == 'delete':
            user_id = request.form.get('user_id')
            user = User.query.get_or_404(user_id)
            if user.role != 'superadmin':
                db.session.delete(user)
                db.session.commit()
                flash('Usuario eliminado.', 'success')

    users = User.query.filter_by(role='specialty').all()
    specialties = Specialty.query.all()
    return render_template('admin/users.html', users=users, specialties=specialties)

@admin_bp.route('/users/change_password', methods=['POST'])
def change_password():
    user_id = request.form.get('user_id')
    new_password = request.form.get('new_password')
    
    user = User.query.get_or_404(user_id)
    if new_password:
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Contraseña actualizada correctamente.'})
    
    return jsonify({'success': False, 'message': 'La contraseña no puede estar vacía.'}), 400

@admin_bp.route('/permissions', methods=['GET', 'POST'])
def manage_permissions():
    if request.method == 'POST':
        specialty_id = request.form.get('specialty_id')
        perm = Permission.query.filter_by(specialty_id=specialty_id).first()
        
        if perm:
            perm.can_create = 'can_create' in request.form
            perm.can_edit = 'can_edit' in request.form
            perm.can_delete = 'can_delete' in request.form
            db.session.commit()
            flash('Permisos actualizados.', 'success')

    permissions = Permission.query.all()
    return render_template('admin/permissions.html', permissions=permissions)
