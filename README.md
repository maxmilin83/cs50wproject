# Description of project

This is a web project where users can buy and sell cryptocurrencies with a demo balance, more commonly known as paper-trading.
On this web application, a user can create their own account with a demo balance.They can add and withdraw this balance to suit their preferences. The user can edit their profile and reset their password.
The user has access to trade with the top 250 coins by market cap. The user can view all their order history and also
has a portfolio page to keep track of what coins they currently have.
Each coin has a price history chart generated, with three time periods, 24H,w eekly and yearly.



# What’s contained in each file you created.

## Users application

### Python
**Models.py** - Create custom user model, added email and balance field. <br>
**Tokens.py** - Hash code function for account activation <br>
**forms.py** - User registration form , login form ,update form and password reset form <br>
**decorators.py** - Decorator if user is not authenticated. Used in views.py later. <br>
**views.py** - 'activate': used to activate user account  <br>
           'activateEmail': Sends email with instruction to activate account <br>
           'register': View for user registration <br>
           'custom_logout' : Log out <br>
           'custom_login' : Logs user in if username and password valid<br>
           'profile' : Profile page<br>
           'password_change' Password change form<br>
           'password_reset_request' : Password reset, also sends out email with link.<br>
           'passwordResetConfirm' : Confirm password reset<br>

### HTML

**login.html** - Login form using crispy forms. User can login with email or username. Forgot password link and sign up link at bottom.<br>
**logout.html** - Logout page<br>
**profile.html** - Users profile page using crispy forms. Can update name,email and password.<br>
**registration.html** - Registration page using crispy forms.<br>
**password_reset_confirm.html** - Confirm password reset <br>
**template_activate_account.html** - Template text that's sent in the body of the email for account activation<br>
**template_reset_password.html** - Template text that's sent in the body of the email for resetting password<br>

## App1 application

### Python

**views.py** - <br>
'index' : View for home page / index page.<br>
'viewtrending' : View for trending page<br>
'generatetrending' : Returns json response for trending coins list<br>
'orders' : View for orders page<br>
'portfolio' : View for portfolio page<br>
'generatecoins' : Returns json response for top 250 coins list<br>
'generatechart' : Returns json response with timestamps and prices for coin chart, takes input for different time period.<br>
'viewcoin' : View to handle the view coin page. Handles buying and selling via post requests.<br>
'viewfunds' : view for user balance page<br>
'addfunds' : Function that handles adding funds to user balance. Works with HTMX.<br>
'withdrawfunds' : Function that handles adding funds to user balance. Works with HTMX.<br>

**models.py** - Models for the order and portfolio<br>
**coinsapi.py** -<br>
'getcoinslist' - Function that returns a json response containing top 250 coins by market cap<br>
'getcoin' - Function that takes one parameter 'coin' and returns <br>
json response containing data for that coin such as price,market_cap,coin_id,coin_img<br>
'gettrendingcoins' - Function that returns json response of currently trending coins according to coingecko<br>
'getcoinchart' - Function that takes two parameters, coin and days. Returns json response of Unix timestamps and corresponding prices. <br>

### HTML

**All pages except modals extend layout.html**

**messaging.html** - Templates for django messages, for all different message types (error,info,warning,success)<br>
**navbar.html** - Template navbar code using bootstrap, used in all pages. Different sections show/hide based on if user is currently logged in.<br>
**addfunds.html** - Modal pop up for addings funds to user balance, works with HTMX.<br>
**funds.html** - Funds page that shows user balance, and allows user to deposit/withdraw. Depositing/withdrawing triggers corresponding deposit/withdraw modal which is addfunds.html and withdrawfunds.html, respectively.<br>
**index.html** - Home page, renders empty price look up table, which is later dynamically generated with JQuery Datatable.<br>
**layout.html** - Layout for all the pages, includes all stylesheet links and script links. Includes navbar.html and messaging.html
Also includes pagination if it exists. In this case theres only pagination on the orders page<br>
**orders.html** - All the orders for the current user, loops through all orders object and dynamically generates table. Includes pagination.<br>
**portfolio.html** - Portfolio for the current user. renders empty table, which is later dynamically generated with JQuery Datatable.<br>
**trending.html** - Trending page, renders empty trending coins table, which is later dynamically generated with JQuery Datatable.<br>
**viewcoin.html** - Page that shows all info about current coin,filtered by coin ID. Allows user to trade coins via buy and sell. Includes order history at bottom and chart for this coin with 3 different time periods.<br>
**withdrawfunds.html** - Modal pop up for withdrawing funds from user balance, works with HTMX.<br>

### JavaScript

**static/app1/main.js** - JS that generates the JQuery datatable for the index page. Contains several functions<br>
'generatecoins' : Fetches data from /generatecoins, which is an endpoint in the django project defined in urls.py,this returns a JSON response of top 250 coins by market cap. This functions returns this JSON repsonse<br>
'dataSet' : Takes one argument, which is the JSON response from the 'generatecoins' function above, and dynamically generates a JQuery datatable.<br>

-Contains code to show/hide the deposit/withdraw modals.<br>
-Contains code to dynamically update funds on front end after deposit funds post request<br>
-Contains code to validate what user types into the deposit and withdraw modals.<br>

**portfolio.html** - Contains js with same 'generatecoins' and 'dataSet' functions that generate the table in the index page with some slight modification. 'dataSet' now uses .filter and only includes elements from coinsArray which is an array populated with coins derived from all portfolio objects for current user which is passed to the django view as 'coins'.<br>
**trending.html** - Uses exact same JS to generate trending table as the index page, except instead of 'generatecoins', a new function called 'generatetrending' fetches a different API call, that returns the exact same JSON response structure, except its a different list of coins.

**viewcoin.html**- Contains js code that uses asynchronous functions to loads charts based on time period. When user visits coin page, 'loadChartData' is initially called to load chart. Charts are generated using a JS framework called chart.js

-Contains js code that dynamically update values of 'amount' and 'total' input fields when buying and selling coins using event listeners.<br>
-Contains js code that uses SweetAlert2 to generate form validation pop ups and confirmation pop ups <br>
-Contains js code that updates hidden input field values with values that are posted to django via a form.<br>

### CSS

**Styles.CSS** - **contains styles for**

<ol>
  <li>Containers and responsiveness</li>
  <li>Table thats generated accross index,trending and portfolio pages</li>
  <li>Funds page</li>
  <li>Deposit/withdraw modals</li>
  <li>View coin page</li>
  <li>Pagination buttons</li>
</ol>



# How to run your application.

To run the application the user must pip install everything in requirements.txt, you can use pip install -r requirements.txt<br>
The user must then be inside of project1 directory. (Same directory as manage.py)<br>
Then the user must make migrations,<br>
1. python manage.py makemigrations users<br>
2. python manage.py makemigrations app1<br>
3. python manage.py migrate<br><br>
Then user can run the server using python manage.py runserver<br><br>
Note: To bypass email verification when registering for new user, you can just create a super user using python manage.py createsuperuser
and login with that user.

If theres problem with running the project, try deleting , if any, sqlite files such as db.sqlite3 and cache1.sqlite.<br>
You can also delete _pycache_ folders.<br>
After that, do the migrations again<br>

# Distinctiveness and Complexity

I believe my project is distinct from other projects in the CS50W course such as (commerce,network,mail) as the intrinsic idea of my project is different to them projects, one is a social network, one is an ecommerce site, and the other is a mail service. My project is none of these. I am also utilizing all the lessons learned in the course and combining them with all the new tools I learned while building this project.

I believe my project is more complex than other projects in the course such as network and commerce. Network and commerce are complex projects but I think network was the most complex, so I can use that as a reference. Network has a login and registration system, it is a basic yet quite complex django project, that utilises making views, making URLS, handling post and get requests,creating django models and forms,editing and deleting django objects,using JSON responses,django messages,django pagination and more.

I believe my project is more complex as I incorporate everything I mentioned above and more. My project has a more complicated login and registration system which requires users to activate their account via email on registration. Forgot password is included that allows the users to reset their password. Users can also update their profile via an update form. My user model also has a balance field and my models have custom save functions. Throughout my project, I am editing,deleting and updating django objects (when buying/selling coins) and validating everything with javascript. In my project, working with APIs was single-handedly the most complex thing. I had to construct functions that communicate with the API in the way I wanted, which meant different paremeters, and different responses. I made my own JSON responses which included error handling and I also made my own api endpoints, in the django urls.py. Doing something with this data is another story, I generated javascript tables dynamically from the API data using Jquery, when working with large datasets, I had to carefully extract what data I want about what coins, and then decide what goes in each row of table.

I could go into detail on every part but there were many aspects of my project that was quite complicated such as working with HTMX Modals,generating charts based on different time periods and parsing UNIX timestamps to create interactive charts using ChartJS, generating and parsing chart data from API, using JS frameworks throughout project such as SweetAlertJS, using caching,as using a free api key can have performance issues,creating custom decorators,working with APIS using JS and python simultaneously, and more.

# Any other additional information the staff should know about your project.
The project may not work in the future when the API key is no longer valid. To use the project,<br>
you can make an account with coingecko API, at https://www.coingecko.com/en/api.<br>
Then copy your API key from the developer dashboard, and paste it in the API_KEY variable in coinsapi.py.<br>


# References
Django register and login system : https://www.youtube.com/playlist?list=PLbMO9c_jUD44i7AkA4gj1VSKvCFIf59fb
Django HTMX modals https://blog.benoitblanchon.fr/django-htmx-modal-form/
