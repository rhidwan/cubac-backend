$(document).ready(function () {
  $(".form").submit(function (e) {
    e.preventDefault();

    let btn = $(this).find(".ajax-submit");
    let help_elm = $(this).find(".help-text")
    let btn_html = btn.html();

    btn.prop("disabled", true);
    btn.html(
      '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...'
    );

    // avoid to execute the actual submit of the form.
    console.log("form submitted using ajax");
    var form = $(this);
    var form_data = new FormData(form[0]);
    var url = form.attr("action").replace("/undefined/", "");
    console.log(url);

    $.ajax({
      type: "POST",
      url: url,
      data: form_data, // serializes the form's elements.
      indexValue: { btn: btn, btn_html: btn_html , help_elm:help_elm},
      processData: false,
      contentType: false,
      success: function (data) {
        console.log(data);
        var res = JSON.parse(JSON.stringify(data));
        console.log(res);
        this.indexValue.btn.prop("disabled", false);
        this.indexValue.btn.html(this.indexValue.btn_html);

        if (res["status"] == "error") {
          this.indexValue.help_elm.text(res["msg"]);
        } else {
          location.reload();
        }
      },
      error: function (data) {
        var res = JSON.parse(JSON.stringify(data));
        this.indexValue.btn.prop("disabled", false);
        this.indexValue.btn.html(this.indexValue.btn_html);

        if (res["status"] == "error") {
          this.indexValue.help_elm.text(res["msg"]);
        }
      },
    });
  });
});
