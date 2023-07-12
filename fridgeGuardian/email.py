from envelopes import Envelope, SMTP


class Email:
    def __init__(self,
                 smtp_address: str,
                 smtp_port: int,
                 login: str,
                 password: str,
                 tls: bool):
        """
        Constructor of the Email class

        :param smtp_address: Address of the SMTP server
        :param login: Login to connect to the SMTP server
        :param password: Password to connect to the SMTP server
        :param tls: TLS encryption of
        """
        self.smtp: SMTP = SMTP(host=smtp_address,
                               port=smtp_port,
                               login=login,
                               password=password,
                               tls=tls,
                               timeout=10)

    def send(self, envelope: Envelope):
        """
        Sends an email

        :param envelope: Envelope containing the email to send
        """
        self.smtp.send(envelope)
