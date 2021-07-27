$("#processo").change(function () {
          var field = $(this).closest("input");
          $.ajax({
            url: field.attr('data-ajax-url'),
            data: {
            'processo': field.val()
            },
            dataType: 'json',
            success: function (data) {
              if (data['isvalid']){
                $("#id_processo").val(data['cod']);
                $("#id_pc").text(data['processo']);
              } else {
                window.alert(data['msg']);
                $("#id_processo").val('');
                $("#id_pc").text('');
                $("#processo").val('');
              }

            }
          });

        });