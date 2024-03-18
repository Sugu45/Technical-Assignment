from django.core.paginator import Paginator
from django.db.models import Q,Max
from django.http import HttpResponse, Http404, JsonResponse
import json
import sys
import traceback

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from profiles.models.profilesmodel import Profile,category,PostModel,CommentModel
from profiles.data.responce.profserializers import ProfileSerializer,CategorySerializer,PostSerializer
from django.http import StreamingHttpResponse
import time
import random
from django.http import JsonResponse

#1 Task
@csrf_exempt
@api_view(['GET','POST'])
def profile_crud(request):
    try:
        data = json.loads(request.POST.get('data'))
        action = data.get('action')
        jsondata = data.get('data')
        if (action == 'CREATE'):
            if not jsondata.get('id') is None:
                profile_u = Profile.objects.get(id=jsondata.get('id'))
                profile_u.name = data.get('name', profile_u.name)
                profile_u.email = data.get('email', profile_u.email)
                if 'file' in request.FILES:
                    profile_u.profile_picture = request.FILES['file']
                profile_u.save()
                serializer = ProfileSerializer(profile_u)
                serializer_data = {"data": serializer.data}
            else:
                profile_c = Profile.objects.create(name=jsondata['name'], email=jsondata['email'],
                                            profile_picture=request.FILES.get('file'))
                serializer = ProfileSerializer(profile_c)
                serializer_data = {"data": serializer.data}
            response = HttpResponse(json.dumps(serializer_data), content_type='application/json')
            return response
        elif action == 'FETCH':
            page_number = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 10))
            condtion = Q()
            if jsondata.get('name') is not None and jsondata.get('name') != '':
                condtion &= Q(name__icontains=jsondata.get('name'))
            if jsondata.get('email') is not None and jsondata.get('email') != '':
                condtion &= Q(email__icontains=jsondata.get('email'))
            profiles = Profile.objects.filter(condtion)
            paginator = Paginator(profiles, page_size)
            page_obj = paginator.page(page_number)
            serialized_profiles = ProfileSerializer(page_obj.object_list, many=True).data
            data = {
                'data': serialized_profiles,
                'page_number': page_number,
                'page_size': page_size,
                'total_pages': paginator.num_pages,
                'total_items': paginator.count
            }
            return JsonResponse(data)
        elif action == 'DELETE':
            profile_d = Profile.objects.filter(id=jsondata.get('id')).delete()
            return JsonResponse({'message': 'Profile deleted'})

    except Exception as excep:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        traceback.print_exc()
        error_obj = {}
        error_obj['status'] = "Falied"
        error_obj['message'] = (str(excep) + " - " + str(filename) + ", line_no: " + str(line_number) + str(
                    ', exception_type : {c} '.format(c=type(excep).__name__)))
        return HttpResponse(json.dumps(error_obj, indent=4), content_type='application/json')
#4 Task
@csrf_exempt
@api_view(['GET'])
def cat_list(request):
    try:
        categories = category.objects.all()
        serializer = CategorySerializer(categories, many=True).data
        return JsonResponse(serializer, safe=False)
    except Exception as excep:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        traceback.print_exc()
        error_obj = {}
        error_obj['status'] = "Falied"
        error_obj['message'] = (str(excep) + " - " + str(filename) + ", line_no: " + str(line_number) + str(
                    ', exception_type : {c} '.format(c=type(excep).__name__)))
        return HttpResponse(json.dumps(error_obj, indent=4), content_type='application/json')
#2 Task
def generate_sentence():
    while True:
        sentence = "This is a random sentence: " + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz ', k=20))
        yield sentence + "<br>"
        time.sleep(3)

def stream_sentence(request):
    response = StreamingHttpResponse(generate_sentence(), content_type='text/html')
    return response

#5 Task
# A. List all the posts with comments for each post in serializer
# F. Calculate total number of comments in each post and include it in PostSerializer
@api_view(['GET'])
def list_posts_with_total_comments(request):
    try:
        posts = PostModel.objects.all()
        serializer = PostSerializer(posts, many=True).data
        return JsonResponse(serializer, safe=False)
    except Exception as excep:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        traceback.print_exc()
        error_obj = {}
    error_obj['status'] = "Falied"
    error_obj['message'] = (str(excep) + " - " + str(filename) + ", line_no: " + str(line_number) + str(
                ', exception_type : {c} '.format(c=type(excep).__name__)))
    return HttpResponse(json.dumps(error_obj, indent=4), content_type='application/json')

# B. Filter all posts if title is None
@api_view(['GET'])
def filter_posts_by_title(request):
    try:
        filtered_posts = PostModel.objects.exclude(title__isnull=True)
        serialized_posts = PostSerializer(filtered_posts, many=True).data
        return JsonResponse(serialized_posts, safe=False)
    except Exception as excep:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        traceback.print_exc()
        error_obj = {}
        error_obj['status'] = "Falied"
        error_obj['message'] = (str(excep) + " - " + str(filename) + ", line_no: " + str(line_number) + str(
                    ', exception_type : {c} '.format(c=type(excep).__name__)))
        return HttpResponse(json.dumps(error_obj, indent=4), content_type='application/json')

# C. List the posts based on recent comments
@api_view(['GET'])
def list_posts_by_recent_comments(request):
    try:
        posts_with_recent_comments = PostModel.objects.annotate(recent_comment=Max('commentmodel_set__publication_date'))
        posts_ordered_by_recent_comments = posts_with_recent_comments.order_by('-recent_comment')
        serialized_posts = PostSerializer(posts_ordered_by_recent_comments, many=True).data
        return JsonResponse(serialized_posts, safe=False)
    except Exception as excep:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        traceback.print_exc()
        error_obj = {}
        error_obj['status'] = "Falied"
        error_obj['message'] = (str(excep) + " - " + str(filename) + ", line_no: " + str(line_number) + str(
            ', exception_type : {c} '.format(c=type(excep).__name__)))
        return HttpResponse(json.dumps(error_obj, indent=4), content_type='application/json')

# D. List the posts based on created_at
@api_view(['GET'])
def list_posts_by_created_at(request):
    try:
        posts = PostModel.objects.order_by('-created_at')
        serialized_posts = PostSerializer(posts, many=True).data
        return JsonResponse(serialized_posts, safe=False)
    except Exception as excep:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        traceback.print_exc()
        error_obj = {}
        error_obj['status'] = "Falied"
        error_obj['message'] = (str(excep) + " - " + str(filename) + ", line_no: " + str(line_number) + str(
            ', exception_type : {c} '.format(c=type(excep).__name__)))
        return HttpResponse(json.dumps(error_obj, indent=4), content_type='application/json')

# E. Delete the posts if all the comments in that post are deleted.
@api_view(['GET'])
def delete_posts_if_comments_deleted(request):
    try:
        posts = PostModel.objects.all()
        for post in posts:
            if post.commentmodel_set.count() == 0:
                post.delete()
        return JsonResponse({'message': 'Posts deleted if all comments were deleted'})
    except Exception as excep:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        traceback.print_exc()
        error_obj = {}
        error_obj['status'] = "Falied"
        error_obj['message'] = (str(excep) + " - " + str(filename) + ", line_no: " + str(line_number) + str(
                    ', exception_type : {c} '.format(c=type(excep).__name__)))
        return HttpResponse(json.dumps(error_obj, indent=4), content_type='application/json')

