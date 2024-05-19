// forum.html
function get_answers(qid, container) {
  $.ajax({
    url: "/latestAnswer/" + qid,
    type: "GET",
    success: function (data) {
      console.log("Data received for:", qid, data);
      if (data.length > 0) {
        var allAnswers = data.map((a) => `<p>Answer: ${a.answer}</p>`).join("");
        container.html(allAnswers);
      } else {
        container.html("<p>No answers found.</p>");
      }
    },
    error: function () {
      console.log("Error fetching data for:", qid);
      container.html("<p>Error retrieving answers. Please try again.</p>");
    },
  });
}

// answer.html
function toggleReplyForm(answerId) {
  var form = document.getElementById('reply-form-' + answerId);
  if (form.style.display === 'block') {
      form.style.display = 'none';
  } else {
      form.style.display = 'block';
  }
}

function toggleLike(answerId) {
  var likeIcon = document.getElementById("like-icon-" + answerId);
  var likesCount = document.getElementById("likes-count-" + answerId);

  fetch(`/toggle_like/${answerId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.liked) {
        likeIcon.innerHTML = '<i class="fas fa-heart" style="color: red;"></i>';
      } else {
        likeIcon.innerHTML =
          '<i class="far fa-heart" style="color: gray;"></i>';
      }
      likesCount.textContent = data.likes;
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
