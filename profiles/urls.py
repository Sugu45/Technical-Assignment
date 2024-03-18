from django.conf import settings
from django.urls import path

from django.conf.urls.static import static
from profiles.controller import profcontroller


urlpatterns = [
            #Task 1
              path('profile_crud', profcontroller.profile_crud, name='profile_crud'),
            #Task 2
              path('stream_sentence/', profcontroller.stream_sentence, name='stream_sentence'),
            #Task 3
              path('cat_list', profcontroller.cat_list, name='cat_list'),
            #Task 5
              path('list-all-posts', profcontroller.list_all_posts, name='list_all_posts'),
              path('filter-posts-by-title', profcontroller.filter_posts_by_title, name='filter_posts_by_title'),
              path('list-posts-by-recent-comments', profcontroller.list_posts_by_recent_comments,
                   name='list_posts_by_recent_comments'),
              path('list-posts-by-created-at', profcontroller.list_posts_by_created_at, name='list_posts_by_created_at'),
              path('delete-posts-if-comments-deleted', profcontroller.delete_posts_if_comments_deleted,
                   name='delete_posts_if_comments_deleted'),
              path('list-posts-with-total-comments', profcontroller.list_posts_with_total_comments,
                   name='list_posts_with_total_comments'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)