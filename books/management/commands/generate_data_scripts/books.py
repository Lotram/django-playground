import logging
from datetime import date
from random import choice, choices, randint, sample

from faker import Faker

from books.models import Book, BookTag, Library, Person, Review

from .bulk_creator import BulkCreator
from .utils import DateTimeGenerator, binomial_distribution


logger = logging.getLogger(__name__)

fake = Faker()

review_date_gen = DateTimeGenerator(date(2018, 5, 31), date(2023, 5, 31))
book_date_gen = DateTimeGenerator(date(1923, 5, 31), date(2023, 5, 31))


def book_gen(libraries: list[Library], persons: list[Person]) -> Book:
    return Book(
        title=fake.sentence(nb_words=10, variable_nb_words=True),
        author=choice(persons),
        library=choice(libraries),
        release_date=book_date_gen.date_between(),
    )


def generate_books(
    total_libraries: int,
    total_books: int,
    avg_readers: int,
    max_readers: int,
    persons: list[Person],
) -> None:
    libraries = Library.objects.bulk_create(
        Library(name=fake.company()) for _ in range(total_libraries)
    )

    with BulkCreator(Book, total=total_books, keep_results=True) as bulk_creator:
        bulk_creator.add_many(book_gen(libraries, persons) for _ in range(total_books))

    generate_readings(avg_readers, max_readers, bulk_creator.results, persons)
    generate_book_tags(bulk_creator.results)


def review_gen(book: Book, readers: list[Person]):
    return (
        Review(
            library_id=book.library_id,
            book=book,
            reader=reader,
            rating=randint(0, 10),
            wrote_at=review_date_gen.date_time_between(),
            comments=fake.paragraph(nb_sentences=5),
        )
        for reader in readers
    )


def generate_readings(
    avg_readers: int, max_readers: int, books: list[Book], persons: list[Person]
):
    logger.info(f"Generating around {avg_readers * len(books)} reviews")
    binomial_weights = binomial_distribution(avg_readers, max_readers)
    reader_counts = choices(
        list(range(max_readers + 1)), weights=binomial_weights, k=len(books)
    )
    with BulkCreator(
        Review, keep_results=False, total=sum(reader_counts)
    ) as bulk_creator:
        bulk_creator.add_many(
            review
            for book, reader_count in zip(books, reader_counts)
            for review in review_gen(
                book,
                readers=sample(persons, reader_count),
            )
        )


def generate_book_tags(books: list[Book]):
    avg_tags_per_book = 3
    logger.info(f"Generating around {avg_tags_per_book * len(books)} book tags")
    binomial_weights = binomial_distribution(avg_tags_per_book, len(BookTag.TagName))
    tag_counts = choices(
        list(range(len(BookTag.TagName) + 1)), weights=binomial_weights, k=len(books)
    )
    with BulkCreator(
        BookTag, keep_results=False, total=sum(tag_counts)
    ) as bulk_creator:
        bulk_creator.add_many(
            BookTag(name=tag_name, book=book, library_id=book.library_id)
            for book, tag_count in zip(books, tag_counts)
            for tag_name in sample(BookTag.TagName.values, tag_count)
        )
