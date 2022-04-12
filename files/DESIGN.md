# Design Document

We decided to implement our project as a website using Python, HTML, CSS, and SQL.
Our website has a similar design/format to the Finance problem set, but just with different functions.
Users are required to register and login to an account so that each user has a personalized experience on the website.
This was implemented in Python code by taking the user input, inserting into our local database file (sneaker.db), and allowing the user to enter a personal "session".
An error apology message appears whenever the user does something wrong to let them know what they did wrong exactly.

Numerous different webpages are accessible within the website, all of which have different purposes (e.g. Upcoming Releases, Add Release, etc.).
This design was to keep these functions organized by separating them as individual HTML files.
We also inserted a nice image of on foot sneakers as the website background to add to the aesthetics. Better than a plain colored background.
Text over the background image is white so that it is easily readible, and tables within the website are grey with black lettering so it is also readible for the user.
The top bar on the website with the title and links to other webpages incorporates the colors white, grey, and blue so that it's design is in sync with the background and content.
A few Bootstrap functions were used, such as every table and the rotating images on the homepage.

The "Upcoming Releases" that user's add via the "Add Release" function are ordered by release date with the nearest release at the top of the table.
This was achieved through an SQL query in our application.py file that ordered the query by date, only if they have not passed the current date yet.
We did this to make it easy for the user to identify which sneakers are releasing and when.
"Past Releases" is designed in a similar way so that the freshly past releases are at the top of the table and the sneakers that released long ago are at the bottom.
The SQL query only selected the user's sneakers that had dates past the current date and ordered them accordingly.
We implemented this design to help users identify which sneakers they just missed out on.

The "Add Sneaker" and "Add Release" inputs are designed in the same order that our database stores the values in to help keep data organized.
(e.g. Brand first, Model second, Colorway third, (Release Date fourth))
"Collection" for each user is alphabetized by the brand of the shoes they own (e.g. Adidas, Balenciaga, Converse, etc.)
The SQL query we used just selected that user's sneakers using their user_id and alphatized the results.
We designed it this way to keep users' sneakers organized for them.
"Community" lets each viewer see other users' collections, and it is alphabetized by username first then by the brand of each shoe.
Our SQL query pulled every sneaker that was not under the current user's id then alphabetized the results by username first then shoe brand.
We designed it like this so the user can see an organized collection for every other user in one place instead of having a scrambled design.

The "Release Info" and "Shops" webpages were designed with equally sized square images of logos from other sneaker websites.
When clicked they take the user to that website using the "a href=" tag in their HTML files.
