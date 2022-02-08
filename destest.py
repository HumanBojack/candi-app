from App.models import Candidacy, User
from App import db




#print(Candidacy.query.join(Users).with_entities(Candidacy.*, Users.first_name).first())

print(Candidacy.query.join(User).with_entities(User.first_name,Candidacy.entreprise, Candidacy.contact_full_name, Candidacy.contact_email, Candidacy.contact_mobilephone,Candidacy.date,Candidacy.status).all())