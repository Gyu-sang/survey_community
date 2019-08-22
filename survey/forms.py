from django import forms
from .models import Post, Withdraw, Deposit, Comment2




class CommentForm2(forms.ModelForm):

    class Meta:
        model = Comment2
        fields = ['message', 'photo']


class PostForm(forms.ModelForm):
    finished_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input','data-target': '#datetimepicker1'}))
    class Meta:
        model = Post
        labels = {
            "title":"제목",
            "link":"링크",
            "content":"내용",
            "finished_at":"마감일",
            "credit":"크레딧",
            "max_participant":"참가자 수",
        }
        help_texts = {
            "credit":"'크레딧 X 참가자 수'로 계산하여 총 크레딧이 차감됩니다."
        }
        widgets = {
            "title": forms.TextInput(attrs={'placeholder': '제목을 입력하세요.'}),
            "link": forms.TextInput(attrs={'placeholder': '설문 링크를 붙여넣으세요.'}),
            "content": forms.Textarea(attrs={'placeholder': '설문 관련하여 유의사항을 적어주세요.'}),
            "credit": forms.TextInput(attrs={'placeholder': '0~100 까지 입력할 수 있습니다.'}),
        }
        fields = ['title', 'content', 'link', 'credit', 'max_participant', 'finished_at']


class WithdrawForm(forms.ModelForm):
    class Meta:
        model = Withdraw
        fields = ['name', 'bank', 'account', 'credit']

class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ['name', 'bank', 'account', 'credit']
