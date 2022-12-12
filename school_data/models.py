from school_data import db


class Teaching(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)

    group = db.relationship('Group', back_populates='teachingS')
    subject = db.relationship('Subject', back_populates='teachingS')
    teacher = db.relationship('Teacher', back_populates='teachingS')


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4), nullable=False, unique=True)

    students = db.relationship('Student', backref='group')

    teachingS = db.relationship('Teaching', back_populates='group')

    def __repr__(self):
        return f"{self.name}"


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)

    teachingS = db.relationship('Teaching', back_populates='teacher')

    def __repr__(self):
        return f"{self.name} {self.surname}"


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)

    def __repr__(self):
        return f"{self.name} {self.surname}"


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

    teachingS = db.relationship('Teaching', back_populates='subject')

    def __repr__(self):
        return f"{self.name}"
