import csv
from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)


with open('/home/mary/Dev/api_yamdb/api_yamdb/static/data/genre.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        _, created = Genre.objects.get_or_create(
            name=row[1],
            slug=row[2],
        )

with open('/home/mary/Dev/api_yamdb/api_yamdb/static/data/category.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        _, created = Category.objects.get_or_create(
            name=row[1],
            slug=row[2],
        )

with open('/home/mary/Dev/api_yamdb/api_yamdb/static/data/titles.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        _, created = Title.objects.get_or_create(
            name=row[1],
            year=row[2],
            category_id=row[3],
        )

with open('/home/mary/Dev/api_yamdb/api_yamdb/static/data/users.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        _, created = User.objects.get_or_create(
            id=row[0],
            username=row[1],
            email=row[2],
            role=row[3],
            bio=row[4],
            first_name=row[5],
            last_name=row[6],
        )

with open(
    '/home/mary/Dev/api_yamdb/api_yamdb/static/data/genre_title.csv'
) as f:
    reader = csv.reader(f)
    for row in reader:
        _, created = GenreTitle.objects.get_or_create(
            title_id=row[1],
            genre_id=row[2],
        )

with open('/home/mary/Dev/api_yamdb/api_yamdb/static/data/comments.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        _, created = Comment.objects.get_or_create(
            id=row[0],
            review_id=row[1],
            text=row[2],
            author_id=row[3],
            pub_date=row[4],
        )

with open('/home/mary/Dev/api_yamdb/api_yamdb/static/data/review.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        _, created = Review.objects.get_or_create(
            id=row[0],
            title_id=row[1],
            text=row[2],
            author_id=row[3],
            score=row[4],
            pub_date=row[5],
        )