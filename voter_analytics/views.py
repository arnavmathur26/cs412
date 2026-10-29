import plotly.graph_objects as go
from django.db.models import Count
from django.views.generic import ListView, DetailView
from plotly.offline import plot

from .models import Voter

ELECTION_FIELDS = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
ELECTION_LABELS = ['2020 State', '2021 Town', '2021 Primary', '2022 General', '2023 Town']


class VoterFilterMixin:
    '''Shared filtering logic and filter-form context for Voter list/graph views.'''

    def filter_voters(self, voters):
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

    def get_filter_context(self):
        context = {}
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
        return context


class VoterListView(VoterFilterMixin, ListView):
    '''View to list and filter all Voter records, 100 per page.'''

    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        voters = super().get_queryset().order_by('last_name', 'first_name')
        return self.filter_voters(voters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_filter_context())

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


class GraphListView(VoterFilterMixin, ListView):
    '''View to show aggregate plotly graphs describing the (optionally filtered) Voters.'''

    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        return self.filter_voters(super().get_queryset())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_filter_context())

        voters = self.get_queryset()

        year_counts = (
            voters.exclude(date_of_birth=None)
            .values('date_of_birth__year')
            .annotate(count=Count('id'))
            .order_by('date_of_birth__year')
        )
        fig_birth_year = go.Figure(data=[go.Bar(
            x=[c['date_of_birth__year'] for c in year_counts],
            y=[c['count'] for c in year_counts],
        )])
        fig_birth_year.update_layout(
            title='Voter Distribution by Year of Birth',
            xaxis_title='Year of Birth', yaxis_title='Number of Voters',
        )
        context['birth_year_graph'] = plot(fig_birth_year, output_type='div', include_plotlyjs='cdn')

        total_voters = voters.count()
        min_party_count = total_voters * 0.0001
        party_counts = (
            voters.values('party_affiliation')
            .annotate(count=Count('id'))
            .filter(count__gte=min_party_count)
            .order_by('-count')
        )
        fig_party = go.Figure(data=[go.Pie(
            labels=[p['party_affiliation'] for p in party_counts],
            values=[p['count'] for p in party_counts],
        )])
        fig_party.update_layout(title='Voter Distribution by Party Affiliation')
        context['party_graph'] = plot(fig_party, output_type='div', include_plotlyjs=False)

        election_counts = [voters.filter(**{field: True}).count() for field in ELECTION_FIELDS]
        fig_elections = go.Figure(data=[go.Bar(x=ELECTION_LABELS, y=election_counts)])
        fig_elections.update_layout(
            title='Voter Participation by Election',
            xaxis_title='Election', yaxis_title='Number of Voters',
        )
        context['election_graph'] = plot(fig_elections, output_type='div', include_plotlyjs=False)

        return context
