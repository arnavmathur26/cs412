from django.views.generic import ListView, DetailView

from .models import Voter

ELECTION_FIELDS = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']


class VoterListView(ListView):
    '''View to list and filter all Voter records, 100 per page.'''

    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        voters = super().get_queryset().order_by('last_name', 'first_name')

        party = self.request.GET.get('party_affiliation')
        if party:
            voters = voters.filter(party_affiliation=party)

        min_dob = self.request.GET.get('min_dob')
        if min_dob:
            voters = voters.filter(date_of_birth__year__gte=min_dob)

        max_dob = self.request.GET.get('max_dob')
        if max_dob:
            voters = voters.filter(date_of_birth__year__lte=max_dob)

        voter_score = self.request.GET.get('voter_score')
        if voter_score:
            voters = voters.filter(voter_score=voter_score)

        for field in ELECTION_FIELDS:
            if self.request.GET.get(field):
                voters = voters.filter(**{field: True})

        return voters

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['party_affiliations'] = (
            Voter.objects.order_by('party_affiliation')
            .values_list('party_affiliation', flat=True).distinct()
        )
        context['voter_scores'] = (
            Voter.objects.order_by('voter_score')
            .values_list('voter_score', flat=True).distinct()
        )
        years = (
            Voter.objects.exclude(date_of_birth=None)
            .values_list('date_of_birth__year', flat=True).distinct().order_by('date_of_birth__year')
        )
        context['years'] = years
        context['election_fields'] = [
            (field, bool(self.request.GET.get(field))) for field in ELECTION_FIELDS
        ]

        # preserve the submitted filter values so the form stays populated
        context['selected'] = self.request.GET

        # querystring for pagination links, without any existing page number
        querystring = self.request.GET.copy()
        querystring.pop('page', None)
        context['querystring'] = querystring.urlencode()
        return context


class VoterDetailView(DetailView):
    '''View to show all details of a single Voter record.'''

    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'
