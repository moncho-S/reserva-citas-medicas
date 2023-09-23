document.addEventListener("DOMContentLoaded", function(){
    window.addEventListener('scroll', function() {

        if (window.scrollY > 0) {

          document.getElementById('navbar_top').classList.add('fixed-top');
          // add padding top to show content behind navbar
          navbar_height = document.querySelector('.navbar').offsetHeight;
          document.body.style.paddingTop = navbar_height + 'px';
          
        } else {

          document.getElementById('navbar_top').classList.remove('fixed-top');
           // remove padding top from body
          document.body.style.paddingTop = '0';
        } 

    });

    var togglePassword1 = document.getElementById('closeEyes');
    var togglePassword2 = document.getElementById('openEyes');

    var password = document.getElementById('floatingContraseña');
    togglePassword1.addEventListener('click', () => {
      voltear()
    // Toggle the type attribute using
    // getAttribure() method
    // var type = password.getAttribute('type');
    // console.log(type);
    // if (type == 'password') {
    //   password.setAttribute('type', 'text');
    //   document.getElementById("openEyes").style.display = "block"; 
    //   document.getElementById("closeEyes").style.display = "none"; 
    // }
    // else {
    //   password.setAttribute('type', 'password');
    //   document.getElementById("openEyes").style.display = "none"; 
    //   document.getElementById("closeEyes").style.display = "block"; 
    // }
  
  });
  togglePassword2.addEventListener('click', () => {
    voltear()
  });

  function voltear() {
    var type = password.getAttribute('type');
    console.log(type);
    if (type == 'password') {
      password.setAttribute('type', 'text');
      document.getElementById("openEyes").style.display = "block"; 
      document.getElementById("closeEyes").style.display = "none"; 
    }
    else {
      password.setAttribute('type', 'password');
      document.getElementById("openEyes").style.display = "none"; 
      document.getElementById("closeEyes").style.display = "block"; 
    }
  }
  }); 

  