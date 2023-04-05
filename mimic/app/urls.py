from django.urls import path
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from django.views.generic import TemplateView

# from mimic.app.views.views import AlphaDetailView
# from mimic.app.views.views import BetaDetailView
# from mimic.app.views.views import DimerDetailView
# from mimic.app.views.views import DimerListView
# from mimic.app.views.views import DrugDetailView
# from mimic.app.views.views import PdbListView
# from mimic.app.views.views import PdbDetailView
# from mimic.app.views.views import DrugListView
# from mimic.app.views.views import ProteinInteractorDetailView
# from mimic.app.views.views import ProteinInteractorListView
from .views import browser, downloads, help, home, interactions, search, structures, views

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('home'), permanent=True), name='app', ),
    path('home', home.HomePageView, name='home', ),
    path('interactions/<slug:protein>', interactions.InteractionsView.as_view(), name='interactions', ),
    path('browser', browser.BrowserView.as_view(), name='browser', ),
    path('search', search.SearchView.as_view(), name='search', ),
    path('downloads', downloads.DownloadView, name='downloads', ),
    path('help', help.HelpView, name='help', ),
    path('integrins/', views.DimerListView.as_view(), name='integrins'),
    path('alpha/<slug:name>', views.AlphaDetailView.as_view(), name='alpha'),
    path('beta/<slug:name>', views.BetaDetailView.as_view(), name='beta'),
    path('dimer/<slug:lookup_name>', views.DimerDetailView.as_view(), name='dimer'),
    path('about', TemplateView.as_view(template_name="app/about.html"), name='about'),
    # path('pdbs/', views.PdbListView.as_view(), name='pdbs'),
    path('pdbs/', structures.StructureView, name='pdbs'),
    path('pdb/<slug:pdb>', views.PdbDetailView.as_view(), name='pdb'),
    path('drugs/', views.DrugListView.as_view(), name='drugs'),
    path('drug/<slug:name>', views.DrugDetailView.as_view(), name='drug'),
    path('protein-interactors/', views.ProteinInteractorListView.as_view(), name='protein-interactors'),
]
