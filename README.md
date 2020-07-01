# final_project
Harvard's CS50 EdX WebProgramming
Project Goal: enable users to post projects they're working on on a publicly-available forum. Allow users to add tags to make their searches filtered. Allow users to register and be added as contributors. Anyone can view the projects as a viewer. Only users can create projects. Projects are managed by managers. Users can offer to become and be contributors. Future iterations will give contributors access to contributor-only features for specific projects. 

The project requires two uses of sql and javascript as well. The SQL code can be found in the request_view and the home_view. The Javascript code can be found in home.html to enable hiding elements when the hide button is clicked, and in the create.html, which enables a confirmation prompt to appear when a form is submitted. 

The user app enables all that is logging in, registering and logging out. 
Inside the user app is models.py, which contains all the models used in the project.
Namely:
- CardClasss: defines the class of cards with different statuses
- Status: defines the different possible statuses of projects and their respective classes
- Tag: defines the different possible tags people can select from
- RequestStatus: defines the different statuses a request can have
- Project: defines the projects that users will define
- Request: defines the requests that users can make to be involved in projects.

The projects app enables all that is project viewing and managing.

In the latter views.py, some of the key functions are:
  - home_view: render the home page with the appropriate base. Non-logged in users are shown a different drop down menu than logged in users.
  - create_tag_view: enables creating a tag
  - create_view: enables creating a project
  - create_request_view: enables creating a request to be involved in a project
  - manage_view: enables viewing all the projects that one manages and contributes to.
  - manage_project_view: enables managers to change the details of the project, including contributors and tags. Future iterations will include an options where managers can create posts. Non-managers see extra information about the project.
  - modify-project_view: enables modifying the project the manger is viewing in manage_project_view
  - request_view: enables users to see all requests, received and sent
  - approve_view and deny_view: enables project managers to approve or deny requests
  - request_modification_view: a former link that enabled approval or denial to happen by url information. Since abandoned, but cannot disable without breaking the code
tors.

