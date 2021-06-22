$(".selectitem").click(function () {
          var row = $(this).closest("input");
          $.ajax({
            url: row.attr('data-ajax-url'),
            dataType: 'json',
            success: function (msg) {
              $("#addmensagem").text(msg.addmsg);
              $("#remmensagem").text(msg.remmsg);
            }
          });

        });