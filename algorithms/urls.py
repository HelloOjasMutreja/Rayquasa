from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.HomeView.as_view(), name='home'),
    
    # Algorithm URLs
    path('algorithms/', views.AlgorithmListView.as_view(), name='algorithm-list'),
    path('algorithms/create/', views.AlgorithmCreateView.as_view(), name='algorithm-create'),
    path('algorithms/<int:pk>/', views.AlgorithmDetailView.as_view(), name='algorithm-detail'),
    path('algorithms/<int:pk>/edit/', views.AlgorithmUpdateView.as_view(), name='algorithm-update'),
    
    # Backtest URLs
    path('algorithms/<int:pk>/backtest/', views.BacktestCreateView.as_view(), name='backtest-create'),
    path('backtests/', views.BacktestListView.as_view(), name='backtest-list'),
    path('backtests/<int:pk>/', views.BacktestDetailView.as_view(), name='backtest-detail'),
]
