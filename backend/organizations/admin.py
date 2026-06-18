from django.contrib import admin

from organizations.models import Classroom, Organization, OrganizationMember, School, Team, TeamMember


admin.site.register(Organization)
admin.site.register(School)
admin.site.register(Classroom)
admin.site.register(OrganizationMember)
admin.site.register(Team)
admin.site.register(TeamMember)
