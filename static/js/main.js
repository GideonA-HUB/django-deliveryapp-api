// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Handle address form submission
    const addressForm = document.getElementById('addressForm');
    if (addressForm) {
        addressForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // Add form submission logic here
            console.log('Address form submitted');
        });
    }

    // Handle profile form submission
    const profileForm = document.getElementById('profileForm');
    if (profileForm) {
        profileForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // Add form submission logic here
            console.log('Profile form submitted');
        });
    }

    // Handle password change form submission
    const passwordForm = document.getElementById('passwordForm');
    if (passwordForm) {
        passwordForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // Add form submission logic here
            console.log('Password form submitted');
        });
    }

    // Handle address deletion
    const deleteAddressButtons = document.querySelectorAll('.delete-address');
    deleteAddressButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (confirm('Are you sure you want to delete this address?')) {
                // Add deletion logic here
                console.log('Address deletion confirmed');
            }
        });
    });
}); 