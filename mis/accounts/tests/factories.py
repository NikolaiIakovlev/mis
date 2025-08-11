import factory
from django.contrib.auth.hashers import make_password
from accounts.models import User, Doctor, Patient

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    password = make_password('testpass123')
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    role = 'patient'

    @factory.post_generation
    def set_role(self, create, extracted, **kwargs):
        if extracted:
            self.role = extracted

class DoctorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Doctor

    user = factory.SubFactory(UserFactory, role='doctor')
    first_name = 'Doctor'
    last_name = 'Test'
    specialization = 'General Practitioner'

class PatientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Patient

    user = factory.SubFactory(UserFactory, role='patient')
    first_name = 'Patient'
    last_name = 'Test'
    phonenumber = '+79991234567'