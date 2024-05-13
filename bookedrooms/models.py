from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rooms.models import RoomCategory
from django.db import models
from django.urls import reverse
from datetime import date, datetime, time


class BookedRoom(models.Model):
    STATUS_CHOICES = [  # Choix pour le statut de la réservation
        ('pending', 'En attente'),
        ('canceled', 'Annulé'),
        ('validated', 'Validé'),
    ]

    LABORATORY_CHOICES = [  # Choix pour les groupes de laboratoire
        ('CReSTIC', 'CReSTIC'),
        ('Labi*', 'Labi*'),
        ('Liciis', 'Liciis'),
    ]

    date = models.DateField()  # Date de la réservation
    startTime = models.TimeField()  # Heure de début de la réservation
    endTime = models.TimeField()  # Heure de fin de la réservation
    groups = models.CharField(max_length=100, choices=LABORATORY_CHOICES)  # Groupe de laboratoire
    status = models.CharField(max_length=100, choices=STATUS_CHOICES,
                              default=STATUS_CHOICES[0][0])  # Statut de la réservation
    motif = models.CharField(max_length=100)  # Motif de la réservation
    peopleAmount = models.IntegerField(default=1)  # Nombre de personnes
    user = models.ForeignKey(  # Utilisateur associé à la réservation
        get_user_model(),  # Utilisation de la fonction get_user_model pour obtenir le modèle utilisateur personnalisé
        on_delete=models.CASCADE,  # Suppression en cascade de l'utilisateur si celui-ci est supprimé

    )
    room_category = models.ForeignKey(  # Catégorie de salle réservée
        RoomCategory,  # Utilisation du modèle RoomCategory pour les catégories de salles
        on_delete=models.CASCADE,  # Suppression en cascade de la catégorie de salle si celle-ci est supprimée
    )

    def clean(self):
        # Vérification de la validité de la date et de l'heure de début
        selected_date = self.date
        if selected_date < date.today():  # Si la date est antérieure à aujourd'hui
            raise ValidationError('Vous ne pouvez pas changer la date pour une date antérieure à aujourd\'hui.')

        start_time = self.startTime
        if start_time:
            # Vérification de l'heure de début dans les plages horaires autorisées
            if start_time < time(8, 0) or start_time > time(18, 0):
                raise ValidationError('L\'heure de début doit être entre 8h00 et 18h00.')

            # Vérification de l'heure de début pour la même journée
            if selected_date == date.today():
                current_time = datetime.now().time()
                new_hour = current_time.hour + 1
                new_minute = current_time.minute + 30
                if new_minute >= 60:
                    new_hour += 1
                    new_minute -= 60
                min_start_time = time(new_hour, new_minute)
                if start_time <= min_start_time:
                    raise ValidationError('L\'heure de début doit être supérieure à 1h30 de l\'heure actuelle.')

        end_time = self.endTime
        if end_time:
            # Vérification de l'heure de fin dans les plages horaires autorisées
            if end_time < time(8, 0) or end_time > time(18, 0):
                raise ValidationError('L\'heure de fin doit être entre 8h00 et 18h00.')
            if end_time <= start_time:
                raise ValidationError('L\'heure de fin doit être supérieure à l\'heure de début.')

        # Ajout de la condition pour le samedi après 12h30 et le dimanche
        if selected_date.weekday() == 5:  # Samedi (0 = lundi, 6 = dimanche)
            if start_time >= time(12, 30):
                raise ValidationError('Aucune réservation possible le samedi après 12h30.')
        elif selected_date.weekday() == 6:  # Dimanche
            raise ValidationError('Aucune réservation possible le dimanche.')

    def get_absolute_url(self):
        # Renvoie l'URL absolue de l'objet BookedRoom, utilisée pour les redirections après une création ou une
        # modification
        return reverse('bookedrooms_detail', args=[str(self.id)])

    def __str__(self):
        # Renvoie une représentation en chaîne de caractères de l'objet BookedRoom, utilisée notamment dans
        # l'interface d'administration Django
        return self.room_category.libRoom + " |  " + self.user.username
