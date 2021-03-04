
// --------------------Get cookie function--------------------
function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i < ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }




// --------------------Ajax search--------------------

const user_input = $("#user-input")
const load_icon = $('#load-icon')
const artists_div = $('#search-results')
const triangle = $('.triangle-up')
const endpoint = '/search/'
const delay_by_in_ms = 700
let scheduled_function = false

let ajax_call = function (endpoint, request_parameters) {

    $.getJSON(endpoint, request_parameters)
        .done(response => {
            triangle.fadeTo('slow', 0)
            artists_div.fadeTo('slow', 0).promise().then(() => {
                artists_div.html(response['html_from_view'])
                artists_div.fadeTo('slow', 1)
                triangle.fadeTo('slow', 1)
                load_icon.hide()
            })
        })
}

user_input.on('keyup', function () {
    const request_parameters = {
        q: $(this).val() 
    }
    load_icon.show()
    // if scheduled_function is NOT false, cancel the execution of the function
    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }
    // setTimeout returns the ID of the function to be executed
    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
})

$("body").click(function(ele) {
    if ( ele.target.id === "user-input" ) {
        $("#user-input").css('color', 'black');
    }
    else {
        $("#search-results").css("display", "none");
        $(".triangle-up").css("display",'none');
        $("#user-input").css('color', 'grey');
    }
});



//---------------- Comment Form --------------------
$(document.body).on('submit','.commentForm', function(e) {
    var form = $(this).closest('form');
    $.ajax({
        type:'post',
        url: form.children("#url").val(),
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data:{
            text:form.children("#id_text").val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        
        success: function(response){
        $(`#${form.attr('id')} input[name=text]`).val('');
        $(`#comment-section-${response['post_id']}`).prepend('<p>'+response['text']+'</p>')
        console.log('successful ajax request')

        },
        
        error: function(response) {
            console.log('ERROR in comment ajax request')
        }
    });
    return false;
});



//--------------- Single Post View -------------------

$(document.body).on('click','.all-comments', function(){

    var id = $(this).attr('id');
    post_id = id.slice(id.lastIndexOf('-')+1,id.length);
    original_url = document.URL

    $.ajax({
        type:'GET',
        url: `p/${post_id}`,
        data:{},
        success: function(response){
            $('.single-post-view').css('display','block');
            $('.single-post-content').html(response.html);
            document.body.style.overflow = "hidden";

            var new_url = '/p/' + post_id;
            window.history.pushState('data', document.title, new_url);
            
            console.log('successful single-post ajax request')
        },
        error: function() {
            console.log('ERROR in single-post ajax request')
        }
    });
    return false;
});


$(document.body).on('click','.single-post-view', function(){
    $(this).css('display','none')
    document.body.style.overflow = "scroll";
    window.history.pushState('data', document.title, original_url);
});

$(document.body).on('click','.single-post-content', function(e){
    e.stopPropagation()
});



// ----------------------Like button functionality----------------------

function likePost(url,post_id){
    console.log('Requesting Like functionality'); 

    $.post(url, {},  function(response){
        console.log(url, 'finished');
        $("#like-btn-"+post_id).toggle();
        $("#unlike-btn-"+post_id).toggle();
        $("#post-like-"+post_id).html(response.html); 
    }).fail(function(xhr) {
        alert('Like failed with '+xhr.status+' '+url);
    });
}



// -------------------Like Button Animation-------------------

$(function(){
    $(document).on('mouseup','.like_btns',function(){
        var ele = $(this).find('svg');
        ele.css("animation", "0.45s linear burst");    
    });
});



// -------------------Save Button Functionality-------------------

function savePost(url,post_id){
    console.log('Requesting Save functionality');
    $.post(url, {},  function(){
        console.log(url, 'finished');
        $("#save-btn-"+post_id).toggle();
        $("#unsave-btn-"+post_id).toggle();
    }).fail(function(xhr) {
        alert('Save failed with '+xhr.status+' '+url);
    });
}



// -------------------Inbox Detail Button Functionality-------------------

function inboxDetail(url,inbox_id){
    console.log('Requesting Inbox Detail functionality');

    $.get(url, function(response) {
        console.log(url, 'detail finished successfully');
        $("#inbox-detail").html(response.html)
        var new_url = `/direct/t/${inbox_id}`;
        window.history.pushState('data', document.title, new_url);

    }).fail(function(xhr) {
        alert('Save failed with '+xhr.status+' '+url);
    });
}



//---------------- Message Form--------------------

$(document.body).on('submit','.messageForm', function(e) {
    var form = $(this).closest('form');
    $.ajax({
        type:'post',
        url: form.children("#url").val(),
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data:{
            text:form.children("#id_text").val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        
        success: function(response){
            $(`#${form.attr('id')} input[name=text]`).val('');
            $(`#message-section-${response['inbox_id']}`).append('<p class="owner_messages"> SENT:  ' +response['text']+ `<small class="text-muted"> ${response['created_at']}</small>` + '</p>')
            console.log('successful message request')
        },
        
        error: function(response) {
            console.log('ERROR in comment message request')
        }
    });
    return false;
});


// ------------------- Message Updating --------------------

function UpdateMessages() {

    var m_id = $('.message-section').attr('id')
    inbox_id = m_id.slice(m_id.lastIndexOf('-')+1,m_id.length);
    
    $.ajax({
        
        url: `message/update/${inbox_id}`,
        success: function(response) {
            $(`#message-section-${inbox_id}`).append(response.html)
        },
        complete: function() {
            setTimeout(UpdateMessages, 4000);
        }
    });

};
