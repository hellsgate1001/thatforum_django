# That Forum (Django)

## Django version of an online forum

The forum will consist of 2 main sections:

1. Forum, comprising a standard forum with private messaging betwen members
2. User admin, for both individual users and as a whole by admin

### Forum
The basis of the site is a chat forum, not a question and answer forum such as StackOverflow.
Users can post either as a registered user or as an anonymous guest. The ability to switch off anonymous posting will be included.
Forums can be categorised.
#### Pages within forum
All pages within the forum section will contain links to:

1. Register / Login
2. Logout
3. Create a new thread
4. Search threads

The individual pages required are

1. Main / home page. Welcome chat with the list of forum categories (if multiple) and child . Category home pages will be the same, but limited to forums within that category.
2. Forum home page consisting of a list of threads ordered by date of the newest post within the thread. Pagination will be customisable by the user.
3. Thread page consisting of a list of posts associated to that thread ordered by the oldest post. Paginationation will be customisable by the user. A link will also be provided to reply to the thread or an individual post, including the option to quote multiple posts. However, display of quotes will not be nested, ie if a user quotes a post that already includes a quote only a link to the sub-quote will be displayed.
4. Thread create / edit page. Allowing a post title and body. Only the post creator or admin are allowed to edit a post.

### User Admin
Whether logged in as admin or a basic user, the individual user admin page will be the same, allowing editing of personal details and site preferences, eg number of threads or post to paginate by.

Stored user information

1. Username *
2. Password *
3. Email *
4. Preferred pagination number
