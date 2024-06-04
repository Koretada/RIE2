import time
import socket
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
import email
from email.mime.text import MIMEText
import smtplib

# Informations de l'expéditeur
expediteur_nom = "Walid Rania"
expediteur_email = "walid@somethingeasy.xyz"
expediteur = f"{expediteur_nom} <{expediteur_email}>"
reply_to = expediteur_email  
destinataire = 'maciej.korczynski@univ-grenoble-alpes.fr'
mot_de_passe = 'abcdefgh'

message = MIMEMultipart('alternative')
message['From'] = expediteur
message['To'] = destinataire
message['Subject'] = 'On a oublier ça la dernière fois'
message['Date'] = email.utils.formatdate(localtime=True)
message.add_header('Reply-To', reply_to)

# Génération d'un Message-ID unique
hostname = socket.gethostname()
timestamp = time.time()
message_id = f"<{timestamp}.{socket.gethostbyname(hostname)}@{hostname}>"
message.add_header('Message-ID', message_id)

texte = "Bonjour, ceci est un test d'envoi d'email via le serveur SMTP."
html = """\
<html>
  <head></head>
  <body>
    <p>Bonjour,<br>
       Ceci est un <b>test</b> d'envoi d'email via le serveur SMTP.<br>
       Cordialement,<br>
       Walid et Rania RIE2 :)
    </p>
  </body>
</html>
"""

part1 = MIMEText(texte, 'plain')
part2 = MIMEText(html, 'html')
message.attach(part1)
message.attach(part2)

# Connexion et envoi du message
try:
    serveur = smtplib.SMTP('ssl0.ovh.net', 587)
    serveur.starttls()
    serveur.login('toto@walidr.fr', mot_de_passe)  # Utilise la bonne adresse expéditeur pour l'authentification
    serveur.sendmail(expediteur_email, destinataire, message.as_string())
    print("Email envoyé avec succès !")
except Exception as e:
    print(f"Erreur lors de l'envoi de l'email : {e}")
finally:
    serveur.quit()
