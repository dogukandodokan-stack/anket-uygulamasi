from django.shortcuts import render, get_object_or_404, redirect
from .models import Survey, Response, Answer


def survey_list(request):
    surveys = Survey.objects.filter(is_active=True).order_by("-created_at")
    return render(request, "survey/list.html", {"surveys": surveys})


def survey_detail(request, pk):
    survey = get_object_or_404(Survey, pk=pk, is_active=True)
    questions = survey.questions.prefetch_related("choices").all()

    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        errors = []

        if not first_name:
            errors.append("Ad alanı zorunludur.")
        if not last_name:
            errors.append("Soyad alanı zorunludur.")

        answers = {}
        for question in questions:
            choice_id = request.POST.get(f"question_{question.pk}")
            if not choice_id:
                errors.append(f'"{question.text}" sorusunu yanıtlayınız.')
            else:
                answers[question.pk] = choice_id

        if not errors:
            response = Response.objects.create(
                survey=survey,
                first_name=first_name,
                last_name=last_name,
            )
            for question_id, choice_id in answers.items():
                Answer.objects.create(
                    response=response,
                    question_id=question_id,
                    choice_id=choice_id,
                )
            return redirect("survey:thank_you", pk=survey.pk)

        return render(request, "survey/detail.html", {
            "survey": survey,
            "questions": questions,
            "errors": errors,
            "post_data": request.POST,
        })

    return render(request, "survey/detail.html", {
        "survey": survey,
        "questions": questions,
    })


def thank_you(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    return render(request, "survey/thank_you.html", {"survey": survey})
