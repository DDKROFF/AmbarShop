// Mobile Menu Script
document.addEventListener('DOMContentLoaded', function() {
  const burgerMenu = document.querySelector('.burger-menu');
  const mobileNav = document.querySelector('#mobileNav');
  const mobileNavOverlay = document.querySelector('#mobileNavOverlay');
  const closeBtn = document.querySelector('.mobile-close-btn');
  
  if (!burgerMenu || !mobileNav || !mobileNavOverlay) return;
  
  // Open mobile menu
  function openMobileMenu() {
    mobileNav.classList.add('active');
    mobileNavOverlay.classList.add('active');
    burgerMenu.classList.add('active');
    document.body.classList.add('modal-open');
  }
  
  // Close mobile menu
  function closeMobileMenu() {
    mobileNav.classList.remove('active');
    mobileNavOverlay.classList.remove('active');
    burgerMenu.classList.remove('active');
    document.body.classList.remove('modal-open');
  }
  
  // Event listeners
  burgerMenu.addEventListener('click', openMobileMenu);
  
  if (closeBtn) {
    closeBtn.addEventListener('click', closeMobileMenu);
  }
  
  mobileNavOverlay.addEventListener('click', closeMobileMenu);
  
  // Close on escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && mobileNav.classList.contains('active')) {
      closeMobileMenu();
    }
  });
  
  // Close on link click (mobile navigation)
  const mobileNavLinks = mobileNav.querySelectorAll('.mobile-nav-links a');
  mobileNavLinks.forEach(link => {
    link.addEventListener('click', function() {
      // Only close on small screens (check with matchMedia)
      if (window.matchMedia('(max-width: 768px)').matches) {
        closeMobileMenu();
      }
    });
  });
});
