// Get references to the comment input field and contexts element
const commentInput = document.getElementById('comment');
const contextsElement = document.querySelector('.contexts');
const extraSpaceAtBottom = 20; // Extra space at the bottom of the comments section

// Initialize comment section height and comment counter
let commentSectionHeight = contextsElement.getBoundingClientRect().bottom + extraSpaceAtBottom;
let i = 0; // Initial number of comments

// Add event listener for Enter key to submit comment
commentInput.addEventListener('keydown', function(event) {
  if (event.shiftKey && event.key === 'Enter') {
    // Allow newline insertion when Shift+Enter is pressed
    commentInput.value;
  } else if (event.key === 'Enter') {
    // Submit comment when Enter is pressed without Shift
    event.preventDefault(); // Prevent default behavior
    $('#submitCommentButton').click();
  }
});

// Show comment section when "Show Comments" button is clicked
document.getElementById("showCommentButton").addEventListener("click", function() {
  document.getElementById("commentSection").style.display = "block";
  document.getElementById("closeCommentButton").style.display = "inline-block";
  document.getElementById("showCommentButton").style.display = "none";
});

// Hide comment section when "Close Comments" button is clicked
document.getElementById("closeCommentButton").addEventListener("click", function() {
  document.getElementById("commentSection").style.display = "none";
  document.getElementById("showCommentButton").style.display = "inline-block";
  document.getElementById("closeCommentButton").style.display = "none";
});

$(document).ready(function() {
  // Get the article ID from the data attribute
  var articleId = document.querySelector("header ul.bar2 h1").getAttribute("data-article-id");

  // Function to load article details
  function loadArticleDetails() {
    $.ajax({
      url: '/api/article/' + articleId,
      method: 'GET',
      success: function(data) {
        if (data.error) {
          $('#articleTitle').text('Article not found');
        } else {
          $('#articleTitle').text(data.title);
          $('#articlePoster').text('Author: ' + data.poster);
          $('#articleContext').text(data.context);
        }
      },
      error: function() {
        $('#articleTitle').text('Error loading article');
      }
    });
  }

  // Function to load comments for the article
  function loadComments() {
    $.ajax({
      url: '/api/comments/' + articleId,
      method: 'GET',
      success: function(data) {
        var commentsList = $('#commentsList');
        commentsList.empty();
        data.forEach(function(comment, index) {
          addCommentElement(comment.poster, comment.context, index + 1);
        });
        i = data.length; // Update comment count
      },
      error: function() {
        $('#commentsList').html('<p>An error occurred while loading comments.</p>');
      }
    });
  }

  // Function to add a comment element to the DOM
  function addCommentElement(poster, commentText, floor) {
    const commentElement = document.createElement('div');
    commentElement.classList.add('comment');
    commentElement.innerHTML = floor + 'F:<br>' + poster + ': ' + commentText.replace(/\n/g, '<br>');

    // Position the new comment
    const newCommentTop = commentSectionHeight;
    commentElement.style.top = newCommentTop + 'px';

    // Insert the new comment after contextsElement
    const nextSibling = contextsElement.nextElementSibling;
    if (nextSibling) {
      nextSibling.parentNode.insertBefore(commentElement, nextSibling);
    } else {
      contextsElement.parentNode.appendChild(commentElement);
    }

    // Update comment section height
    commentSectionHeight += commentElement.getBoundingClientRect().height + extraSpaceAtBottom;
  }

  // Event handler for submitting a comment
  $('#submitCommentButton').click(function() {
    const commentText = commentInput.value.trim();
    if (commentText !== '') {
      $.ajax({
        url: '/api/comments/' + articleId,
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({context: commentText}),
        success: function(response) {
          if (response.success) {
            $('#comment').val(''); // Clear the comment input
            // Fetch and display the latest comment
            $.ajax({
              url: '/api/comments/' + articleId,
              method: 'GET',
              success: function(data) {
                var lastComment = data[data.length - 1];
                addCommentElement(lastComment.poster, lastComment.context, ++i);
              },
              error: function() {
                alert('Error fetching the latest comment');
              }
            });
          } else {
            alert('Error submitting comment');
          }
        },
        error: function(response) {
          console.log('Response:', response);
          if (response.status === 403) {
            alert('You must be logged in to comment');
          } else {
            alert('Error submitting comment');
          }
        }
      });
    }
  });

  loadComments(); // Load comments when the page is ready
});
