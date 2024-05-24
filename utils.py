from django.core.mail import send_mail

from hotel_reservation_project import settings


# CREATION DE RESERVATION

def send_reservation_validated_email_admin(booked_room):
    """
    Envoie un mail qui confirme directement la réservation faite par l'admin
    """
    subject = 'Votre réservation a bien été ajoutée'
    message = f'Salle: {booked_room.room_category}\n' \
              f'Nombre de personnes: {booked_room.peopleAmount}\n' \
              f'Date: {booked_room.date}\n' \
              f'Heure de début: {booked_room.startTime}\n' \
              f'Heure de fin: {booked_room.endTime}\n' \
              f'Groupe/Laboratoire: {booked_room.groups}\n' \
              f'Motif: {booked_room.motif}\n'
    sender = 'à compléter avec l''adresse de l''expéditeur'
    recipient_list = settings.EMAIL_RECIPIENTS
    send_mail(subject, message, sender, recipient_list)


def send_reservation_confirmation_email_admin(booked_room):
    """
    Envoie un mail qui demande la confirmation de la réservation d'un utilisateur
    """
    subject = 'Nouvelle réservation en attente de validation'
    message = f'Une nouvelle réservation a été faite par {booked_room.user.first_name} {booked_room.user.last_name}.\n' \
              f'Salle: {booked_room.room_category}\n' \
              f'Nombre de personnes: {booked_room.peopleAmount}\n' \
              f'Date: {booked_room.date}\n' \
              f'Heure de début: {booked_room.startTime}\n' \
              f'Heure de fin: {booked_room.endTime}\n' \
              f'Groupe/Laboratoire: {booked_room.groups}\n' \
              f'Motif: {booked_room.motif}\n' \
              f'Veuillez valider ou refuser cette demande de réservation.'
    sender = 'à compléter avec l''adresse de l''expéditeur'
    recipient_list = settings.EMAIL_RECIPIENTS
    send_mail(subject, message, sender, recipient_list)


def send_reservation_confirmation_email_user(booked_room):
    """
    Envoie un mail qui atteste de la demande réservation d'un utilisateur
    """
    subject = 'Demande de réservation a bien été effectuée'
    message = f'Salle: {booked_room.room_category}\n' \
              f'Nombre de personnes: {booked_room.peopleAmount}\n' \
              f'Date: {booked_room.date}\n' \
              f'Heure de début: {booked_room.startTime}\n' \
              f'Heure de fin: {booked_room.endTime}\n' \
              f'Groupe/Laboratoire: {booked_room.groups}\n' \
              f'Motif: {booked_room.motif}\n' \
              f'Veuillez patienter pendant qu''une secrétaire valide ou refuse cette demande de réservation.'
    sender = 'à compléter avec l''adresse de l''expéditeur'
    recipient_list = settings.EMAIL_RECIPIENTS
    send_mail(subject, message, sender, recipient_list)


# MODIFICATION DE RESERVATION


def send_reservation_update_email_admin(booked_room):
    """
    Envoie un mail qui montre le changement d'une réservation faite par l'admin
    """
    subject = 'Réservation modifiée'
    message = f'La réservation suivante a été modifiée.\n' \
              f'Salle: {booked_room.room_category}\n' \
              f'Nombre de personnes: {booked_room.peopleAmount}\n' \
              f'Date: {booked_room.date}\n' \
              f'Heure de début: {booked_room.startTime}\n' \
              f'Heure de fin: {booked_room.endTime}\n' \
              f'Groupe/Laboratoire: {booked_room.groups}\n' \
              f'Motif: {booked_room.motif}\n' \
              f'La réservation a été modifiée avec succès.'
    sender = 'à compléter avec l''adresse de l''expéditeur'
    recipient_list = settings.EMAIL_RECIPIENTS
    send_mail(subject, message, sender, recipient_list)


def send_reservation_update_email_user_by_admin(booked_room):
    """
    Envoie un mail qui montre le changement d'une réservation par l'admin faite par un utilisateur
    """
    subject = 'Mise à jour de votre réservation'
    message = f'La réservation suivante a été modifiée par les secrétaires:\n' \
              f'Salle: {booked_room.room_category}\n' \
              f'Nombre de personnes: {booked_room.peopleAmount}\n' \
              f'Date: {booked_room.date}\n' \
              f'Heure de début: {booked_room.startTime}\n' \
              f'Heure de fin: {booked_room.endTime}\n' \
              f'Groupe/Laboratoire: {booked_room.groups}\n' \
              f'Motif: {booked_room.motif}\n' \
              f'Veuillez patienter pendant qu''une secrétaire valide ou refuse cette modification.'
    sender = 'à compléter avec l''adresse de l''expéditeur'
    recipient_list = settings.EMAIL_RECIPIENTS
    send_mail(subject, message, sender, recipient_list)


def send_reservation_update_email_user(booked_room):
    """
    Envoie un mail qui indique à l'utilisateur que sa demande de réservation doit être acceptée à nouveau
    """
    subject = 'Mise à jour de votre réservation'
    message = f'La réservation suivante a été modifiée:\n' \
              f'Salle: {booked_room.room_category}\n' \
              f'Nombre de personnes: {booked_room.peopleAmount}\n' \
              f'Date: {booked_room.date}\n' \
              f'Heure de début: {booked_room.startTime}\n' \
              f'Heure de fin: {booked_room.endTime}\n' \
              f'Groupe/Laboratoire: {booked_room.groups}\n' \
              f'Motif: {booked_room.motif}\n' \
              f'Veuillez patienter pendant qu''une secrétaire valide ou refuse cette modification.'
    sender = 'à compléter avec l''adresse de l''expéditeur'
    recipient_list = settings.EMAIL_RECIPIENTS
    send_mail(subject, message, sender, recipient_list)


def send_reservation_update_email_admin_alert(booked_room):
    """
    Envoie un mail qui indique à l'admin qu'un utilisateur a modifié sa réservation
    """
    subject = 'Mise à jour d''une réservation'
    message = f'La réservation suivante a été modifiée par {booked_room.user.first_name} {booked_room.user.last_name}:\n' \
              f'Salle: {booked_room.room_category}\n' \
              f'Nombre de personnes: {booked_room.peopleAmount}\n' \
              f'Date: {booked_room.date}\n' \
              f'Heure de début: {booked_room.startTime}\n' \
              f'Heure de fin: {booked_room.endTime}\n' \
              f'Groupe/Laboratoire: {booked_room.groups}\n' \
              f'Motif: {booked_room.motif}\n' \
              f'Veuillez valider ou refuser cette modification.'
    sender = 'à compléter avec l''adresse de l''expéditeur'
    recipient_list = settings.EMAIL_RECIPIENTS
    send_mail(subject, message, sender, recipient_list)


# ANNULATION DE RESERVATION


def send_reservation_cancellation_email_user_alert_validated_pending_reservation(booked_room):
    """
    Envoie un mail qui indique à l'utilisateur que sa réservation a été annulée
    """
    subject = 'Réservation annulée'
    message = f'Votre réservation suivante a été annulée.\n' \
              f'Salle: {booked_room.room_category}\n' \
              f'Nombre de personnes: {booked_room.peopleAmount}\n' \
              f'Date: {booked_room.date}\n' \
              f'Heure de début: {booked_room.startTime}\n' \
              f'Heure de fin: {booked_room.endTime}\n' \
              f'Groupe/Laboratoire: {booked_room.groups}\n' \
              f'Motif: {booked_room.motif}\n' \
              f'La réservation a été annulée.'
    sender = 'à compléter avec l''adresse de l''expéditeur'
    recipient_list = settings.EMAIL_RECIPIENTS
    send_mail(subject, message, sender, recipient_list)


def send_reservation_cancellation_email_admin_alert_validated_pending_reservation(booked_room):
    """
    Envoie un mail qui indique à l'admin qu'une réservation a été annulée
    """
    subject = 'Réservation annulée'
    message = f'Votre réservation suivante a été annulée.\n' \
              f'Salle: {booked_room.room_category}\n' \
              f'Nombre de personnes: {booked_room.peopleAmount}\n' \
              f'Date: {booked_room.date}\n' \
              f'Heure de début: {booked_room.startTime}\n' \
              f'Heure de fin: {booked_room.endTime}\n' \
              f'Groupe/Laboratoire: {booked_room.groups}\n' \
              f'Motif: {booked_room.motif}\n' \
              f'La réservation a été annulée.'
    sender = 'à compléter avec l''adresse de l''expéditeur'
    recipient_list = settings.EMAIL_RECIPIENTS
    send_mail(subject, message, sender, recipient_list)


def send_reservation_cancellation_email_user(booked_room):
    """
    Envoie un mail qui confirme l'annulation effectuée par l'utilisateur d'une réservation (en attente)
    """
    subject = 'Annulation de votre réservation'
    message = f'La réservation suivante a été annulée :\n' \
              f'Salle: {booked_room.room_category}\n' \
              f'Nombre de personnes: {booked_room.peopleAmount}\n' \
              f'Date: {booked_room.date}\n' \
              f'Heure de début: {booked_room.startTime}\n' \
              f'Heure de fin: {booked_room.endTime}\n' \
              f'Groupe/Laboratoire: {booked_room.groups}\n' \
              f'Motif: {booked_room.motif}\n' \
              f'La réservation a été annulée.\n'
    sender = 'à compléter avec l''adresse de l''expéditeur'
    recipient_list = settings.EMAIL_RECIPIENTS
    send_mail(subject, message, sender, recipient_list)


def send_reservation_cancellation_email_admin_alert_validated_reservation(booked_room):
    """
    Envoie un mail qui confirme l'annulation effectuée par l'admin d'une réservation (confirmée)
    """
    subject = 'Réservation annulée'
    message = f'La réservation (confirmée) suivante a été annulée par {booked_room.user.first_name} {booked_room.user.last_name}.\n' \
              f'Salle: {booked_room.room_category}\n' \
              f'Nombre de personnes: {booked_room.peopleAmount}\n' \
              f'Date: {booked_room.date}\n' \
              f'Heure de début: {booked_room.startTime}\n' \
              f'Heure de fin: {booked_room.endTime}\n' \
              f'Groupe/Laboratoire: {booked_room.groups}\n' \
              f'Motif: {booked_room.motif}\n' \
              f'La réservation a été annulée.'
    sender = 'à compléter avec l''adresse de l''expéditeur'
    recipient_list = settings.EMAIL_RECIPIENTS
    send_mail(subject, message, sender, recipient_list)


def send_reservation_cancellation_email_user_alert_validated_reservation(booked_room):
    """
    Envoie un mail qui confirme l'annulation effectuée par l'utilisateur d'une réservation (confirmée)
    """
    subject = 'Réservation annulée'
    message = f'Votre réservation (confirmée) suivante a été annulée:\n' \
              f'Salle: {booked_room.room_category}\n' \
              f'Nombre de personnes: {booked_room.peopleAmount}\n' \
              f'Date: {booked_room.date}\n' \
              f'Heure de début: {booked_room.startTime}\n' \
              f'Heure de fin: {booked_room.endTime}\n' \
              f'Groupe/Laboratoire: {booked_room.groups}\n' \
              f'Motif: {booked_room.motif}\n' \
              f'La réservation a été annulée.'
    sender = 'à compléter avec l''adresse de l''expéditeur'
    recipient_list = settings.EMAIL_RECIPIENTS
    send_mail(subject, message, sender, recipient_list)
