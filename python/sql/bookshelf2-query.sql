
select
    book.isbn as "ISBN",
    book.title as "Title",
    auth.name as "Author",
    pub.name as "Publisher",
    users.fullname as "Owner",
    copies.copy_condition as "Condition"
from
    copies_table copies,
    book_table book,
    author_table auth,
    publisher_table pub,
    user_table users
where
    copies.book_id = book.id
    and copies.owner_id = users.id
    and book.author_id = auth.id
    and book.publisher_id = pub.id 
order by book.title;

