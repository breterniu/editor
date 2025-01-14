from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic

from editor import forms
from editor.models import EditorItem, ItemQueue, Project, ItemQueueChecklistItem, ItemQueueEntry, ItemQueueChecklistTick, IndividualAccess
import editor.views.generic
from editor.views.generic import CanViewMixin, CanEditMixin, CanDeleteMixin, SettingsPageMixin, RestrictAccessMixin

class MustBeOwnerMixin(RestrictAccessMixin):
    def can_access(self, request):
        return request.user == self.get_object().owner

class CreateView(CanEditMixin, generic.CreateView):
    model = ItemQueue
    form_class = forms.CreateItemQueueForm
    template_name = 'queue/new.html'

    def can_access(self, request):
        if self.request.method == 'POST':
            project = Project.objects.get(pk=int(self.request.POST.get('project')))
            return project.can_be_edited_by(self.request.user)
        else:
            return True

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        data = self.initial.copy()
        data['owner'] = self.request.user
        if 'project' in self.request.GET:
            data['project'] = Project.objects.get(pk=int(self.request.GET['project']))
        else:
            data['project'] = self.request.user.userprofile.personal_project
        return data

    def form_valid(self, form):
        response = super().form_valid(form)
        for label in self.request.POST.getlist('checklist'):
            label = label.strip()
            if label!='':
                ItemQueueChecklistItem.objects.create(queue=self.object, label=label)
        return response

    def get_success_url(self):
        return reverse('queue_view', args=(self.object.pk,))

class UpdateView(SettingsPageMixin, generic.UpdateView):
    model = ItemQueue
    form_class = forms.UpdateItemQueueForm
    template_name = 'queue/edit.html'
    context_object_name = 'queue'
    settings_page = 'options'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['checklist_items'] = [c.as_json() for c in self.object.checklist.all()]

        return context

    def form_valid(self, form):
        response = super().form_valid(form)

        labels = self.request.POST.getlist('checklist')
        pks = self.request.POST.getlist('id')

        self.object.checklist.exclude(pk__in=[int(x) for x in pks if x]).delete()

        for label,pk in zip(labels, pks):
            if pk:
                item = ItemQueueChecklistItem.objects.get(pk=int(pk))
                if label:
                    item.label = label
                    item.save()
                else:
                    item.delete()
            else:
                if label:
                    ItemQueueChecklistItem.objects.create(queue=self.object, label=label)

        return response

    def get_success_url(self):
        return reverse('queue_view', args=(self.object.pk,))

class ManageMembersView(SettingsPageMixin, generic.UpdateView):
    model = ItemQueue
    context_object_name = 'queue'
    template_name = 'queue/manage_members.html'
    settings_page = 'members'
    form_class = editor.forms.IndividualAccessFormset

    def get_context_data(self, **kwargs):
        context = super(ManageMembersView, self).get_context_data(**kwargs)
        ct = ContentType.objects.get_for_model(self.object)
        context['add_member_form'] = editor.forms.AddMemberForm({'object_content_type': ct.pk, 'object_id': self.object.pk, 'adding_user':self.request.user})
        return context

    def get_success_url(self):
        return reverse('queue_settings_members', args=(self.get_object().pk,))

class AddMemberView(SettingsPageMixin, generic.CreateView):
    model = IndividualAccess
    form_class = editor.forms.AddMemberForm
    template_name = 'queue/add_member.html'
    settings_page = 'members'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['queue'] = self.get_queue()
        return context

    def get_queue(self):
        return ItemQueue.objects.get(pk=self.kwargs['queue_pk'])

    def get_access_object(self):
        return self.get_queue()

    def get_success_url(self):
        return reverse('queue_settings_members', args=(self.object.object.pk,))

class DetailView(CanViewMixin, generic.DetailView):
    model = ItemQueue
    template_name = 'queue/view.html'
    context_object_name = 'queue'

class DeleteView(CanDeleteMixin, generic.DeleteView):
    model = ItemQueue
    template_name = 'queue/delete.html'
    context_object_name = 'queue'

    def get_success_url(self):
        return reverse('project_index', args=(self.object.project.pk,))

class AddEntryView(CanViewMixin, generic.CreateView):
    model = ItemQueueEntry
    form_class = forms.CreateItemQueueEntryForm
    template_name = 'queue/add.html'

    def get_access_object(self):
        return self.queue

    def dispatch(self, *args, **kwargs):
        self.queue = ItemQueue.objects.get(pk=self.kwargs.get('pk'))
        return super().dispatch(*args, **kwargs)

    def get_given_item(self):
        if 'item' in self.request.GET:
            return EditorItem.objects.get(pk=int(self.request.GET['item']))

    def get_initial(self):
        data = self.initial.copy()
        given_item = self.get_given_item()
        if given_item:
            data['item'] = given_item
        data['created_by'] = self.request.user
        data['queue'] = self.queue
        return data

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        context['queue'] = self.queue
        context['given_item'] = self.get_given_item()

        context['json'] = {
            'recent_items': self.request.user.userprofile.recent_questions,
            'basket': self.request.user.userprofile.question_basket.all(),
        }

        return context

    def get_success_url(self):
        return reverse('queue_view', args=(self.queue.pk,))

class EntryMixin(object):
    model = ItemQueueEntry
    context_object_name = 'entry'

    def get_queue(self):
        return self.get_object().queue

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['queue'] = self.get_queue()
        return context

class ReviewEntryView(CanViewMixin, EntryMixin, generic.DetailView):
    template_name = 'queue/review_entry.html'

    def get_access_object(self):
        return self.get_object().queue

    def post(self, request, *args, **kwargs):
        entry = self.get_object()
        if not entry.can_be_edited_by(request.user):
            return self.get_no_access_response()

        ticked_pks = [int(x) for x in self.request.POST.getlist('ticked-items')]
        to_delete = ItemQueueChecklistTick.objects.filter(entry=entry).exclude(item__pk__in=ticked_pks)
        to_delete.delete()
        to_add = entry.checklist_items().filter(ticked=False,pk__in=ticked_pks)
        for item in to_add:
            ItemQueueChecklistTick.objects.create(entry=entry, item=item, user=self.request.user)

        entry.complete = self.request.POST.get('remove') == 'on'
        entry.save()

        return redirect('queue_view', pk=entry.queue.pk)

class CommentView(CanViewMixin, editor.views.generic.CommentView):
    model = ItemQueueEntry

class UpdateEntryView(CanEditMixin, EntryMixin, generic.UpdateView):
    fields = ['note']
    template_name = 'queue/edit_entry.html'
    context_object_name = 'entry'

    def get_success_url(self):
        return reverse('queue_entry_review', args=(self.object.pk,))

class DeleteEntryView(CanEditMixin, EntryMixin, generic.DeleteView):
    template_name = 'queue/delete_entry.html'

    def get_success_url(self):
        return reverse('queue_view', args=(self.object.queue.pk,))
