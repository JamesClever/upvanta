const menuButton = document.getElementById("menu-toggle");

const navLinks = document.getElementById("nav-links");

if(menuButton){

    menuButton.addEventListener("click", () => {

        navLinks.classList.toggle("active");

    });

}

const profileInput = document.getElementById("profile_picture");
const profilePreview = document.getElementById("profile-preview");

if (profileInput && profilePreview) {
    profileInput.addEventListener("change", function () {
        const file = this.files[0];

        if (file) {
            profilePreview.src = URL.createObjectURL(file);
        }
    });
}