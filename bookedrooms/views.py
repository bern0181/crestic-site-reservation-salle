import bookedrooms.models  # Import du modèle bookedrooms pour accéder aux choix de statut
from django.contrib.auth.mixins import \
    LoginRequiredMixin  # Import du mixin LoginRequiredMixin pour obliger l'authentification de l'utilisateur
from django.shortcuts import \
    get_object_or_404  # Import de la fonction get_object_or_404 pour récupérer un objet ou renvoyer une erreur 404
from django.views.generic import ListView, DetailView  # Import des vues génériques ListView et DetailView
from django.views.generic.edit import UpdateView, DeleteView, \
    CreateView  # Import des vues génériques UpdateView, DeleteView et CreateView
from django.urls import \
    reverse_lazy  # Import de la fonction reverse_lazy pour obtenir les URL inversées de manière retardée
from bootstrap_datepicker_plus import DatePickerInput, \
    TimePickerInput  # Import des widgets DatePickerInput et TimePickerInput de Bootstrap
from rooms.models import RoomCategory  # Import du modèle RoomCategory pour les catégories de salles
from .models import BookedRoom  # Import du modèle BookedRoom pour les réservations de salles
from rooms.views import add_to_ics


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
        form.fields['date'].widget = DatePickerInput()  # Utilisation du widget DatePickerInput pour le champ date

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
        form.instance.status = bookedrooms.models.BookedRoom.STATUS_CHOICES[0][
            0]  # Attribution du premier choix de statut par défaut
        data = super(BookedRoomsUpdateView, self).form_valid(form)
        add_to_ics()
        return data


class BookedRoomsDeleteView(LoginRequiredMixin, DeleteView):
    model = BookedRoom  # Utilisation du modèle BookedRoom pour cette vue
    template_name = 'bookedroom_delete.html'  # Utilisation du template 'bookedroom_delete.html'
    success_url = reverse_lazy('myprofile')  # URL à laquelle rediriger après la suppression
    login_url = 'login'  # URL vers laquelle rediriger les utilisateurs non authentifiés

    def delete(self, request, *args, **kwargs):
        # Appel de la méthode delete de la super classe
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
        form.fields['date'].widget = DatePickerInput()  # Utilisation du widget DatePickerInput pour le champ date

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
        """
        Remplacement pour toujours définir l'utilisateur sur l'utilisateur actuellement connecté
        """
        user = self.request.user
        form.instance.user = user
        form.instance.status = bookedrooms.models.BookedRoom.STATUS_CHOICES[0][0]  # Attribution du premier choix de statut par défaut

        print("Form data:", form.cleaned_data)
        print("Form errors:", form.errors)
        data = super(BookedRoomsCreateView, self).form_valid(form)
        add_to_ics()
        return data
