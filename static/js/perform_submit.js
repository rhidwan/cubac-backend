$(document).ready(function () {
    $(".ajax-apply-now").click( function (e) {
      e.preventDefault();
        
      let link_url = $(this).attr('href');
    //   let help_elm = $(this).find(".help-text")
    //   let btn_html = btn.html();
        $.confirm({
            theme: 'bootstrap',
             // 'material', 'bootstrap'
            title: 'Attention!',
            content: "Are you Sure you want to Submit the application? You won't be able to change the submitted application Later",
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
                            type: "POST",
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
  