from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import TradingAlgorithm, BacktestResult
from .forms import TradingAlgorithmForm, BacktestForm
from .backtest_runner import run_backtest
import os


class AlgorithmListView(ListView):
    """List all trading algorithms"""
    model = TradingAlgorithm
    template_name = 'algorithms/algorithm_list.html'
    context_object_name = 'algorithms'
    paginate_by = 10


class AlgorithmDetailView(DetailView):
    """View details of a specific algorithm"""
    model = TradingAlgorithm
    template_name = 'algorithms/algorithm_detail.html'
    context_object_name = 'algorithm'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get recent backtests for this algorithm
        context['recent_backtests'] = self.object.backtests.all()[:5]
        return context


class AlgorithmCreateView(CreateView):
    """Create a new trading algorithm"""
    model = TradingAlgorithm
    form_class = TradingAlgorithmForm
    template_name = 'algorithms/algorithm_form.html'
    success_url = reverse_lazy('algorithm-list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Algorithm "{form.instance.name}" created successfully!')
        return super().form_valid(form)


class AlgorithmUpdateView(UpdateView):
    """Update an existing trading algorithm"""
    model = TradingAlgorithm
    form_class = TradingAlgorithmForm
    template_name = 'algorithms/algorithm_form.html'
    success_url = reverse_lazy('algorithm-list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Algorithm "{form.instance.name}" updated successfully!')
        return super().form_valid(form)


class BacktestCreateView(View):
    """Create and run a new backtest"""
    
    def get(self, request, pk):
        algorithm = get_object_or_404(TradingAlgorithm, pk=pk)
        form = BacktestForm()
        return render(request, 'algorithms/backtest_form.html', {
            'algorithm': algorithm,
            'form': form
        })
    
    def post(self, request, pk):
        algorithm = get_object_or_404(TradingAlgorithm, pk=pk)
        form = BacktestForm(request.POST)
        
        if form.is_valid():
            # Create backtest result
            backtest = BacktestResult.objects.create(
                algorithm=algorithm,
                symbols=form.cleaned_data['symbols'],
                weeks=form.cleaned_data['weeks'],
                initial_cash=form.cleaned_data['initial_cash']
            )
            
            try:
                # Run the backtest
                success = run_backtest(backtest)
                
                if success:
                    messages.success(request, 'Backtest completed successfully!')
                    return redirect('backtest-detail', pk=backtest.pk)
                else:
                    messages.error(request, 'Backtest failed. Please check the symbols and try again.')
                    backtest.delete()
            except Exception as e:
                messages.error(request, f'Error running backtest: {str(e)}')
                backtest.delete()
        
        return render(request, 'algorithms/backtest_form.html', {
            'algorithm': algorithm,
            'form': form
        })


class BacktestDetailView(DetailView):
    """View detailed backtest results"""
    model = BacktestResult
    template_name = 'algorithms/backtest_detail.html'
    context_object_name = 'backtest'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get trade log
        trade_log = self.object.get_trade_log()
        context['trade_log'] = trade_log[-20:] if trade_log else []  # Last 20 trades
        
        # Check if chart exists
        if self.object.chart_path and os.path.exists(self.object.chart_path):
            # Convert absolute path to media URL
            media_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            media_path = os.path.join(media_root, 'media')
            if self.object.chart_path.startswith(media_path):
                context['chart_url'] = self.object.chart_path.replace(media_path, '/media')
        
        return context


class BacktestListView(ListView):
    """List all backtest results"""
    model = BacktestResult
    template_name = 'algorithms/backtest_list.html'
    context_object_name = 'backtests'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        algorithm_id = self.request.GET.get('algorithm')
        if algorithm_id:
            queryset = queryset.filter(algorithm_id=algorithm_id)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['algorithms'] = TradingAlgorithm.objects.all()
        return context


class HomeView(View):
    """Home page"""
    
    def get(self, request):
        algorithms = TradingAlgorithm.objects.all()[:5]
        recent_backtests = BacktestResult.objects.all()[:5]
        
        return render(request, 'algorithms/home.html', {
            'algorithms': algorithms,
            'recent_backtests': recent_backtests
        })

