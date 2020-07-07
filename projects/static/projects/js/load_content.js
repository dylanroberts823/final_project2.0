//start with the first post
let counter = 1;

//Load posts 10 at a time
const quantity = 10;

//When DOM loads, render the first 10 posts
document.addEventListener('DOMContentLoaded', load);

//Load the next set of posts
function load() {

  //Set start and end of post numbers, and update counter
  const start = counter;
  const end = start + quantity - 1;
  counter = end + 1;

  //Open xml request to get new posts
  const xml = new XMLHttpRequest();
  const csrftoken = Cookies.get('csrftoken');
  console.log(csrftoken)
  xml.open('POST', '{% url 'projects:manage' %}',
  {headers: {'X-CSRFToken': csrftoken}});
  xml.onload = () => {
    const data = JSON.parse(xml.responseText);
    data.forEach(add_post);
  };

  //Add start and end points to requst data
  const data = new FormData();
  data.append('start', start);
  data.append('end', end);

  //Send xml
  xml.send(data)
};

//Add a new post with a given contents to DOM
function add_post(contents) {

  //Create new post
  const post = document.createElement('div');
  post.innerHTML = contents;

  //Add post to DOMContentLoadeddocument.querySelector('#posts').append(post);
};
