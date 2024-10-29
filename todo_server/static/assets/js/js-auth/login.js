function togglePasswordVisibility() {
  var passwordField = document.getElementById("floatingPassword");
  var icon = document.getElementById("password_icon");

  if (passwordField.type === "password") {
    // Hiển thị mật khẩu
    passwordField.type = "text";
    icon.src = "../../static/assets/icons/eye.png"; // Đổi sang icon hidden
    icon.alt = "Show password";
  } else {
    // Ẩn mật khẩu
    passwordField.type = "password";
    icon.src = "../../static/assets/icons/hidden.png"; // Đổi lại icon eye
    icon.alt = "Show password";
  }
}
