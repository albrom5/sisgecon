$(".selectitem").click(function () {
          var row = $(this).closest("input");
          $.ajax({
            url: row.attr('data-ajax-url'),
            dataType: 'json',
            success: function (msg) {
              $("#mensagem").text(msg.msg);
            }
          });

        });