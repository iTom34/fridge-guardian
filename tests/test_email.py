from fridgeGuardian.email import Email
from envelopes import Envelope
from pytest import fixture


@fixture
def email():
    email = Email(smtp_address='smtp_address',
                  smtp_port=587,
                  login='login',
                  password='password',
                  tls=True,
                  from_email="from@email.com",
                  from_name="From Name")

    assert email.smtp._host == 'smtp_address'
    assert email.smtp._port == 587
    assert email.smtp._login == 'login'
    assert email.smtp._password == 'password'
    assert email.smtp._timeout == 10
    return email


def test_constructor(email):
    pass


def test_send(email):
    envelope = Envelope(to_addr=(u'test@test.com', u'Name Familly_name'),
                        from_addr=(u'noreply@test.com', u'Fridge Guardian'),
                        subject=u'Test',
                        html_body=u"This is a test")
    email.send(envelope)


def test_build_envelope(email):
    envelope = email.build_envelope(message="message",
                                    subject="subject",
                                    dest_addr="dest@email.com",
                                    dest_name="Dest Name")
    assert envelope.from_addr == ('from@email.com', 'From Name')
    assert envelope.to_addr == [('dest@email.com', "Dest Name")]
    assert envelope._subject == "subject"
