# Network 🗨️ ❤️

**Project 4 of the CS50 Web Development Course with Python and JavaScript**

## Task 💻

**Design a Twitter-like** (now updated to Threads-like) **social network website for making posts and following users.**

## Specification 📝

* **New Post:**  Users who are signed in should be able to write a new text-based post by filling in text into a text area ("New Post" box) and then clicking a button to submit the post.
    - I chose to add the "New Post" box on the All Posts page instead of making it a separate page.
* **All Posts:** The “All Posts” link in the navigation bar should take the user to a page where they can see all posts from all users, with the most recent posts first.
    - Each post includeS the username of the poster, the post content itself, the date and time at which the post was made, and the number of “likes” the post has (this will be 0 for all posts until you implement the ability to “like” a post later).
* **Profile Page:** Clicking on a username loads that user’s profile page. This page displays;
    - The number of followers the user has, as well as the number of accounts the user is following.
    - All the posts of the user in reverse chronological order.
    - For any other user who is signed in, this page also displays a “Follow” or “Unfollow” button that will let the current user toggle whether or not they are following this user’s posts.  
* **Following:** The “Following” link in the navigation bar takes the user to a page where they see all posts made by users that the current user follows.
    - This page behaves just as the “All Posts” page does, just with a more limited set of posts.
    - This page is only available for users who are signed in.
* **Pagination:** On any page that displays posts, posts are only displayed 10 on a page. If there are more than ten posts, a “Next” button appears to take the user to the next page of posts (which should be older than the current page of posts). If not on the first page, a “Previous” button appears to take the user to the previous page of posts as well.
* **Edit Post:** Users are able to click the “Edit” button on any of their own posts to edit that post.
    - When a user clicks “Edit” for one of their own posts, the content of their post is replaced with a textarea where the user can edit the content of their post.
    - The user is then able to “Save” the edited post. JavaScript enables the user to do this without having to reload the page on their browser.
    -  It is not possible for a user, via any route, to edit another user’s posts.
* **Like and Unlike:** Users are able to click a button or link on any post to toggle whether or not they “like” that post.
    - sing JavaScript, one can asynchronously let the server know to update the like count (as via a call to fetch) and then update the post’s like count displayed on the page, without requiring a reload of the entire page.

## Functionality ⚙️

You can the video demonstration of the social media site on YouTube by clicking this [link](https://youtu.be/yT59n7LuXfc).
