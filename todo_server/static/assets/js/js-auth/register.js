function setGender(value) {
    document.getElementById("genderButton").innerText = value;
    document.getElementById("genderInput").value = value
}

function togglePass() {
    var passwordField = document.getElementById("floatingPassword");
    var pass_icon = document.getElementById("pass_eye");


    if (passwordField.type === "password") {
        // Hiển thị mật khẩu
        passwordField.type = "text";
        pass_icon.src = "../../static/assets/icons/eye.png"; // Đổi sang icon hidden
        pass_icon.alt = "Show password";
    } else {
        // Ẩn mật khẩu
        passwordField.type = "password";
        pass_icon.src = "../../static/assets/icons/hidden.png"; // Đổi lại icon eye
        pass_icon.alt = "Show password";
    }
}

function togglePassAgain() {

    var pass_again = document.getElementById("pass_again");
    var pass_again_icon = document.getElementById("pass_again_eye");

    if (pass_again.type === "password") {
        // Hiển thị mật khẩu
        pass_again.type = "text";
        pass_again_icon.src = "../../static/assets/icons/eye.png"; // Đổi sang icon hidden
        pass_again_icon.alt = "Show password";
    } else {
        // Ẩn mật khẩu
        pass_again.type = "password";
        pass_again_icon.src = "../../static/assets/icons/hidden.png"; // Đổi lại icon eye
        pass_again_icon.alt = "Show password";
    }
}
