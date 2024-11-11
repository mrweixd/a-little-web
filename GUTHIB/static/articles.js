$(document).ready(function() {
    var category = "遊戲"; // Set this to the appropriate category

    function loadArticles() {
        $.ajax({
            url: '/api/articles/' + encodeURIComponent(category),
            method: 'GET',
            success: function(data) {
                console.log('Articles loaded:', data); // Log the loaded articles
                var articlesContainer = $('#articlesContainer');
                articlesContainer.empty();
                data.forEach(function(article) {
                    var articleElement = $('<div class="art"></div>');
                    var articleLink = $('<a></a>').attr('href', '/article/' + article.id).text(article.title);
                    articleElement.append(articleLink);
                    articlesContainer.append(articleElement);
                });
            },
            error: function() {
                $('#articlesContainer').html('<p>An error occurred while loading articles.</p>');
            }
        });
    }

    loadArticles(); // Load articles when the page is ready
});
