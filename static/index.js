function language(){
  language  = $("#language").val();
  // model = $("#model").val();
  console.log("language");
  d3.xhr("/get_language/")
  .header("Content-Type" , "application/json")
  .post(
    JSON.stringify(language),
    function(err, rawData){

      var data = JSON.parse(rawData.response);
      console.log(data);
    })};

function typein(){

  class chat_control{
    constructor(){
      this.msg_list = $('.msg-group');
      console.log(this.msg_list);

    }

    send_msg(name,msg){
      this.msg_list.append(this.get_msg_html(name,msg,'right'));
      this.scroll_to_bottom();
    }

    receive_msg(name,msg){
      this.msg_list.append(this.get_msg_html(name,msg,'left'));
      this.scroll_to_bottom();
    }

    get_msg_html(name, msg, side){
      var msg_temple = `
        <div class="card">
          <div class="card-body">
              <h6 class="card-subtitle mb-2 text-muted text-${side}">${name}</h6>
              <p class="card-text float-${side}">${msg}</p>
          </div>
        </div>
        `;
        return msg_temple;
    }

    scroll_to_bottom(){
      this.msg_list.scrollTop(this.msg_list[0].scrollHeight);

    }
  }


  var chat = new chat_control();

  send_button = $('button');
  var input_box = $('#input-box');
  console.log(input_box);
  console.log(input_box.val());


  function handle_msg(msg){
    msg = msg.trim();
    return msg
  }

  function send_msg(){

    msg = handle_msg(input_box.val());
    console.log(msg);

    if (msg !=''){
      chat.send_msg('you',msg);
      console.log("msg is not null")
      var input={"MESSAGE":input_box.val()}
      input_box.val('');
      console.log("input")
      console.log(input)

      setTimeout(function(){
        d3.xhr("/get_message/")
          .header("Content-Type" , "application/json")
          .post(
            JSON.stringify(input),
            function(err, rawData){
              var data = JSON.parse(rawData.response);
              chat.receive_msg('Mr. Jarvis',data);},1000);
            }
          );
          MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
      }
    }

    function box_key_pressing(){
      if((event.keyCode ===10 || event.keyCode ===13) && event.ctrlKey){
        send_msg();
        $("#input-box").val('');
      }
      if(event.keyCode ===27){
        input_box.blur();
      }
    }
    send_msg();
    box_key_pressing();
  };
