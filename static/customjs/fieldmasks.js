var ProcBehavior = function (val) {
  return val.replace(/\D/g, '').length === 16 ? '0000.0000/0000000-0' : '0000/009999999999';
},
procOptions = {
  onKeyPress: function(val, e, field, options) {
      field.mask(ProcBehavior.apply({}, arguments), options);
    }
};

$(document).ready(function(){
            $('.datemask').mask('00/00/0000');
            $('.procmask').mask(ProcBehavior, procOptions);
            // $('.procmask').mask('0000.0000/0000000-0');
        });