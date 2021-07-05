var ProcBehavior = function (val) {
  return val.replace(/\D/g, '').length === 16 ? '0000.0000/0000000-0' : '0000/009999999999';
},
procOptions = {
  onKeyPress: function(val, e, field, options) {
      field.mask(ProcBehavior.apply({}, arguments), options);
    }
};

var FornBehavior = function (val) {
  return val.replace(/\D/g, '').length === 14 ? '00.000.000/0000-00' : '000.000.000-00999';
},
fornOptions = {
  onKeyPress: function(val, e, field, options) {
      field.mask(FornBehavior.apply({}, arguments), options);
    }
};

$(document).ready(function(){
            $('.datemask').mask('00/00/0000');
            $('.fornmask').mask(FornBehavior, fornOptions);
            $('.procmask').mask(ProcBehavior, procOptions);
            $('.moneymask').mask("#.##0,00", {reverse: true});
            $('.cnpjmask').mask('00.000.000/0000-00');
            $('.cpfmask').mask('000.000.000-00');
            $('.cepmask').mask('00000-000');
        });
