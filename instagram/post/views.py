from django.shortcuts import render, get_object_or_404, redirect

from .forms import CommentForm
from .models import Post, Comment


def post_list(request):
    posts = Post.objects.all()
    comment_form = CommentForm()
    context = {
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'post/post_list.html', context)


def comment_create(request, post_pk):
    # 요청 메서드가 POST방식 일 때만 처리
    if request.method == 'POST':
        # Post인스턴스를 가져오거나 404 Response를 돌려줌
        post = get_object_or_404(Post, pk=post_pk)
        # request.POST데이터를 이용한 Bounded Form생성
        comment_form = CommentForm(request.POST)
        # 올바른 데이터가 Form인스턴스에 바인딩 되어있는지 유효성 검사
        if comment_form.is_valid():
            # 유효성 검사에 통과하면 Comment객체 생성 및 DB저장
            Comment.objects.create(
                post=post,
                # 작성자는 현재 요청의 사용자로 지정
                author=request.user,
                content=comment_form.cleaned_data['content']
            )
            # 정상적으로 Comment가 생성된 후
            # 'post'네임스페이스를 가진 url의 'post_list'이름에 해당하는 뷰로 이동
            return redirect('post:post_list')
