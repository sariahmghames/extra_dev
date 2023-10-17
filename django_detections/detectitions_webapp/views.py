import os
import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import ImageUploadSerializer
from django.conf import settings


from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from .models import Question, Choice # django database API
from django.template import loader
from django.urls import reverse


# Create your views here.


DARKNET_PATH = os.path.join(settings.BASE_DIR, 'polls_app', 'static', 'darknet')


def index(request):
	latest_question_list = Question.objects.order_by("-pub_date")[:5]
	context = {"latest_question_list": latest_question_list,}  # The context is a dictionary mapping template variable names to Python objects.

	return render(request, "polls/index.html", context) # HttpResponse or use django shotcuts as render with template and context args



def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls_app:results", args=(question.id,))) # url to which user will be redirected, reverse() helps avoid having to hardcode a URL in the view function



def react_app_view(request):
    return render(request, 'index.html')



class DetectionAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['image']
            image_path = os.path.join(settings.MEDIA_ROOT, image.name)
            
            with open(image_path, 'wb') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            
            detections = self.detect_objects(image_path)
            
            os.remove(image_path)
            
            return Response({'detections': detections})
        else:
            return Response(serializer.errors, status=400)

    def detect_objects(self, image_path):
        result = subprocess.check_output([os.path.join(DARKNET_PATH, 'darknet'), 'detector', 'test', '../build/darknet/x64/data/obj.data', '../build/darknet/x64/cfg/yolo-obj.cfg', '../build/darknet/x64/backup/yolo-obj_final.weights', image_path], cwd=DARKNET_PATH, text=True)
        return result
