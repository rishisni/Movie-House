# Movie House

Movie House is a web application built with Flask that allows users to book movie tickets and manage shows and venues.

## Features

- User registration and authentication
- User and admin roles
- Show listing and booking
- Venue management
- Admin dashboard for show and venue management

## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   
2. Change into the project directory:
   cd movie-house
 
3. Create a virtual environment:
   python3 -m venv venv
   
4. Activate the virtual environment:
   source venv/bin/activate

5. Install the dependencies:
   pip install -r requirements.txt
  
6. Set up the database:
   flask db init
   flask db migrate
   flask db upgrade

7. Start the application:
   flask run


Usage

    Register a new user account or login with existing credentials.
    Admin users can manage venues, shows, and bookings from the admin panel.
    Users can search for shows, book tickets, and view their bookings.   
   
Contributing

Contributions are welcome! If you find any issues or want to add new features, feel free to submit a pull request.


