from django.contrib import admin

from .models import Monomer
from .models import Dimer
from .models import Structure
from .models import AlternativeName
from .models import Pdb
from .models import MonomerToStructure

admin.site.register(Monomer)
admin.site.register(Dimer)
admin.site.register(Structure)
admin.site.register(AlternativeName)
admin.site.register(Pdb)
admin.site.register(MonomerToStructure)
