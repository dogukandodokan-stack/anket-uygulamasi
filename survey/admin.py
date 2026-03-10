from django.contrib import admin
from django.urls import path
from django.shortcuts import get_object_or_404, render
from django.utils.html import format_html
import nested_admin
from .models import Survey, Question, Choice, Response, Answer


class ChoiceInline(nested_admin.NestedTabularInline):
    model = Choice
    extra = 3
    min_num = 2


class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    extra = 1
    inlines = [ChoiceInline]


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    readonly_fields = ("question", "choice")
    can_delete = False


@admin.register(Survey)
class SurveyAdmin(nested_admin.NestedModelAdmin):
    list_display = ("title", "is_active", "response_count", "created_at", "statistics_link")
    list_editable = ("is_active",)
    inlines = [QuestionInline]

    def response_count(self, obj):
        return obj.responses.count()
    response_count.short_description = "Katılımcı"

    def statistics_link(self, obj):
        return format_html(
            '<a href="{}">İstatistikler</a>',
            f"/admin/survey/survey/{obj.pk}/istatistik/"
        )
    statistics_link.short_description = ""

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path("<int:pk>/istatistik/", self.admin_site.admin_view(self.statistics_view), name="survey_statistics"),
        ]
        return custom + urls

    def statistics_view(self, request, pk):
        survey = get_object_or_404(Survey, pk=pk)
        total_responses = survey.responses.count()

        stats = []
        for question in survey.questions.prefetch_related("choices").all():
            choices_data = []
            for choice in question.choices.all():
                count = Answer.objects.filter(question=question, choice=choice).count()
                percentage = round((count / total_responses * 100), 1) if total_responses else 0
                choices_data.append({
                    "text": choice.text,
                    "count": count,
                    "percentage": percentage,
                })
            stats.append({
                "question": question.text,
                "choices": choices_data,
            })

        context = {
            **self.admin_site.each_context(request),
            "survey": survey,
            "total_responses": total_responses,
            "stats": stats,
            "title": f"{survey.title} — İstatistikler",
        }
        return render(request, "admin/survey/statistics.html", context)


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "survey", "submitted_at")
    list_filter = ("survey",)
    readonly_fields = ("first_name", "last_name", "survey", "submitted_at")
    inlines = [AnswerInline]
