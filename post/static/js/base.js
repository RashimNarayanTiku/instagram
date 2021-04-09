
function clearField(target){
    target.value= "";
}

// -------------------- Notifications Numbers -------------------------
const user_id = JSON.parse(document.getElementById('user_id').textContent);
const url = `/notification/${user_id}`;

$.get(url, function(response) {
    console.log(url, 'Notification finished successfully');
    $("#notification").html(response.html);  
    if(response.count != 0) {
        $("#notification-dot").css('display','block')
    }

}).fail(function(xhr) {
    console.log('Notification failed with '+xhr.status+' '+url);
});
        


// ---------------------- popup click listener ------------------------

$("body").on('click',function(ele) {

    // search
    if ( ele.target.id === "user-input" ) {
        $("#user-input").css('color', 'black');
    }
    else {
        $("#search-results").css("display", "none");
        $(".triangle-up").css("display",'none');
        $("#user-input").css('color', 'grey');
    }
    
    // ---------notification---------
    if(ele.target.id !== "notification" && ele.target.id !== "notification-display") {
        $("#notification-display").css('display', 'none');
    }    

});
   


// ------------ Inbox Create Profile search --------------

var new_inbox_endpoint = '/direct/profile/';
const delay_by = 700;
let scheduled_func = false;

let ajax_calling = function(new_inbox_endpoint, request_parameters) {

    $.getJSON(new_inbox_endpoint, request_parameters)
        .done(response => {
            $('#new-inbox-results').html(response['html'])
        });
};

$(document).on('keyup', '#new-inbox-input', function(){
    const request_parameters = {
        q: $(this).val() 
    }
    if (scheduled_func) {
        clearTimeout(scheduled_func)
    }
    scheduled_func = setTimeout(ajax_calling, delay_by, new_inbox_endpoint, request_parameters)
});




// ----------------------- notification-display click -------------------------

$(document).on('click','#notification', function(e) {
    
    const user_id = JSON.parse(document.getElementById('user_id').textContent);
    
    $.get(`/notification/display/${user_id}`, function(response) {
        console.log(url, 'Notification finished successfully');           
        $("#notification-display").html(response.html);    
        $("#notification-display").css('display', 'block');   
        $("#notification-dot").css('display','none')
        
    }).fail(function(xhr) {
        console.log('Notification failed with '+xhr.status+' '+url);
    });
});




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




// --------------------Profile search--------------------

let user_input = $("#user-input")
let load_icon = $('#load-icon')
let artists_div = $('#search-results')
let triangle = $('.triangle-up')
let endpoint = '/search/'
let delay_by_in_ms = 700
let scheduled_functio = false

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
    // if scheduled_functio is NOT false, cancel the execution of the function
    if (scheduled_functio) {
        clearTimeout(scheduled_functio)
    }
    // setTimeout returns the ID of the function to be executed
    scheduled_functio = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
});


//------------------- Reply Button-----------------------

$(document).on('click','.reply-btn', function(){
    
    var reply_btn_id = $(this).attr('id').split('-');
    comment_id = reply_btn_id[reply_btn_id.length-1];

    comment_username = $(this).siblings('.owner-username').text();

    var comment_form = $(this).parents('.comment-section').siblings('.modal-footer').children('.commentForm');
    var reply_form = $(this).parents('.comment-section').siblings('.modal-footer').children('.replyForm');
    comment_form.attr('class','replyForm col-12 row');
    comment_form.attr('id',`replyForm-${comment_id}`)
    comment_form.attr('name','replyForm')
    
    reply_form.attr('id',`replyForm-${comment_id}`)
    comment_form.find('#id_text').val(`@${comment_username} `)
    reply_form.find('#id_text').val(`@${comment_username} `)

    comment_form.find('#id_text').focus();
    comment_form.find('#url').val(`/reply/${comment_id}`);
});


//--------------------Reply Form Functionality-----------------

$(document).on('submit','.replyForm', function(){
    var form = $(this).closest('form');

    if(form.find('#id_text').val() == '')
    {
        console.log('Empty Reply stopped') 
        return false;
    }

    $.ajax({
        type:'post',
        url: form.children("#url").val(),
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data:{
            text:form.find("#id_text").val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            action: 'post',
        },
        
        success: function(response) {
            $(`#${form.attr('id')} input[name=text]`).val('');
            $(`#reply-section-${response['comment_id']}`).prepend("<div class='media'><div class='media-left'><img class='rounded-circle' src='"+response['photo']+"'style='width:25px; height:25px;'></div><div class='media-body'><span class='owner-username'> <a href='/"+response['owner']+"/'>"+ response['owner'] +"</a></span>  "+ response['text']+" <br><small class='text-muted'>Now</small></div></div>")

            var reply_form = $(`#replyForm-${response['comment_id']}`);
            reply_form.attr('class','commentForm col-12 row');
            reply_form.attr('id',`commentForm-${response['post_id']}`);
            reply_form.attr('name','commentForm');
            reply_form.find('#url').val(`comment/${response['post_id']}`);
            
        },
        
        error: function(response) {
            console.log('ERROR in Reply ajax request')
        }
    });
    return false;
});

//------------------- Comment Form ----------------------

$(document).on('submit','.commentForm', function(e) {
    var form = $(this).closest('form');

    if(form.find('#id_text').val() == '')
    {
        console.log('Empty Comment stopped') 
        return false;
    }

    $.ajax({
        type:'post',
        url: form.children("#url").val(),
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data:{
            text:form.find("#id_text").val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        
        success: function(response) {
            $(`#${form.attr('id')} input[name=text]`).val('');

            if(form.parent().hasClass('modal-footer')) 
                $(`#comment-section-${response['post_id']}`).prepend("<div class='media'><div class='media-left'><img class='rounded-circle' src='" + response['photo']+
                "'style='width:25px; height:25px;'></div><div class='media-body'><span class='owner-username'><a href='/"+response['owner']+"/'>"+ response['owner'] +"</a></span>  " + response['text']+
                "<br><small class='text-muted'>Now</small><small class='reply-btn text-muted pl-2' id='reply-btn-" + response['comment_id'] + "'style='cursor:pointer;'>Reply</small><div class='reply-section' id='reply-section-" + response['comment_id']+ "'></div></div></div>")
            else 
                form.parent().prev().children('.comment-section').prepend("<p><span class='owner-username'><a href='/" + response['owner'] + "/'>" + response['owner'] + "</a></span> " + response['text'] + '</p>')
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
    
    $.get(`/p/${post_id}`, function(response) {
        
        $('#single-post-view').modal('show');

        $('.single-post-content').html(response.html);        
        
        console.log('successful single-post ajax request')
    }).fail(function() {
        console.log('ERROR in single-post ajax request')
    });
    return false;
});


$(document).on('click','.single-post-content', function(e){
    e.stopPropagation()
})



// ----------------------Like button functionality----------------------


$(document).on('dblclick', '.post-img', function(){
    var heart = $(this).siblings('.heart').first();
    console.log(heart.attr('class'))

    heart.css("display", "inline");    
    heart.css("animation", "1s linear double_burst");    
    
    
    var img_id = $(this).attr('id').split('-');
    post_id = img_id[img_id.length-1];
    btn = $('.like-btn-'+post_id)
    if(btn.css('display')=='none') 
    $('.unlike-btn-'+post_id).click();
    
    setTimeout(function() {
        heart.removeAttr('style');
    }, 1050);
});

function likePost(url,post_id){
    console.log('Requesting Like functionality'); 

    $.post(url, {},  function(response){
        console.log(url, 'finished');
        $(".like-btn-"+post_id).toggle();
        $(".unlike-btn-"+post_id).toggle();
        $(".post-like-"+post_id).html(response.html); 
    }).fail(function(xhr) {
        console.log('Like failed with '+xhr.status+' '+url);
    });
}



// -------------------Like Button Animation-------------------

$(function(){
    $(document).on('mouseup','.like_btn',function(){
        var ele = $(this).find('svg');
        ele.css("animation", "0.45s linear burst");    
    });
});



// -------------------Save Button Functionality-------------------

function savePost(url,post_id){
    console.log('Requesting Save functionality');
    $.post(url, {},  function(){
        console.log(url, 'finished');
        $(".save-btn-"+post_id).toggle();
        $(".unsave-btn-"+post_id).toggle();
    }).fail(function(xhr) {
        console.log('Save failed with '+xhr.status+' '+url);
    });
}



// --------------------Share Profile search-----------------------

const endpointURL = '/share/search/'
const delay_ = 700
let scheduled_fu = false

let ajax_calledd = function (endpointURL, request_parameters) {

    $.getJSON(endpointURL, request_parameters)
        .done(response => {
            console.log(`#share-search-results-${request_parameters['post_id']}`)
            $(`#share-search-results-${request_parameters['post_id']}`).html(response['html_from_view']);
        });
};

$(document).on('keyup','.share-input', function () {
    
    share_id = $(this).attr('id').split('-')
    post_id = share_id[share_id.length-1];
    const request_parameters = {
        q: $(this).val(),
        post_id:post_id,
    }

    if (scheduled_fu) {
        clearTimeout(scheduled_fu)
    }
    scheduled_fu = setTimeout(ajax_calledd, delay_, endpointURL, request_parameters)
});


// --------------------Share Post -----------------------

$(document).on('click','.share-post', function(){

    id = $(this).attr('id').split('-')
    profile_id = id[id.length-1]

    var search_results = $(this).closest('.share-search-results').attr('id').split('-');
    var post_id = search_results[search_results.length-1]
    
    $(`#share-modal-${post_id}`).modal('toggle');
    $(`#share-input-${post_id}`).val('');
    $(`#share-search-results-${post_id}`).html("")


    var url = '/share/'
    var data = {'profile_id':profile_id, 'post_id':post_id}
    
    $.post(url, data, function(){
        console.log("Post shared successfully")
    }).fail(function(xhr) {
        console.log('Post share failed with '+xhr.status+' '+url);
    });
});



// -------------------Inbox Detail Button Functionality-------------------

function inboxDetail(url,inbox_id){

    $('.dropdown-toggle').css('display','none');
    $.get(url, function(response) {
        $("#inbox-detail").html(response.html)

        var new_url = `/direct/t/${inbox_id}`;
        window.history.pushState('data', document.title, new_url);

        var message_section = $(`#message-section-${inbox_id}`)
        message_section[0].scrollTop = message_section[0].scrollHeight - message_section[0].clientHeight;

    }).fail(function(xhr) {
        console.log('Save failed with '+xhr.status+' '+url);
    });
}




//---------------------- Message Form--------------------------

$(document).on('submit','.messageForm', function(e) {
    var form = $(this).closest('form');
    if(form.children('#id_text').val() == '')
    {
        console.log('Empty message stopped') 
        return false;
    }
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
            var message_section = $(`#message-section-${response['inbox_id']}`)
            message_section.append("<div class='row m-2 justify-content-end'><div class='owner_message'>"+ response['text'] +"</div></div>")
            message_section[0].scrollTop = message_section[0].scrollHeight - message_section[0].clientHeight;
        },
        
        error: function(response) {
            console.log('ERROR in message request')
        }
    });
    return false;
});



// ------------------- Message Updating --------------------
var isLoading = false;
function UpdateMessages() {

    var m_id = $('.message-section').attr('id')
    inbox_id = m_id.slice(m_id.lastIndexOf('-')+1,m_id.length);
    
    $.ajax({
        url: `message/update/${inbox_id}`,
        success: function(response) {
            $(`#message-section-${inbox_id}`).append(response.html)
        },
        complete: function() {
            setTimeout(UpdateMessages, 3000);
        }
    });
};



// ------------------ Message Notification ----------------------

var message_notification = setInterval(function(){

    var page_url = window.location.href;
    let inbox_id = '00'
    if(page_url.includes("direct/t")) {        
        inbox_id = page_url.slice(page_url.lastIndexOf('/')+1, page_url.length);
    }    
    var url = `/notification/message/${inbox_id}`

    $.get(url, function(response) {
        console.log('Inbox notification successful');

        $("#inbox-notification .inbox-notif-numbers").html(response.html); 

        var notif = response.notifications

        $('.inbox').removeClass('unread')
        console.log(notif + " are the no of notifs")
        for(var i=0; i<notif.length; i++){
            $(`.inbox-${notif[i]}`).addClass('unread')
        }
    }).fail(function(xhr) {
        console.log('Inbox notification failed with '+xhr.status+' '+url);
    });


}, 1000);



// --------------------------- follow-btn --------------------------

$(document.body).on('click','.follow-btn', function() {
    
    var page_url = window.location.href.split('/');
    user_username = page_url[page_url.length - 2];
    console.log('follow request sent @ /follow/')

    $.post('/follow/',{'username':user_username}, function(response){
        console.log(response.html);
        $('.follow-section').html(response.html)
    }).fail(function(xhr){
        console.log('Follow failed with '+xhr.status+' '+'/follow/');
    });
    
    return false;
});
