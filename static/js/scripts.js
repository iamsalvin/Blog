// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Add animation to like buttons
    const likeButtons = document.querySelectorAll('.btn-like');
    likeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Prevent default action
            e.preventDefault();
            
            // Get the post ID from the data attribute
            const postId = this.getAttribute('data-post-id');
            
            // Send AJAX request to like or unlike the post
            fetch(`/like/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                credentials: 'same-origin'
            })
            .then(response => response.json())
            .then(data => {
                // Update the like count
                const likeCount = document.querySelector(`#like-count-${postId}`);
                if (likeCount) {
                    likeCount.textContent = data.likes_count;
                }
                
                // Toggle the liked class on the button
                if (data.liked) {
                    this.classList.add('liked');
                    this.querySelector('i').classList.remove('far');
                    this.querySelector('i').classList.add('fas');
                } else {
                    this.classList.remove('liked');
                    this.querySelector('i').classList.remove('fas');
                    this.querySelector('i').classList.add('far');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
    
    // Handle comment form submission via AJAX
    const commentForm = document.getElementById('comment-form');
    if (commentForm) {
        commentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const postId = this.getAttribute('data-post-id');
            const commentContent = document.getElementById('id_content').value;
            
            if (!commentContent.trim()) {
                alert('Please enter a comment');
                return;
            }
            
            fetch(`/post/${postId}/comment/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({
                    'content': commentContent,
                    'csrfmiddlewaretoken': getCookie('csrftoken')
                })
            })
            .then(response => {
                if (response.ok) {
                    // Reload the page to show the new comment
                    window.location.reload();
                } else {
                    alert('Error submitting comment. Please try again.');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
    
    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Auto-resize textarea
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    });
    
    // Flash messages fade out
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.add('fade');
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 3000);
    });
    
    // Image preview for post form
    const imageInput = document.getElementById('id_featured_image');
    if (imageInput) {
        imageInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = document.getElementById('image-preview');
                    if (preview) {
                        preview.src = e.target.result;
                        preview.style.display = 'block';
                    } else {
                        const newPreview = document.createElement('img');
                        newPreview.id = 'image-preview';
                        newPreview.src = e.target.result;
                        newPreview.className = 'img-fluid mt-2 rounded';
                        newPreview.style.maxHeight = '300px';
                        imageInput.parentNode.appendChild(newPreview);
                    }
                }
                reader.readAsDataURL(file);
            }
        });
    }
    
    // Profile picture preview
    const profilePicInput = document.getElementById('id_profile_pic');
    if (profilePicInput) {
        profilePicInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = document.getElementById('profile-pic-preview');
                    if (preview) {
                        preview.src = e.target.result;
                    } else {
                        const newPreview = document.createElement('img');
                        newPreview.id = 'profile-pic-preview';
                        newPreview.src = e.target.result;
                        newPreview.className = 'img-fluid mt-2 rounded-circle';
                        newPreview.style.width = '150px';
                        newPreview.style.height = '150px';
                        newPreview.style.objectFit = 'cover';
                        profilePicInput.parentNode.appendChild(newPreview);
                    }
                }
                reader.readAsDataURL(file);
            }
        });
    }
});
