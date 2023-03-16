from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    
    # one-to-one communication
    authorUser = models.OneToOneField(User, on_delete = models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default = 0)

    def update_rating(self) -> None:
        postRat = self.post_set.aggregate(postRating = Sum("rating"))
        pRat: int = 0
        pRat += postRat.get("postRating")

        commentRat = self.authorUser.comment_set.aggregate(commentRating = Sum("rating"))
        cRat: int = 0
        cRat += commentRat.get("commentRating")

        self.ratingAuthor = pRat*3 + cRat
        self.save()


class Category(models.Model):
    
    name = models.CharField(max_length = 64, unique = True)


class Post(models.Model):
    
    # one-to-many relationship
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
 
    ARTICLE: str = "AR"
    NEWS: str = "NW"

    CATEGORY_CHOICES: list = (
        (ARTICLE, "Статья"),
        (NEWS, "Новость"),
    )

    # selecting the category of the post (article or news), character length = 2, default = "Article"
    categoryType = models.CharField(max_length = 2, choices = CATEGORY_CHOICES, 
                default = ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add = True)
    postCategory = models.ManyToManyField(Category, through = "PostCategory")
    title = models.CharField(max_length = 128)
    text: str = models.TextField() # text article/news
    rating: int = models.SmallIntegerField(default = 0) # rating article/news

    def like(self) -> None:
        self.rating += 1
        self.save()

    def dislike(self) -> None:
        self.rating -= 1
        self.save()

    def preview(self) -> str:
        return self.text[0:123] + "..."


class Comment(models.Model):
    
    # one-to-many relationship
    commentPost = models.ForeignKey(Post, on_delete = models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete = models.CASCADE)

    text = models.TextField() #comment text
    dateCreation = models.DateTimeField(auto_now_add = True)
    rating: int = models.SmallIntegerField(default = 0) #comment rating
    
    def like(self) -> None:
        self.rating += 1
        self.save()

    def dislike(self) -> None:
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    
    # one-to-many relationship
    postThrough = models.ForeignKey(Post, on_delete = models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete = models.CASCADE)

