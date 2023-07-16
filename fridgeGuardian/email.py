from envelopes import Envelope, SMTP


class Email:
    def __init__(self,
                 smtp_address: str,
                 smtp_port: int,
                 login: str,
                 password: str,
                 tls: bool,
                 from_email: str,
                 from_name: str):
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
        self.from_email = from_email
        self.from_name = from_name

    def send(self, envelope: Envelope):
        """
        Sends an email

        :param envelope: Envelope containing the email to send
        """
        self.smtp.send(envelope)

    def build_envelope(self,
                       subject: str,
                       message: str,
                       dest_addr: str,
                       dest_name: str) -> Envelope:
        return Envelope(from_addr=(self.from_email, self.from_name),
                        to_addr=(dest_addr, dest_name),
                        subject=subject,
                        text_body=message)
