from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from django.core.mail import send_mail

import bookedrooms.models  # Import du modèle bookedrooms pour accéder aux choix de statut
from django.contrib.auth.mixins import (
    LoginRequiredMixin,  # Import du mixin LoginRequiredMixin pour obliger l'authentification de l'utilisateur
    UserPassesTestMixin
)
from django.shortcuts import render, get_object_or_404, redirect  # Import de la fonction get_object_or_404 pour
from django.urls import \
    reverse_lazy  # Import de la fonction reverse_lazy pour obtenir les URL inversées de manière retardée
# récupérer un objet ou renvoyer une erreur 404
from django.views.generic import ListView, DetailView  # Import des vues génériques ListView et DetailView
from django.views.generic.edit import UpdateView, DeleteView, \
    CreateView  # Import des vues génériques UpdateView, DeleteView et CreateView
from rooms.models import RoomCategory  # Import du modèle RoomCategory pour les catégories de salles
from rooms.views import add_to_ics
from utils import send_reservation_confirmation_email_admin
from .models import BookedRoom  # Import du modèle BookedRoom pour les réservations de salles
from django.core.exceptions import PermissionDenied
from django.db import transaction

class BookedRoomsListView(LoginRequiredMixin, ListView):
    model = BookedRoom  # Utilisation du modèle BookedRoom pour cette vue
    template_name = 'bookedroom_list.html'  # Utilisation du template 'bookedroom_list.html'
    login_url = 'login'  # URL vers laquelle rediriger les utilisateurs non authentifiés

    # Retourne uniquement les données de l'utilisateur actuellement connecté
    def get_queryset(self):
        return BookedRoom.objects.filter(
            user=self.request.user).order_by('date')


class BookedRoomsDetailView(LoginRequiredMixin, DetailView):
    model = BookedRoom  # Utilisation du modèle BookedRoom pour cette vue
    template_name = 'bookedroom_detail.html'  # Utilisation du template 'bookedroom_detail.html'
    login_url = 'login'  # URL vers laquelle rediriger les utilisateurs non authentifiés


class BookedRoomsUpdateView(LoginRequiredMixin, UpdateView):
    model = BookedRoom
    fields = ('room_category', 'peopleAmount', 'date', 'startTime', 'endTime', 'groups',
              'motif')  # Champs modifiables dans le formulaire
    template_name = 'bookedroom_edit.html'  # Utilisation du template 'bookedroom_edit.html'
    success_url = reverse_lazy('myprofile')  # URL à laquelle rediriger après la modification
    login_url = 'login'  # URL vers laquelle rediriger les utilisateurs non authentifiés

    def get_form(self):
        # Personnalisation du formulaire
        form = super(BookedRoomsUpdateView, self).get_form()
        form.fields['room_category'].label = 'Nom de la salle'  # Changement de l'étiquette du champ room_category

        form.fields['peopleAmount'].label = 'Nombre de personne'  # Changement de l'étiquette du champ peopleAmount
        form.fields['peopleAmount'].widget.attrs['min'] = 1  # Définition de la valeur minimale autorisée
        form.fields['peopleAmount'].widget.attrs['max'] = 30  # Définition de la valeur maximale autorisée

        form.fields['date'].label = 'Jour de la réservation'  # Changement de l'étiquette du champ date
        form.fields['date'].widget = DatePickerInput(
            options={
                "locale": "fr",
                "format": "DD/MM/YYYY",
            }
        )
        form.fields['startTime'].label = 'Début de la réservation'  # Changement de l'étiquette du champ startTime
        form.fields['startTime'].widget = TimePickerInput().start_of(
            'duration')  # Utilisation du widget TimePickerInput pour le champ startTime

        form.fields['endTime'].label = 'Fin de la réservation'  # Changement de l'étiquette du champ endTime
        form.fields['endTime'].widget = TimePickerInput().end_of(
            'duration')  # Utilisation du widget TimePickerInput pour le champ endTime

        form.fields['groups'].label = 'Laboratoire'  # Changement de l'étiquette du champ groups

        form.fields['motif'].label = 'Motif'  # Changement de l'étiquette du champ motif

        return form

    def form_valid(self, form):
        # Validation du formulaire
        user = self.request.user
        form.instance.user = user
        data = super(BookedRoomsUpdateView, self).form_valid(form)
        #send_reservation_confirmation_email_admin(form.instance)
        add_to_ics()
        return data


class BookedRoomsDeleteView(LoginRequiredMixin, DeleteView):
    model = BookedRoom  # Utilisation du modèle BookedRoom pour cette vue
    template_name = 'bookedroom_delete.html'  # Utilisation du template 'bookedroom_delete.html'
    success_url = reverse_lazy('myprofile')  # URL à laquelle rediriger après la suppression
    login_url = 'login'  # URL vers laquelle rediriger les utilisateurs non authentifiés

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        #send_reservation_confirmation_email_admin(self.object)
        response = super().delete(request, *args, **kwargs)

        # Appel de la fonction add_to_ics pour ajouter l'événement à l'ICS
        add_to_ics()

        return response


class BookedRoomsCreateView(LoginRequiredMixin, CreateView):
    model = BookedRoom  # Utilisation du modèle BookedRoom pour cette vue
    fields = ('room_category', 'peopleAmount', 'date', 'startTime', 'endTime', 'groups', 'status',
              'motif')  # Champs modifiables dans le formulaire
    template_name = 'bookedroom_add.html'  # Utilisation du template 'bookedroom_add.html'
    success_url = reverse_lazy('myprofile')  # URL à laquelle rediriger après la création
    login_url = 'login'  # URL vers laquelle rediriger les utilisateurs non authentifiés

    def dispatch(self, request, *args, **kwargs):
        """
        Remplacement pour s'assurer que la clé primaire passée
        existe
        """
        self.room_category = get_object_or_404(RoomCategory, pk=kwargs['room_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        """
        Retourne les données initiales à utiliser pour les formulaires sur cette vue.
        """
        initial = super(BookedRoomsCreateView, self).get_initial()
        initial['room_category'] = self.room_category
        return initial

    def get_form(self):
        """
        Remplacement pour changer les champs DateFields des boîtes de texte en
        widgets DatePicker
        """
        form = super(BookedRoomsCreateView, self).get_form()
        form.fields['room_category'].label = 'Nom de la salle'  # Changement de l'étiquette du champ room_category

        form.fields['peopleAmount'].label = 'Nombre de pers. max.'  # Changement de l'étiquette du champ peopleAmount
        form.fields['peopleAmount'].widget.attrs['min'] = 1  # Définition de la valeur minimale autorisée
        form.fields['peopleAmount'].widget.attrs['max'] = 30  # Définition de la valeur maximale autorisée

        form.fields['date'].label = 'Jour de la réservation'  # Changement de l'étiquette du champ date
        form.fields['date'].widget = DatePickerInput(
            options={
                "locale": "fr",
                "format": "DD/MM/YYYY",
            }
        )

        form.fields['startTime'].label = 'Début de la réservation'  # Changement de l'étiquette du champ startTime
        form.fields['startTime'].widget = TimePickerInput().start_of(
            'duration')  # Utilisation du widget TimePickerInput pour le champ startTime

        form.fields['endTime'].label = 'Fin de la réservation'  # Changement de l'étiquette du champ endTime
        form.fields['endTime'].widget = TimePickerInput().end_of(
            'duration')  # Utilisation du widget TimePickerInput pour le champ endTime

        form.fields['groups'].label = 'Laboratoire'  # Changement de l'étiquette du champ groups

        form.fields['motif'].label = 'Motif'  # Changement de l'étiquette du champ motif

        del form.fields['status']  # Suppression du champ status du formulaire
        return form

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        form.instance.status = BookedRoom.STATUS_CHOICES[0][0]

        response = super(BookedRoomsCreateView, self).form_valid(form)
        #send_reservation_confirmation_email_admin(form.instance)
        add_to_ics()
        return response


class BookedRoomsValidationView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = BookedRoom  # Utilisation du modèle BookedRoom pour cette vue
    template_name = 'bookedroom_validation.html'  # Utilisation du template 'bookedroom_validation.html'
    success_url = reverse_lazy('bookedrooms_validation')
    login_url = 'login'  # URL vers laquelle rediriger les utilisateurs non authentifiés

    def test_func(self):
        """
        Fonction de test pour vérifier si l'utilisateur est un superutilisateur.
        """
        return self.request.user.isSecretary or self.request.user.is_superuser


def BookedRoomsValidationRefusedView(request, pk):
    if not request.user.is_authenticated or (not request.user.isSecretary and not request.user.is_superuser):
        raise PermissionDenied
    reservation = get_object_or_404(BookedRoom, id=pk)
    if request.method == 'POST':
        reservation.status = 'canceled'
        reservation.save()
        add_to_ics()
        return redirect('bookedrooms_validation')  # redirigez vers une page de succès ou de confirmation
    return render(request, 'bookedroom_validation_refused.html', {'reservation': reservation})


def BookedRoomsValidationValidatedView(request, pk):
    if not request.user.is_authenticated or (not request.user.isSecretary and not request.user.is_superuser):
        raise PermissionDenied
    reservation = get_object_or_404(BookedRoom, id=pk)
    if request.method == 'POST':
        reservation.status = 'validated'
        reservation.save()
        # Recherche des réservations en attente qui occupent la même salle
        pending_bookings_to_delete = BookedRoom.objects.filter(
            room_category=reservation.room_category,
            date=reservation.date,
            startTime__lt=reservation.endTime,
            endTime__gt=reservation.startTime,
            status='pending'
        )
        # Suppression des réservations en attente trouvées
        with transaction.atomic():
            pending_bookings_to_delete.delete()
        add_to_ics()
        return redirect('bookedrooms_validation')  # redirigez vers une page de succès ou de confirmation
    return render(request, 'bookedroom_validation_validated.html', {'reservation': reservation})

