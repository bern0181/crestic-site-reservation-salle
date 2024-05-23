from django.core.mail import send_mail


def send_reservation_confirmation_email(booked_room):
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
    recipient_list = ['à compléter avec l''adresse des destinataires']
    send_mail(subject, message, sender, recipient_list)


def send_reservation_update_email(booked_room):
    subject = 'Réservation modifiée'
    message = f'La réservation suivante a été modifiée par {booked_room.user.first_name} {booked_room.user.last_name}.\n' \
              f'Salle: {booked_room.room_category}\n' \
              f'Nombre de personnes: {booked_room.peopleAmount}\n' \
              f'Date: {booked_room.date}\n' \
              f'Heure de début: {booked_room.startTime}\n' \
              f'Heure de fin: {booked_room.endTime}\n' \
              f'Groupe/Laboratoire: {booked_room.groups}\n' \
              f'Motif: {booked_room.motif}\n' \
              f'Veuillez valider ou refuser cette modification de réservation.'
    sender = 'à compléter avec l''adresse de l''expéditeur'
    recipient_list = ['à compléter avec l''adresse des destinataires']
    send_mail(subject, message, sender, recipient_list)


def send_reservation_cancellation_email(booked_room):
    subject = 'Réservation annulée'
    message = f'La réservation suivante a été annulée par {booked_room.user.first_name} {booked_room.user.last_name}.\n' \
              f'Salle: {booked_room.room_category}\n' \
              f'Nombre de personnes: {booked_room.peopleAmount}\n' \
              f'Date: {booked_room.date}\n' \
              f'Heure de début: {booked_room.startTime}\n' \
              f'Heure de fin: {booked_room.endTime}\n' \
              f'Groupe/Laboratoire: {booked_room.groups}\n' \
              f'Motif: {booked_room.motif}\n' \
              f'La réservation a été annulée et n\'a plus besoin d\'être validée.'
    sender = 'à compléter avec l''adresse de l''expéditeur'
    recipient_list = ['à compléter avec l''adresse des destinataires']
    send_mail(subject, message, sender, recipient_list)
