
function clearField(target){
    target.value= "";
}



// -------------------- notifications numbers -------------------------
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
    if(ele.target.id !== "notification" && ele.target.id !== "notification-display"){
        $("#notification-display").css('display', 'none');
    }
    
    console.log(ele.target.id)

    // ----------new inbox----------
    if(ele.target.id === 'new-inbox-icon' || ele.target.id === 'new-inbox' || ele.target.id === 'new-inbox-input'|| ele.target.id === 'new-inbox-results'){
        $('#new-inbox').css('display','block');
    }
    else{
        $('#new-inbox').css('display','none');
    }
});
   




// ------------ Inbox Create Profile search --------------

const new_inbox_input = $("#new-inbox-input")
const new_inbox_load_icon = $('#new-inbox-load-icon')
const profile_div = $('#new-inbox-results')
var new_inbox_endpoint = '/direct/profile/'
const delay_by = 700
let scheduled_func = false


let ajax_calling = function (new_inbox_endpoint, request_parameters) {

    $.getJSON(new_inbox_endpoint, request_parameters)
        .done(response => {
            profile_div.fadeTo('slow', 0).promise().then(() => {
                profile_div.html(response['html_from_view'])
                profile_div.fadeTo('slow', 1)
                new_inbox_load_icon.hide()
            })
        })
}

new_inbox_input.on('keyup', function () {
    console.log('new inbox text sent')

    const request_parameters = {
        q: $(this).val() 
    }
    new_inbox_load_icon.show()
    // if scheduled_func is NOT false, cancel the execution of the function
    if (scheduled_func) {
        clearTimeout(scheduled_func)
    }
    // setTimeout returns the ID of the function to be executed
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

const user_input = $("#user-input")
const load_icon = $('#load-icon')
const artists_div = $('#search-results')
const triangle = $('.triangle-up')
const endpoint = '/search/'
const delay_by_in_ms = 700
const scheduled_functio = false

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




//------------------- Comment Form ----------------------

$(document).on('submit','.commentForm', function(e) {
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
        
        success: function(response) {
        $(`#${form.attr('id')} input[name=text]`).val('');

        if(window.location.href.includes("/p/")) {        
            $(`#comment-section-${response['post_id']}`).prepend("<p style='margin-bottom:10% !important;'>  <img class='rounded-circle' src='" +response['photo']+ "' style='width:25px;'><span class='owner-username'>  " + response['owner']+ "</span>  "+ response['text']+"</p>")
        }
        else {
        $(`#comment-section-${response['post_id']}`).prepend("<p><span class='owner-username'>"+response['owner']+'</span> '+response['text']+'</p>')
        }
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
    
    $.get(`/p/${post_id}`, function(response) {
        
        $('#single-post-view').modal('show');

        $('.single-post-content').html(response.html);
        document.body.style.overflow = "hidden";
        
        var new_url = '/p/' + post_id;
        window.history.pushState('data', document.title, new_url);
        
        console.log('successful single-post ajax request')
    }).fail(function() {
        console.log('ERROR in single-post ajax request')
    });
    return false;
});

$(document).on('click','.single-post-view', function(){
    $(this).css('display','none')
    document.body.style.overflow = "scroll";
    window.history.pushState('data', document.title, original_url);
});

$(document).on('click','.single-post-content', function(e){
    e.stopPropagation()
})



// ----------------------Like button functionality----------------------


$(document).on('dblclick', '.post-img', function(){
    var btn = $(this).siblings('.like_btns');

    if($('.like-btn').css('display') == 'none')
        var r = btn.find('.unlike-btn');
    else
        var r = btn.find('.like-btn');
    r.click();
});


function likePost(url,post_id){
    console.log('Requesting Like functionality'); 

    $.post(url, {},  function(response){
        console.log(url, 'finished');
        $(".like-btn-"+post_id).toggle();
        $(".unlike-btn-"+post_id).toggle();
        $(".post-like-"+post_id).html(response.html); 
    }).fail(function(xhr) {
        alert('Like failed with '+xhr.status+' '+url);
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
        alert('Save failed with '+xhr.status+' '+url);
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
    console.log('Requesting Inbox Detail functionality');

    $.get(url, function(response) {
        console.log(url, 'detail finished successfully');
        $("#inbox-detail").html(response.html)

        var new_url = `/direct/t/${inbox_id}`;
        window.history.pushState('data', document.title, new_url);

        var message_section = $(`#message-section-${inbox_id}`)
        message_section[0].scrollTop = message_section[0].scrollHeight - message_section[0].clientHeight;

    }).fail(function(xhr) {
        alert('Save failed with '+xhr.status+' '+url);
    });
}




//---------------------- Message Form--------------------------

$(document).on('submit','.messageForm', function(e) {
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
            var message_section = $(`#message-section-${response['inbox_id']}`)
            message_section.append('<p class="owner_messages"> SENT:  ' +response['text']+ `<small class="text-muted"> ${response['created_at']}</small>` + '</p>')
            message_section[0].scrollTop = message_section[0].scrollHeight - message_section[0].clientHeight;
            
            console.log('successful message sent')
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
            // console.log('0000000000 MESSAGE CAME 0000000000')
            console.log(response.html)
            $(`#message-section-${inbox_id}`).append(response.html)
        },
        complete: function() {
            setTimeout(UpdateMessages, 3100);
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

        $("#inbox-notification").html(response.html); 

        var notif = response.notifications

        $('.inbox').removeClass('unread')
        for(var i=0; i<notif.length; i++){
            $(`#inbox-${notif[i]}`).addClass('unread')
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
        alert('Follow failed with '+xhr.status+' '+'/follow/');
    });
    
    return false;
});





