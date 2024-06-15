function submitAnswer() {
    let answer_id = $('input[name="answer"]:checked').val();
    if (!answer_id) {
        alert("Please select an answer.");
        return;
    }
    $.ajax({
        url: "{% url 'testing:ajax_answer' %}",
        method: "POST",
        data: {
            'csrfmiddlewaretoken': "{{ csrf_token }}",
            'answer_id': answer_id
        },
        success: function (data) {
            $("#answer-button").hide();
            $("#skip-button").hide();
            if (data.finished) {
                window.location.href = "{% url 'testing:results' %}";
            } else {
                updateQuestion(data);
            }
        },
        error: function (xhr, status, error) {
            console.error(xhr);
        }
    });
}

function skipAnswer() {
    $.ajax({
        url: "{% url 'testing:ajax_answer' %}",
        method: "POST",
        data: {
            'csrfmiddlewaretoken': "{{ csrf_token }}",
            'answer_id': ''  // отправка пустого ответа для пропуска
        },
        success: function (data) {
            $("#answer-button").hide();
            $("#skip-button").hide();
            if (data.finished) {
                window.location.href = "{% url 'testing:results' %}";
            } else {
                updateQuestion(data);
            }
        },
        error: function (xhr, status, error) {
            console.error(xhr);
        }
    });
}

function navigateToQuestion(index) {
    $.ajax({
        url: "{% url 'testing:navigate_question' %}",
        method: "POST",
        data: {
            'csrfmiddlewaretoken': "{{ csrf_token }}",
            'question_index': index
        },
        success: function (data) {
            updateQuestion(data);
        },
        error: function (xhr, status, error) {
            console.error(xhr);
        }
    });
}

function updateQuestion(data) {
    $("#current-question").text(data.current_question);
    $("#question-text").text(data.next_question_text);
    $("#answer-form").empty();
    data.next_answers.forEach(function(answer) {
        $("#answer-form").append(
            `<div>
                <input type="radio" id="answer_${answer.id}" name="answer" value="${answer.id}">
                <label for="answer_${answer.id}">${answer.text_ru}</label>
            </div>`
        );
    });
    $("#answer-form").append('<button type="button" id="answer-button" onclick="submitAnswer()">Answer</button>');
    $("#answer-form").append('<button type="button" id="skip-button" onclick="skipAnswer()">Skip</button>');
    $("#result").text("Correct: " + data.correct_answers + ", Incorrect: " + data.incorrect_answers);

    // Update navigation
    data.question_status.forEach(function(status, index) {
        let questionNav = $("#question-" + index);
        questionNav.removeClass("correct incorrect");
        if (status == 'correct') {
            questionNav.addClass("correct");
        } else if (status == 'incorrect') {
            questionNav.addClass("incorrect");
        }
    });
}
