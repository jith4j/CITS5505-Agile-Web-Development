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

$(document).ready(function() {
  $('#ques_ans_list').on('click', '.tab', function() {
      var uid = $(this).data('id')
      $('.tab').removeClass('active'); // Remove 'active' class from all tabs
      $(this).addClass('active'); // Add 'active' class to clicked tab
      var type = $(this).data('tab'); // Get data type (questions or answers)
      var container = $('#content'); 
      container.empty();
      if (type === 'questions') {
          get_u_questions(uid, container);
      } else {
          get_u_answers(uid, container);
      }
  });
});

function get_u_questions(uid, container) {
  $.ajax({
      url: '/uQuestions/' + uid,
      type: 'GET',
      success: function(data) {
          if (data.length > 0) {
              var allQuestions = data.map(a => `<li><strong style="color: grey;">${a.time}:</strong> ${a.question}</li>`).join('');
              container.html(allQuestions);
          } else {
              container.html('<p>No questions found.</p>');
          }
      },
      error: function() {
          container.html('<p>Error retrieving questions. Please try again.</p>');
      }
  });
}

function get_u_answers(uid, container) {
  $.ajax({
      url: '/uAnswers/' + uid,
      type: 'GET',
      success: function(data) {
          if (data.length > 0) {
              var allAnswers = data.map(a => `<li><strong style="color: grey;">${a.time}:</strong> ${a.answer}</li>`).join('');
              container.html(allAnswers);
          } else {
              container.html('<p>No answers found.</p>');
          }
      },
      error: function() {
          container.html('<p>Error retrieving answers. Please try again.</p>');
      }
  });
}

$(document).ready(function () {
  $('#questionList').on('mouseenter', '.question-card', function () {
      console.log("Hovered over question card with ID:", $(this).data('id'));
      var qid = $(this).data('id');
      var container = $('#' + String(qid).trim()); // Access the container by dynamically created ID
      if (container.is(':empty')) {
          console.log("Container is empty, fetching answers...");
          get_answers(qid, container);
      }
  }).on('mouseleave', '.question-card', function () {
      var qid = $(this).data('id');
      $('#' + String(qid).trim()).empty(); // Clear the content
      console.log("Cleared answers on mouse leave...");
  });
});