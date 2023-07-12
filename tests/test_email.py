from fridgeGuardian.email import Email
from envelopes import Envelope
from pytest import fixture

@fixture
def email():
    email = Email(smtp_address='smtp_address',
                  smtp_port=587,
                  login='login',
                  password='password',
                  tls=True)

    assert email.smtp._host == 'smtp_address'
    assert email.smtp._port == 587
    assert email.smtp._login == 'login'
    assert email.smtp._password == 'password'
    assert email.smtp._timeout == 10

def test_constructor(email):
    pass

def test_send(email):
    envelope = Envelope(to_addr=(u'test@test.com', u'Name Familly_name'),
                        from_addr=(u'noreply@test.com', u'Fridge Guardian'),
                        subject=u'Test',
                        html_body=u"This is a test")
    email.send(envelope)
