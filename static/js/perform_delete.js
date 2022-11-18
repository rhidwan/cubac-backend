$(document).ready(function () {
    $(".ajax-delete").click( function (e) {
      e.preventDefault();
        
      let link_url = $(this).attr('href');
    //   let help_elm = $(this).find(".help-text")
    //   let btn_html = btn.html();
        $.confirm({
            theme: 'bootstrap',
             // 'material', 'bootstrap'
            title: 'Attention!',
            content: "Are you Sure you want to proceed?",
            buttons:{
                cancel: {
                    text: "Close",
                    btnClass: 'btn btn-light ml-2',
                    action: function(){}

                    //close
                },
                formSubmit: {
                    text: 'Proceed',
                    btnClass: 'btn btn-danger ',
                    action: function () {
                        $.ajax({
                            type: "DELETE",
                            url: link_url,
                            success: function (data) {
                                console.log(data);
                                var res = JSON.parse(JSON.stringify(data));
                                console.log(res);

                                if (res["status"] == "error") {
                                  this.indexValue.help_elm.text(res["msg"]);
                                } else {
                                  location.reload();
                                }
                            }
                        });
                    },
                },
                

            }
  
      
      });
    });
  });
  