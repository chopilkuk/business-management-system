document.addEventListener('DOMContentLoaded', function(){
  var form = document.querySelector('form');
  if(!form) return;
  form.addEventListener('submit', function(e){
    var company = form.querySelector('[name=company_name]');
    var representative = form.querySelector('[name=representative]');
    var brn = form.querySelector('[name=business_registration_number]');
    var email = form.querySelector('[name=e_mail]');
    var phone = form.querySelector('[name=phone_number]');
    var errors = [];

    function patternTest(el, regex, msg){
      if(el && el.value && !regex.test(el.value)) errors.push(msg);
    }

    if(company && !company.value.trim()) errors.push('기업명을 입력하세요.');
    if(representative && !representative.value.trim()) errors.push('대표자명을 입력하세요.');
    if(brn && !brn.value.trim()) errors.push('사업자등록번호를 입력하세요.');
    patternTest(email, /^[^@\s]+@[^@\s]+\.[^@\s]+$/, '유효한 이메일을 입력하세요.');
    patternTest(phone, /^[0-9\-\s+()]+$/, '유효한 전화번호를 입력하세요.');

    if(errors.length){
      e.preventDefault();
      alert(errors.join('\n'));
    }
  });
});
