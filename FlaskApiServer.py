from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ======= MODELS =======
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(10), nullable=False)


# ======= ENDPOINTS =======

# Add student
@app.route('/students', methods=['POST'])
def add_student():
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Name is required'}), 400

    student = Student(name=name)
    db.session.add(student)
    db.session.commit()
    return jsonify({'message': 'Student added', 'id': student.id}), 201


# Update student
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.json
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    student.name = data.get('name', student.name)
    db.session.commit()
    return jsonify({'message': 'Student updated'}), 200


# Delete student
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    Attendance.query.filter_by(student_id=student_id).delete()
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student and related attendance deleted'}), 200


# Mark attendance
@app.route('/attendance', methods=['POST'])
def mark_attendance():
    data = request.json
    student_id = data.get('student_id')
    status = data.get('status', 'present').lower()
    att_date = data.get('date', date.today().isoformat())

    if status not in ['present', 'absent']:
        return jsonify({'error': 'Invalid status'}), 400

    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    existing = Attendance.query.filter_by(student_id=student_id, date=att_date).first()
    if existing:
        return jsonify({'error': 'Attendance already marked'}), 409

    attendance = Attendance(student_id=student_id, status=status, date=att_date)
    db.session.add(attendance)
    db.session.commit()
    return jsonify({'message': 'Attendance marked'}), 200


# Get all attendance
@app.route('/attendance', methods=['GET'])
def get_attendance():
    records = Attendance.query.all()
    result = []
    for record in records:
        student = Student.query.get(record.student_id)
        result.append({
            'id': record.id,
            'student_id': record.student_id,
            'student_name': student.name if student else 'Unknown',
            'date': record.date,
            'status': record.status
        })
    return jsonify(result), 200


# Update attendance
@app.route('/attendance', methods=['PUT'])
def update_attendance():
    data = request.json
    student_id = data.get('student_id')
    att_date = data.get('date')
    new_status = data.get('status', 'present').lower()

    if not student_id or not att_date:
        return jsonify({'error': 'student_id and date are required'}), 400

    record = Attendance.query.filter_by(student_id=student_id, date=att_date).first()
    if not record:
        return jsonify({'error': 'Attendance record not found'}), 404

    record.status = new_status
    db.session.commit()
    return jsonify({'message': 'Attendance updated'}), 200


# ======= RUN APP (Flask 3.x+ Compatible) =======
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
