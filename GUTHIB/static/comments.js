// 獲取留言輸入框和留言區域的元素引用
const commentInput = document.getElementById('comment');
const contextsElement = document.querySelector('.contexts');
const extraSpaceAtBottom = 20; // Extra space at the bottom of the comments section

// 初始化樓層和留言區域高度
let commentSectionHeight = contextsElement.getBoundingClientRect().bottom + extraSpaceAtBottom;
let i = 0; // 初始评论数量

// 當按下 Enter 鍵時,添加新留言
commentInput.addEventListener('keydown', function(event) {
  if (event.shiftKey && event.key === 'Enter') {
    // 插入换行符
    commentInput.value;
  } else if (event.key === 'Enter') {
    // 添加留言
    event.preventDefault(); // 只有在没有按下 Shift 键时才阻止默认行为
    $('#submitCommentButton').click();
  }
});

document.getElementById("showCommentButton").addEventListener("click", function() {
  document.getElementById("commentSection").style.display = "block";
  document.getElementById("closeCommentButton").style.display = "inline-block";
  document.getElementById("showCommentButton").style.display = "none";
});

document.getElementById("closeCommentButton").addEventListener("click", function() {
  document.getElementById("commentSection").style.display = "none";
  document.getElementById("showCommentButton").style.display = "inline-block";
  document.getElementById("closeCommentButton").style.display = "none";
});

$(document).ready(function() {
  var articleId = document.querySelector("header ul.bar2 h1").getAttribute("data-article-id");
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
        i = data.length; // 设置评论数量
      },
      error: function() {
        $('#commentsList').html('<p>An error occurred while loading comments.</p>');
      }
    });
  }

  function addCommentElement(poster, commentText, floor) {
    const commentElement = document.createElement('div'); // Create a new div element
    commentElement.classList.add('comment'); // Add 'comment' class
    commentElement.innerHTML = floor + '樓:<br>' + poster + ': ' + commentText.replace(/\n/g, '<br>'); // Set comment content

    // Calculate the new comment's top value
    const newCommentTop = commentSectionHeight;

    // Set the comment's top value
    commentElement.style.top = newCommentTop + 'px';

    // Find the next sibling of contexts and insert the new comment before it
    const nextSibling = contextsElement.nextElementSibling;
    if (nextSibling) {
      nextSibling.parentNode.insertBefore(commentElement, nextSibling);
    } else {
      // If contexts has no next sibling, append the new comment to the parent of contexts
      contextsElement.parentNode.appendChild(commentElement);
    }

    // Update comment section height
    commentSectionHeight += commentElement.getBoundingClientRect().height + extraSpaceAtBottom;
  }

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
            $('#comment').val('');
            $.ajax({
              url: '/api/comments/' + articleId,
              method: 'GET',
              success: function(data) {
                var lastComment = data[data.length - 1];
                addCommentElement(lastComment.poster, lastComment.context, ++i); // Add the new comment to the DOM
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
