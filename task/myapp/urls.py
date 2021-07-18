from django.urls import path, include
from myapp.views import UserLoginView, UserRegisterView, UserLogoutView, MainView, CreateTestView, ProfileUserView, ProfileUserUpdateView, ListTestView, ListTestDetailView, CommentCreateView, SearchResultsView, quiz_detail_passing, ResultQuiz
from task import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('login/', UserLoginView.as_view(), name='login_page'),
    path('register/', UserRegisterView.as_view(), name='register_page'),
    path('logout/', UserLogoutView.as_view(), name='logout_page'),
    path('accounts/', include('allauth.urls')),
    path('createtest/', CreateTestView , name='createtest'),
    path('profile/<str:username>/', ProfileUserView.as_view(), name='profile'),
    path('profile_update/<str:user__username>/', ProfileUserUpdateView.as_view(), name='profile_update'),
    path('test_all/', ListTestView.as_view(), name='test_all'),
    path('test/<str:title>/', ListTestDetailView.as_view(), name='test'),
    path('comment_create/<int:pk>/', CommentCreateView.as_view(), name='comment_create'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('test_passing/<str:quiz__title>/', quiz_detail_passing, name='test_passing'),
    path('result/<str:quiz__title>', ResultQuiz.as_view(), name='result')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
