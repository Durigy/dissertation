/* reference: https://getbootstrap.com/docs/5.2/components/tooltips/ */
tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

const messageBox = document.getElementById("messages");
//scrollDown()

let socket = io(); // 'http://localhost:5000');

let next_page = 1;
let total_pages = 2;

let message_id_list = [];

let message_field = $('#message-field');
let message_btn = $('#send-btn');

// let initial_load = t;
localStorage.setItem('initial_load', 'true');

// socket.connect({withCredentials: true})

$( document ).ready(() => { 
    socket.on('connect', () => {
        socket.emit('room-connect', {
            'user': `${user_id}`,
            'room': `${thread_id}`
        });
        
        // send messages to fix connection issue
        socket.emit('wake_up',  {'user': 'client-get', 'room': `${thread_id}`, 'message': ''});
        
        // console.log(localStorage.getItem('initial_load'))
        if (localStorage.getItem('initial_load') == 'true') {
            get_messages()
            localStorage.setItem('initial_load', 'false');
        }
    });

    /*socket.on('connect', () => {
        socket.emit('room-connect', {
            'user': `${user_id}`,
            'room': `${thread_id}`
        });
        // console.log('connected');
        // if(next_page > 0) {
            
        get_messages()

        // scrollDown()
        // }
    });*/

    socket.on('disconnect', () => {
        // need to come back and do something here
    });

    socket.on('message', (data) => {
        if ($('#no-messages-here')) {
            message_spacers = $('#no-messages-here').before(
            `<span id="top-message-spacer" class="p-1"></span>
            <span id="bottom-message-spacer" class="p-1"></span>`
        )

            $('#no-messages-here').remove()
        }


        // console.log(data)

        if(data.user == username) {
            displayNewUserMessage(data)
        } else {
            displayNewOtherUserMessage(data)
        }

        // console.log(data.message)

        // tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
        // tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
        
        // if(!messageBox.classList.contains('active')) {
        //     scrollDown()
        // }
    })

    console.log(message_btn.prop('disabled'))

    const sendMessage = () => {
        if(message_btn.prop('disabled') == false) {
            let message_val = $('#message-field')
        
            if(message_val.val() != '') {
                socket.emit("message",  {
                    'user': `${username}`,
                    'user_id': `${user_id}`,
                    'other_user_id': `${other_user_id}`,
                    'room': `${thread_id}`,
                    'message': message_val.val()
                });
                
                message_val.val('')

                // if(!messageBox.classList.contains('active')) {
                //     scrollDown()
                // }
                
                $('#inner_error_message').remove()
            } else {
                $('#inner_error_message').remove()
                $('#error_message').append("<div id='inner_error_message'>Add a message</div>")
            };
        }
    };

    message_btn.on('click touchstart', () => {
        if(message_btn.prop('disabled') == false) {
            sendMessage();
        }
    });

    /* reference: https://youtu.be/Ezj00-Gbdl0 */
    let input = document.getElementById('message-field');

    input.addEventListener('keyup', (e) => {
        if(message_btn.prop('disabled') == false) {
            if(e.keyCode === 13) {
                sendMessage();
            }
        }
    })
});

// detect when the user comes back online
window.addEventListener('online', () => {
    console.log('Became online')
    message_field.removeAttr('disabled')
    message_btn.prop('disabled', false);

    let now = new Date();
    // now.getUTCDate()

    const date_options = { day: 'numeric', month: 'short', year: 'numeric' };
    const time_options = { hour12: false, hour: '2-digit', minute: '2-digit'};

    const utcHours = now.getUTCHours().toString().padStart(2, '0');
    const utcMinutes = now.getUTCMinutes().toString().padStart(2, '0');
    // const formattedTime = now.toLocaleTimeString('en-GB', time_options);
    const formattedDate = now.toLocaleDateString('en-GB', date_options);
    
    // const formattedDateTime = `${formattedTime}, ${formattedDate}`;
    const formattedDateTime = `${utcHours}:${utcMinutes}, ${formattedDate}`;
    
    // console.log(formattedDateTime);

    data = {
        'user': 'Device',
        'message': 'You are online',
        'datetime': formattedDateTime
    }
    
    displayNewOtherUserMessage(data)
});

// detect when the user goes offline
window.addEventListener('offline', () => {
    console.log('You\'ve gone offline')
    message_field.attr('disabled','disabled');
    message_btn.prop('disabled', true);
    // went_offline = true;

    let now = new Date();
    // now.getUTCDate()

    const date_options = { day: 'numeric', month: 'short', year: 'numeric' };
    const time_options = { hour12: false, hour: '2-digit', minute: '2-digit'};

    const utcHours = now.getUTCHours().toString().padStart(2, '0');
    const utcMinutes = now.getUTCMinutes().toString().padStart(2, '0');
    // const formattedTime = now.toLocaleTimeString('en-GB', time_options);
    const formattedDate = now.toLocaleDateString('en-GB', date_options);
    
    // const formattedDateTime = `${formattedTime}, ${formattedDate}`;
    const formattedDateTime = `${utcHours}:${utcMinutes}, ${formattedDate}`;

    data = {
        'user': 'Device',
        'message': 'You are offline',
        'datetime': formattedDateTime
    }

    displayNewOtherUserMessage(data)
});

messageBox.onmouseenter = () => {
    messageBox.classList.add('active')
}

messageBox.onmouseleave = () => {
    messageBox.classList.remove('active')
}

function displayNewUserMessage(data) {
    if (data.message != '') {
        const message = $('#bottom-message-spacer').before(
            `<br>
            <div class="text-end">
                <span data-bs-toggle="tooltip" data-bs-title="${data.datetime}" style="cursor: default;">                
                    <div class="text-wrap text-break my-2 rounded px-4 py-2 my-1 bg-white shadow-sm" style="display: inline; overflow:hidden">
                        ${data.message}
                    </div>
                </span>
            </div>`
        )

        tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
        tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
            
        if(!messageBox.classList.contains('active')) {
            scrollDown()
        }
    }
}

function displayNewOtherUserMessage(data) {
    if (data.message != '') {
        const message = $('#bottom-message-spacer').before(
            `<br>
            <div>
                ${data.user}:
                <span data-bs-toggle="tooltip" data-bs-title="${data.datetime}" style="cursor: default;">
                    <div class="text-wrap text-break my-2 rounded px-4 py-2 my-1 bg-secondary text-white shadow-sm" style="display: inline;">
                        ${data.message}
                    </div>
                </span>
            </div>`
        )

        tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
        tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
            
        if(!messageBox.classList.contains('active')) {
            scrollDown()
        }
    }
}

function displayUserMessage(data, random_string) {
    if (data.message != '') {
        const message = $('#'+random_string+'-message-spacer').before(
            `<br>
            <div class="text-end">
                <span data-bs-toggle="tooltip" data-bs-title="${data.datetime}" style="cursor: default;">                
                    <div class="text-wrap text-break my-2 rounded px-4 py-2 my-1 bg-white shadow-sm" style="display: inline; overflow:hidden">
                        ${data.message}
                    </div>
                </span>
            </div>`
        )
    }
}

function displayOtherUserMessage(data, random_string) {
    if (data.message != '') {
        const message = $('#'+random_string+'-message-spacer').before(
            `<br>
            <div>
                ${data.user}:
                <span data-bs-toggle="tooltip" data-bs-title="${data.datetime}" style="cursor: default;">
                    <div class="text-wrap text-break my-2 rounded px-4 py-2 my-1 bg-secondary text-white shadow-sm" style="display: inline;">
                        ${data.message}
                    </div>
                </span>
            </div>`
        )
    }
}

function get_messages() {
    fetch(`${message_url}?message_page=${next_page}`).then((response) => {
        if(response.status !== 200) {
            // console.log('something wrong')
        }
        // console.log(flask_says)

        response.json().then((data) => {
            if(data.length > 1) {
                if ($('#no-messages-here')) {
                    message_spacers = $('#no-messages-here').before(
                        `<span id="top-message-spacer" class="p-1"></span>
                        <span id="bottom-message-spacer" class="p-1"></span>`
                    )

                    $('#no-messages-here').remove()
                }

                $('#load-more').remove()

                let message_id_list = []

                let current_scroll_height = messageBox.scrollHeight

                // program to generate random strings

                let random_string = Math.random().toString(36).substring(2,9);
                
                let spacer = `<span id="`+random_string+`-message-spacer" class="p-1"></span>`

                const message = $('#top-message-spacer').after(spacer)
                // console.log(data)

                
                for (let i = data.length -1 ; i > 0 ; i--) {
                    let the_data = data[i]
                    if(!message_id_list.includes(the_data.message_id)){
                        message_id_list.unshift(the_data.message_id)

                        if(the_data.user == username) {
                            displayUserMessage(the_data, random_string) 
                        } else if(the_data.user != username) {
                            displayOtherUserMessage(the_data, random_string)
                        }
                    }

                }
                
                // console.log(data[0].next_page)
                // console.log(next_page)


                if(data[0].next_page <= data[0].total_pages) {
                    addBtn()
                }

                next_page += 1

                const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
                const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
                
                // let new_scroll_height = messageBox.scrollHeight

                // console.log(current_scroll_height)
                // console.log(new_scroll_height)


                if (next_page < 3) {
                    // console.log(next_page)
                    scrollDown()
                } else {
                    // console.log('here')
                    let new_scroll_height = messageBox.scrollHeight
            
                    messageBox.scrollTop = new_scroll_height-current_scroll_height - 62
                }
        
                // scrollDownTo(random_string)
            }
        });
    });        
}   

function scrollDownTo(random_string) {
    messageBox.scrollIntoView(`#`+random_string+`-message-spacer`)
}

function addBtn() {
    $('#top-message-spacer').before(
    `<div id="load-more" class="text-center p-1">
        <button id="load-more-messages" class="btn btn-success rounded mt-3" onclick='get_messages()'>Load More</button>
    </div>`
    )
}

function scrollDown() {
    messageBox.scrollTop = messageBox.scrollHeight;
};

window.onbeforeunload = function(){
    localStorage.removeItem('initial_load');
  };