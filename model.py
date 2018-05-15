"""This is tables file for all"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


##############################################################################
# Model definitions

class Applicant(db.Model):
    """Applicant form data. This is how we can persist data in database"""

    __tablename__ = "applicants"

    _id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(20),nullable=False)
    date_applied = db.Column(db.DateTime, nullable=False, index=True)
    status = db.Column(db.String(64), nullable=False)
    
   
    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<Applicant Name ={} {} email={} id={} status={}>".format(self.first_name, \
                self.last_name, self.email, self._id, self.status)



##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///instacart_shoppers'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # us in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
    db.create_all()