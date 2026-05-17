import ssl
from django.core.mail.backends.smtp import EmailBackend as DjangoSMTPBackend


class Py312SMTPBackend(DjangoSMTPBackend):
    """SMTP backend compatibile con Python 3.12, evita keyfile/certfile."""

    def open(self):
        if self.connection:
            return False

        connection_params = {}
        if self.timeout is not None:
            connection_params["timeout"] = self.timeout
        if self.use_ssl:
            connection_params["context"] = ssl.create_default_context()

        try:
            self.connection = self.connection_class(
                self.host, self.port, **connection_params
            )
            if not self.use_ssl and self.use_tls:
                self.connection.starttls(context=ssl.create_default_context())
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except OSError:
            if not self.fail_silently:
                raise