$("#cnpjcpf").change(function () {
          var field = $(this).closest("input");
          $.ajax({
            url: field.attr('data-ajax-url'),
            data: {
            'cnpj_cpf': field.val()
            },
            dataType: 'json',
            success: function (data) {
              if (data['isvalid']){
                $("#id_fornecedor").val(data['cod']);
              } else {
                window.alert(data['msg']);
                $("#id_fornecedor").val('');
              }

            }
          });

        });