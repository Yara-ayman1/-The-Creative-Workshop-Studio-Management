from django.urls import path
from . import views

urlpatterns = [
    # ── Workshop CRUD ──────────────────────────────────────────
    path('',                                           views.workshop_list,   name='workshop_list'),
    path('add/',                                       views.add_workshop,    name='add_workshop'),
    path('<int:artist_id>/<int:studio_id>/<int:workshop_id>/edit/',
                                                       views.edit_workshop,   name='edit_workshop'),
    path('<int:artist_id>/<int:studio_id>/<int:workshop_id>/delete/',
                                                       views.delete_workshop, name='delete_workshop'),

    # ── Detail page (registrations + materials) ────────────────
    path('<int:artist_id>/<int:studio_id>/<int:workshop_id>/',
                                                       views.workshop_detail, name='workshop_detail'),

    # ── Registrations ──────────────────────────────────────────
    path('<int:artist_id>/<int:studio_id>/<int:workshop_id>/register/',
                                                       views.register_member, name='register_member'),
    path('<int:artist_id>/<int:studio_id>/<int:workshop_id>/unregister/<int:member_id>/',
                                                       views.unregister_member, name='unregister_member'),

    # ── Material consumption ────────────────────────────────────
    path('<int:artist_id>/<int:studio_id>/<int:workshop_id>/consume/',
                                                       views.log_consumption, name='log_consumption'),
]