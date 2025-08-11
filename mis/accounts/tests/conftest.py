import pytest
from factories import UserFactory, DoctorFactory, PatientFactory


@pytest.fixture
def admin_factory():
    """Фабрика для создания администратора."""
    def _admin_factory(**kwargs):
        return UserFactory(role='admin', **kwargs)
    return _admin_factory


@pytest.fixture
def doctor_factory():
    """Фабрика для создания доктора."""
    return DoctorFactory


@pytest.fixture
def patient_factory():
    """Фабрика для создания пациента."""
    return PatientFactory
