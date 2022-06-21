from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from ..models import Question, Answer
from django.db.models import Q, Count

def index(request):
    """
        pybo 목록 출력
        """
    # 입력 인자
    page = request.GET.get('page', '1')  # page
    kw = request.GET.get('kw', '')
    so = request.GET.get('so', 'recent')

    #정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else: #recent
        question_list = Question.objects.order_by('-create_date')


    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()

    # 페이징 처리
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so} #page와 kw가 추가됨
    return render(request, 'pybo/question_list.html', context)



def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.view_count += 1
    question.save()

    so = request.GET.get('so', 'recent')

    #정렬
    if so == 'recommend':
        answer_list = Answer.objects.annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'recent':
        answer_list = Answer.objects.filter(question=question).order_by('create_date')

    # 입력 파라미터
    page_a = request.GET.get('page', '1')

    #조회#########
    #answer_list = Answer.objects.filter(question=question).order_by('create_date')

    #페이징###########
    paginator_a = Paginator(answer_list, 10)
    page_obj_a = paginator_a.get_page(page_a)

    context = {'question': question, 'answer_list': page_obj_a, 'so': so}
    return render(request, 'pybo/question_detail.html', context)

