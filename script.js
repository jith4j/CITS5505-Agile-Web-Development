// function to toggle between sign-in and sign-up

var toggleSignin = false;
function toggleContent(event) {
  console.log(event.target.textContent);
  var signInSection = document.getElementById("signInSection");
  var signUpSection = document.getElementById("signUpSection");
  console.log(signInSection.style.display);

  if (event.target.textContent === "Sign In") {
    signInSection.classList.remove("hide");
    signUpSection.classList.add("hide");
  } else if (event.target.textContent === "Sign Up") {
    signInSection.classList.add("hide");
    signUpSection.classList.remove("hide");
  }
}
