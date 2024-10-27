from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TrashEmissions(db.Model):
    """Model to store trash-related emissions and suggestions."""
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each record
    emission_kg = db.Column(db.Float, nullable=False)  # Total emissions in kg CO2
    suggestions = db.Column(db.String(500), nullable=True)  # Suggestions for reduction
    services = db.Column(db.String(500), nullable=True)  # Local service recommendations

    def __repr__(self):
        return f"<TrashEmissions(id={self.id}, emission_kg={self.emission_kg})>"
