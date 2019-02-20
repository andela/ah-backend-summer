[![Build Status](https://travis-ci.org/andela/ah-backend-summer.svg?branch=ch-integrate-travisCI-with-readme-badge-163383166)](https://travis-ci.org/andela/ah-backend-summer)
[![Coverage Status](https://coveralls.io/repos/github/andela/ah-backend-summer/badge.svg?branch=develop)](https://coveralls.io/github/andela/ah-backend-summer?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/27123e7f01956befbc23/maintainability)](https://codeclimate.com/github/andela/ah-backend-summer/maintainability)

# Authors Haven - A Social platform for the creative at heart.

## Vision

Create a community of like minded authors to foster inspiration and innovation
by leveraging the modern web.

---

## Getting Started
- Clone this repository
- Create and activate your [virtual environment](https://virtualenv.pypa.io/en/latest/)
- Install the project requirements: `pip install -r requirements.txt` from the project directory

## API Spec

### Endpoint and Versioning
The API can be accessed at the `/api/{version}` endpoint and is versioned as implied by the endpoint. The current version in development is `v1`.

### Live API and Docs
The API version in `development`, mirroring the `develop` branch is currently hosted at [here](http://ah-backend-summer-staging.herokuapp.com/api/v1/).
The live API docs are hosted [here](http://ah-backend-summer-staging.herokuapp.com/).

The preferred JSON object to be returned by the API should be structured as follows:

### Users (for authentication)

```source-json
{
  "user": {
    "email": "jake@jake.jake",
    "token": "jwt.token.here",
    "username": "jake",
    "first_name": "Jake",
    "last_name": "Doe",
    "bio": "I work at statefarm",
    "image": null
  }
}
```

### Profile

```source-json
{
  "profile": {
    "username": "jake",
    "first_name": "Jake",
    "last_name": "Doe",
    "bio": "I work at statefarm",
    "image": "image-link",
    "following": false
  }
}
```

### Single Article

```source-json
{
  "article": {
    "slug": "how-to-train-your-dragon",
    "title": "How to train your dragon",
    "description": "Ever wonder how?",
    "body": "It takes a Jacobian",
    "tagList": ["dragons", "training"],
    "created_at": "2016-02-18T03:22:56.637Z",
    "updated_at": "2016-02-18T03:48:35.824Z",
    "favorited": false,
    "favorites_count": 0,
    "author": {
      "username": "jake",
      "bio": "I work at statefarm",
      "image": "https://i.stack.imgur.com/xHWG8.jpg",
      "following": false
    }
  }
}
```

### Multiple Articles

```source-json
{
  "articles":[{
    "slug": "how-to-train-your-dragon",
    "title": "How to train your dragon",
    "description": "Ever wonder how?",
    "body": "It takes a Jacobian",
    "tag_list": ["dragons", "training"],
    "created_at": "2016-02-18T03:22:56.637Z",
    "updated_at": "2016-02-18T03:48:35.824Z",
    "favorited": false,
    "favorites_count": 0,
    "author": {
      "username": "jake",
      "bio": "I work at statefarm",
      "image": "https://i.stack.imgur.com/xHWG8.jpg",
      "following": false
    }
  }, {

    "slug": "how-to-train-your-dragon-2",
    "title": "How to train your dragon 2",
    "description": "So toothless",
    "body": "It a dragon",
    "tag_list": ["dragons", "training"],
    "created_at": "2016-02-18T03:22:56.637Z",
    "updated_at": "2016-02-18T03:48:35.824Z",
    "favorited": false,
    "favorites_count": 0,
    "author": {
      "username": "jake",
      "bio": "I work at statefarm",
      "image": "https://i.stack.imgur.com/xHWG8.jpg",
      "following": false
    }
  }],
  "articles_count": 2
}
```

### Single Comment

```source-json
{
  "comment": {
    "id": 1,
    "created_at": "2016-02-18T03:22:56.637Z",
    "updated_at": "2016-02-18T03:22:56.637Z",
    "body": "It takes a Jacobian",
    "author": {
      "username": "jake",
      "bio": "I work at statefarm",
      "image": "https://i.stack.imgur.com/xHWG8.jpg",
      "following": false
    },
    "commenting_on": "lorem ipsum"
  }
}
```

### Multiple Comments

```source-json
{
  "comments": [{
    "id": 1,
    "created_at": "2016-02-18T03:22:56.637Z",
    "updated_at": "2016-02-18T03:22:56.637Z",
    "body": "It takes a Jacobian",
    "author": {
      "username": "jake",
      "bio": "I work at statefarm",
      "image": "https://i.stack.imgur.com/xHWG8.jpg",
      "following": false
    },
    "commenting_on": "lorem ipsum"
  }],
  "comments_count": 1
}
```

### List of Tags

```source-json
{
  "tags": [
    "reactjs",
    "angularjs"
  ]
}
```


### Notification Settings

```source-json
{
    "allow_in_app_notifications": true,
    "allow_email_notifications": false,
}
```

### Errors and Status Codes

If a request fails any validations, expect errors in the following format:

```source-json
{
  "errors":{
    "field_with_error": [
      "can't be empty"
    ]
  }
}
```

### Other status codes:

401 for Unauthorized requests, when a request requires authentication but it isn't provided

403 for Forbidden requests, when a request may be valid but the user does't have permissions to perform the action

404 for Not found requests, when a resource can't be found to fulfill the request

# Endpoints:

Prefix `/api/{version}` is implied.

## Authentication:

`POST /users/login`

Example request body:

```source-json
{
  "user":{
    "email": "jake@jake.jake",
    "password": "jakejake"
  }
}
```

No authentication required, returns a User

Required fields: `email`, `password`

### Registration:

`POST /users`

Example request body:

```source-json
{
  "user":{
    "username": "Jacob",
    "email": "jake@jake.jake",
    "password": "jakejake"
  }
}
```

No authentication required, returns a User

Required fields: `email`, `username`, `password`

### Get Current User

`GET /user`

Authentication required, returns a User that's the current user

### Update User

`PATCH /user`

Example request body:

```source-json
{
  "user":{
    "email": "jake@jake.jake",
    "username": "jake",
    "password": "jakejake"
  }
}
```

Authentication required, returns the User

Accepted fields: `email`, `username`, `password`

## Profiles

### Get Profile

`GET /profiles/:username`

Authentication optional, returns a Profile

### Update Profile

`PUT /profile`

```source-json
{
  "profile": {
    "username": "jake",
    "first_name": "Jake",
    "last_name": "Doe",
    "bio": "I work at statefarm",
    "image": "image-link",
    "date_of_birth": "12/09/1998"
  }
}
```

Accepted fields: `username`, `first_name`, `last_name`, `bio`, `image`

Authentication required, returns the updated Profile

## Following

### Follow user

`POST /profiles/:username/follow`

Authentication required, returns a Profile

No additional parameters required

### Unfollow user

`DELETE /profiles/:username/follow`

Authentication required, returns a Profile

No additional parameters required

## Articles

### List Articles

`GET /articles`

Returns most recent articles globally by default, provide `tag`, `author` or `favorited` query parameter to filter results

Query Parameters:

Filter by tag:

`?tag=AngularJS`

Filter by author:

`?author=jake`

Favorited by user:

`?favorited=jake`

Limit number of articles (default is 20):

`?limit=20`

Offset/skip number of articles (default is 0):

`?offset=0`

Authentication optional, will return multiple articles, ordered by most recent first

### Feed Articles

`GET /articles/feed`

Can also take `limit` and `offset` query parameters like List Articles

Authentication required, will return multiple articles created by followed users, ordered by most recent first.

### Get Article

`GET /articles/:slug`

No authentication required, will return single article

### Create Article

`POST /articles`

Example request body:

```source-json
{
  "article": {
    "title": "How to train your dragon",
    "description": "Ever wonder how?",
    "body": "You have to believe",
    "tag_list": ["reactjs", "angularjs", "dragons"]
  }
}
```

Authentication required, will return an Article

Required fields: `title`, `description`, `body`

Optional fields: `tag_list` as an array of Strings

### Update Article

`PUT /articles/:slug`

Example request body:

```source-json
{
  "article": {
    "title": "Did you train your dragon?"
  }
}
```

Authentication required, returns the updated Article

Optional fields: `title`, `description`, `body`

The `slug` also gets updated when the `title` is changed

### Delete Article

`DELETE /articles/:slug`

Authentication required

## Comments

### Add Comments to an Article

`POST /articles/:slug/comments`

Example request body:

```source-json
{
  "comment": {
    "body": "His name was my name too.",
    "commenting_on": "lorem ipsum"
  }
}
```

Authentication required, returns the created Comment
Required field: `body`

### Get Comments from an Article

`GET /articles/:slug/comments`

Authentication optional, returns multiple comments

### Delete Comment

`DELETE /articles/:slug/comments/:id`

Authentication required

## Favoriting Articles

### Favorite Article

`POST /articles/:slug/favorite`

Authentication required, returns the Article
No additional parameters required

### Unfavorite Article

`DELETE /articles/:slug/favorite`

Authentication required, returns the Article

No additional parameters required

## Like/ Dislike

### Like Article

`POST /articles/:slug/like`

Authentication required

### Undo A Like

`DELETE /articles/:slug/like`

Authentication required

### Dislike Article

`POST /articles/:slug/dislike`

Authentication required

### Undo A Dislike

`DELETE /articles/:slug/dislike`

### Check if an article is liked

`GET /articles/:slug/is-liked`

Authentication required

Returns the like status

```source-json
{
    "is_liked": true
}
```

### Check if an article is disliked

`GET /articles/:slug/is-disliked`

Authentication required

Returns the dislike status

```source-json
{
    "is_disliked": true
}
```

## Tags

### Get Tags

`GET /tags`

No additional parameters required


## Notifications

### Get a user's unread notifications

`GET /notifications`


### Set a user's notifications as read

`POST /notifications/read`

Authentication required

### Get a user's notification settings

`GET /notifications/settings`

Authentication required

### Update a user's notification settings

`PATCH /notifications/settings`

Authentication required

Allows fields displayed in the notification settings `json`, both optional
