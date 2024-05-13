from django.http import HttpResponse  # Importe la classe HttpResponse pour gérer les réponses HTTP
from django.views.generic import ListView  # Importe la classe ListView pour afficher une liste d'objets
from django.urls import reverse_lazy  # Importe la fonction reverse_lazy pour les URL asynchrones
from hotel_reservation_project import settings  # Importe les paramètres du projet
from .models import RoomCategory  # Importe le modèle RoomCategory
from bookedrooms.models import BookedRoom  # Importe le modèle BookedRoom
from bootstrap_datepicker_plus import DatePickerInput, \
    TimePickerInput  # Importe les widgets DatePickerInput et TimePickerInput
from django.contrib.auth.mixins import \
    LoginRequiredMixin  # Importe le mixin LoginRequiredMixin pour les vues basées sur les classes
from django.views.generic.edit import UpdateView, DeleteView, CreateView  # Importe les vues génériques d'édition
from icalendar import Calendar, Event  # Importe les classes pour créer des fichiers .ics
from datetime import datetime, time  # Importe les classes pour manipuler les dates et heures
import os  # Importe le module os pour les opérations sur le système d'exploitation


def add_to_ics():
    objets = BookedRoom.objects.all()
    # print('affichage des reservations (brut) :')
    # # Affichez les données
    # for objet in objets:
    #     print(objet.__dict__)

    # for objet in objets:
    #     print('===============================')
    #     print('     Affichage des salles :')
    #     print('===============================')
    #     print('     affichage de l\'id :\n' + '     ' + str(objet.id))
    #     print('     affichage du labo :\n' + '     ' + str(objet.groups))
    #     print('     affichage de la salle :\n' + '     ' + str(objet.room_category))
    #     print('     affichage de la date :\n' + '     ' + str(objet.date))
    #     print('     affichage de l\'heure de début:\n' + '     ' + str(objet.startTime))
    #     print('     affichage de l\'heure de fin:\n' + '     ' + str(objet.endTime))
    #     print('     affichage de status:\n' + '     ' + str(objet.status))
    #     print('     affichage du motif:\n' + '     ' + str(objet.motif))
    #     print('     affichage du nombre de personnes:\n' + '     ' + str(objet.peopleAmount))
    #     print('     affichage du user:\n' + '     ' + str(objet.user))

    cal = Calendar()

    for objet in objets:
        event = Event()
        # 20240504T080000
        dateDeb = datetime.combine(objet.date, objet.startTime)
        dateFin = datetime.combine(objet.date, objet.endTime)
        event.add('summary', str(objet.room_category))
        event.add('dtstart', dateDeb)
        event.add('dtend', dateFin)

        cal.add_component(event)

    ical_data = cal.to_ical()
    current_directory = os.path.dirname(__file__)

    # Chemin relatif vers le fichier
    ics_file_path = os.path.join(current_directory, '..', 'fullcalendar', 'calendarFiles', 'calendarBookedroom.ics')

    # Écrire les données dans le fichier
    with open(ics_file_path, 'wb') as f:
        f.write(ical_data)


class HomePageView(LoginRequiredMixin, CreateView):
    """
    Affiche la page d'accueil et gère la création de réservations de chambres.
    """
    model = BookedRoom
    template_name = 'home.html'
    fields = ('room_category', 'peopleAmount', 'date', 'startTime', 'endTime', 'groups', 'status', 'motif')
    success_url = reverse_lazy('home')
    login_url = 'login'

    def get_form(self):
        """
        Surcharge pour changer les DateFields en widgets DatePicker.
        """
        form = super(HomePageView, self).get_form()
        form.fields['room_category'].label = 'Nom de la salle'
        form.fields['peopleAmount'].label = 'Nombre de pers. max.'
        form.fields['peopleAmount'].widget.attrs['min'] = 1
        form.fields['peopleAmount'].widget.attrs['max'] = 30
        form.fields['date'].label = 'Jour de la réservation'
        form.fields['date'].widget = DatePickerInput()
        form.fields['startTime'].label = 'Début de la réservation'
        form.fields['startTime'].widget = TimePickerInput().start_of('duration')
        form.fields['endTime'].label = 'Fin de la réservation'
        form.fields['endTime'].widget = TimePickerInput().end_of('duration')
        form.fields['groups'].label = 'Laboratoire'
        form.fields['motif'].label = 'Motif'
        del form.fields['status']
        return form

    def form_valid(self, form):
        """
        Surcharge pour toujours définir l'utilisateur sur l'utilisateur actuellement connecté.
        """
        user = self.request.user
        form.instance.user = user
        print("Form data:", form.cleaned_data)
        print("Test:", form.cleaned_data['room_category'])
        print("Form errors:", form.errors)
        data = super(HomePageView, self).form_valid(form)
        add_to_ics()
        return data


def default_image(request):
    """
    Renvoie l'image par défaut.
    """
    default_image_path = os.path.join(settings.MEDIA_IMAGE)  # Chemin absolu vers l'image par défaut

    # Vérifie si l'image par défaut existe
    if os.path.exists(default_image_path):
        with open(default_image_path, 'rb') as f:
            image_content = f.read()  # Lit le contenu de l'image par défaut
        return HttpResponse(image_content, content_type='image/jpeg')  # Renvoie le contenu de l'image en réponse
    else:
        return HttpResponse(status=404)  # Renvoie une réponse 404 si l'image par défaut n'existe pas


class RoomListView(ListView):
    """
    Affiche une liste des catégories de chambres disponibles.
    """
    model = RoomCategory
    template_name = 'roomreservation_list.html'
    login_url = 'login'
