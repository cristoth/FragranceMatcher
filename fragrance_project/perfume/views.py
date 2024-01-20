from django.shortcuts import render

# Create your views here.
from datetime import timedelta, timezone
import os
from gensim.models import word2vec
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
# from django.db.models import Count
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView
)
from .models import Fragrance, Perfume, Perfume_Fragrance
from .forms import PerfumeForm, PerfumeFragranceFormSet
# from hitcount.views import HitCountDetailView


@login_required
def home(request):
    # popular = Perfume.objects.order_by("-hit_count_generic__hits")
    # period = timezone.now() - timedelta(days=30)
    # top_models = Perfume.objects.filter(
    #     hitcounts__hit__created__gte=period
    # ).annotate(
    #     counts=Recipe.Count('hitcounts__hit')
    # ).order_by('-counts')
    context = {
        'perfumes': Perfume.objects.all(),
        # 'popular': top_models,
    }
    return render(request, 'perfume/home.html', context)


class PerfumeListView(LoginRequiredMixin, ListView):  # class based view
    model = Perfume
    # if template_name not given, needs view template with name: <app>/<model>_<viewtype>.html
    template_name = 'perfume/home.html'
    context_object_name = 'perfumes'
    ordering = ['-date_posted']
    paginate_by = 3

    # def get_context_data(self, **kwargs):
        # popular = Recipe.objects.annotate(downloads=Count('download')).order_by(
        #     '-downloads', '-hit_count_generic__hits')[:6]
        # context = super().get_context_data(**kwargs)
        # context.update({
        #     'popular': popular,
        # })
        # return context


# class UserPerfumeListView(LoginRequiredMixin, ListView):  # filtered recipes by user
#     model = Perfume
#     template_name = 'perfume/user_perfume.html'
#     context_object_name = 'perfumes'
#     ordering = ['-date_posted']
#     paginate_by = 3

#     def get_queryset(self):
#         user = get_object_or_404(User, username=self.kwargs.get('username'))
#         return Perfume.objects.filter(author=user).order_by('-date_posted')


class PerfumeDetailView(LoginRequiredMixin, DetailView): #, HitCountDetailView):
    model = Perfume  # template: perfume/perfume_detail.html
    context_object_name = 'rec'
    template_name = 'perfume/perfume_detail.html'
    # set to True to count the hit
    # count_hit = True


# def download(request):
#     if request.method == 'POST':
#         pk = request.POST.get('recipe')
#         rec = get_object_or_404(Recipe, id=pk)
#         download = Download(recipe=rec)
#         download.save()
#     return redirect('perfume-detail', pk)


@login_required
def perfume_create_view(request):
    if request.method == 'POST':
        perfume_form = PerfumeForm(request.POST, request.FILES)
        perfume_form.instance = perfume_form.save(commit=False)
        perfume_form.instance.author = request.user
        formset = PerfumeFragranceFormSet(request.POST)

        if not formset.is_valid():
            messages.error(
                request, f'Please correct the errors below and resubmit.')
            context = {
                'perfume_form': perfume_form,
                'perfume_fragrance_formset': formset,
                'form_errors': formset.errors
            }
            return render(request, 'perfume/perfume_form.html', context)

        if perfume_form.is_valid() and formset.is_valid():
            perfume_form.save()

            for form in formset:
                if form.cleaned_data != {} and form not in formset.deleted_forms:
                    form.instance.perfume = perfume_form.instance
                    form.save()
                    perfume_form.instance.fragrances.add(
                        form.instance.fragrance)
            perfume_form.save()
        messages.success(request, f'Your perfume has been created!')
        return redirect('perfume-home')

    else:
        perfume_form = PerfumeForm()
        formset = PerfumeFragranceFormSet(
            queryset=Perfume_Fragrance.objects.none())

    context = {
        'title': 'Create Perfume',
        'perfume_form': perfume_form,
        'perfume_fragrance_formset': formset
    }
    return render(request, 'perfume/perfume_form.html', context)


@login_required
def perfume_update_view(request, pk):
    perfume = get_object_or_404(Perfume, id=pk)
    if perfume.author != request.user:
        raise Http404()
    qs = perfume.perfume_fragrance_set.all()

    if request.method == 'POST':
        # get path to old image
        dir = os.path.abspath(os.path.dirname(__name__))
        filename = [dir] + perfume.image.url.split('/')
        old_image_url = os.path.join(*filename)

        perfume_form = PerfumeForm(request.POST, request.FILES, instance=perfume)
        formset = PerfumeFragranceFormSet(request.POST)

        if not formset.is_valid():
            messages.error(
                request, f'Please correct the errors below and resubmit.')
            context = {
                'perfume_form': perfume_form,
                'perfume_fragrance_formset': formset,
                'form_errors': formset.errors
            }
            return render(request, 'perfume/perfume_form.html', context)

        if perfume_form.is_valid():
            # formset.save()
            for form in formset:  # fragrances
                if form.is_valid() and form.cleaned_data != {} and form not in formset.deleted_forms:
                    form.instance.perfume = perfume_form.instance
                    form.save()
                    perfume_form.instance.fragrances.add(
                        form.instance.fragrance)

            # delete old image
            if os.path.isfile(old_image_url) and not old_image_url.endswith('default_perfume.jpg') and 'image' in request.FILES:
                os.remove(old_image_url)
            # perfume_form.calculate_nutritional_value()
            perfume_form.save()

            # to delete objects
            instances = formset.save(commit=False)
            for obj in formset.deleted_objects:
                obj.delete()
        messages.success(request, f'Your perfume has been updated!')
        return redirect('perfume-home')

    else:
        perfume_form = PerfumeForm(instance=perfume)
        formset = PerfumeFragranceFormSet(queryset=qs)

    context = {
        'title': 'Update Perfume',
        'perfume_form': perfume_form,
        'perfume_fragrance_formset': formset
    }
    return render(request, 'perfume/perfume_form.html', context)


class PerfumeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):  # class based view
    model = Perfume
    success_url = '/'

    # user must pass test function in order to delete a perfume
    def test_func(self):
        perfume = self.get_object()
        if self.request.user == perfume.author:
            return True
        return False


def about(request):
    return render(request, 'perfume/about.html', {'title': 'About'})


@login_required
def fragrance_view(request):
    context = {'title': 'Fragrance Similarities'}
    if 'search-form' in request.POST:
        # get path to ai model
        dir = os.path.abspath(os.path.dirname(__name__))
        filename = dir + '\\ai\\word2vec.model'
        model = word2vec.Word2Vec.load(filename)
        fragrance = get_object_or_404(
            Fragrance, id=request.POST['fragrance'])
        context['ingr'] = fragrance
        fragrance = fragrance.name
        ingr = []
        comp = []
        if fragrance.lower().strip() not in model.wv.key_to_index:
            context['exists'] = False
        else:
            context['exists'] = True
            for ing, compatibility in model.wv.most_similar(positive=fragrance.lower().strip()):
                ingr.append(Fragrance.objects.filter(name__iexact=ing).first())
                comp.append(round(compatibility*100, 2))
            # Fragrance.objects.filter(name__in=ingr)
            context['similar'] = zip(ingr, comp)

    elif 'test-form' in request.POST:
        # get path to ai model
        dir = os.path.abspath(os.path.dirname(__name__))
        filename = dir + '\\ai\\word2vec.model'
        model = word2vec.Word2Vec.load(filename)
        ingr1 = get_object_or_404(Fragrance, id=request.POST['fragrance1'])
        ingr2 = get_object_or_404(Fragrance, id=request.POST['fragrance2'])
        context['ingr1'] = ingr1
        context['ingr2'] = ingr2
        if ingr1.name.lower().strip() not in model.wv.key_to_index or ingr2.name.lower().strip() not in model.wv.key_to_index:
            context['exists'] = False
        else:
            context['exists'] = True
            context['test_result'] = round(
                model.wv.similarity(ingr1.name.lower().strip(), ingr2.name.lower().strip())*100, 2)

    ingr_search = Fragrance.objects.all()

    context['ingr_search'] = ingr_search
    return render(request, 'perfume/fragrance_similarity.html', context)
