from mailer import Mailer, Message

def send_mail(event_subjec, event_url, event_text):
    sender = Mailer('smtp.gmail.com', use_tls=True, port=587)
    sender.login("zgztecnologica@gmail.com", "nopenopenope")
    message = Message(From="ztecnologica@gmail.com", To="me@davidfrancos.net", Subject=event_subject)
    message.Html = event_text + " <a href=\"" + event_url + "\">Mas informacion</a>"
    sender.send(message)

